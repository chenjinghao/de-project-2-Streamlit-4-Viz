# Tableau Google Sheets Sync Notes

This document preserves the implementation details for the Tableau Public fallback dashboard.

## Why This Exists

The primary dashboard is a Streamlit app connected to PostgreSQL. Tableau Public is useful as an alternate BI view, but the free Tableau Public version cannot connect directly to a private PostgreSQL database. To work around that limitation, I use a scheduled Google Apps Script job to copy the latest modeled PostgreSQL tables into Google Sheets. Tableau Public then reads from the Google Sheet.

## Sync Behavior

- Skips weekends.
- Uses append mode for date-based fact tables.
- Uses upsert mode for company metadata.
- Sends an email alert if some tables fail.
- Sends a critical failure email if the database connection fails.

## Google Apps Script

```javascript
// Extract stock information from PostgreSQL into Google Sheets.
function importPostgresData() {
  // 1. Skip weekends.
  const today = new Date().getDay();
  if (today === 0 || today === 6) {
    Logger.log('Weekend detected. Skipping sync.');
    return;
  }

  const scriptProperties = PropertiesService.getScriptProperties();
  const address = scriptProperties.getProperty('DB_ADDRESS');
  const dbName = scriptProperties.getProperty('DB_NAME');
  const user = scriptProperties.getProperty('DB_USER');
  const password = scriptProperties.getProperty('DB_PASSWORD');
  const alertEmail = scriptProperties.getProperty('EMAIL');

  const syncConfigs = [
    { tableName: 'mart_price_news__analysis', syncMode: 'append', dateColName: 'date', dateColIndex: 1 },
    { tableName: 'biz_info_lookup', syncMode: 'upsert', pkCol: 'Symbol', checkCol: 'LatestQuarter' },
    { tableName: 'mart_price_vol_chgn', syncMode: 'append', dateColName: 'extraction_date', dateColIndex: 1 },
    { tableName: 'stg_price', syncMode: 'append', dateColName: 'extraction_date', dateColIndex: 1 },
    { tableName: 'mart_news__recent', syncMode: 'append', dateColName: 'extraction_date', dateColIndex: 1 }
  ];

  const dbUrl = `jdbc:postgresql://${address}/${dbName}`;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let errorLog = [];

  try {
    const conn = Jdbc.getConnection(dbUrl, user, password);
    const stmt = conn.createStatement();

    for (let i = 0; i < syncConfigs.length; i++) {
      const config = syncConfigs[i];
      const sheet = ss.getSheetByName(config.tableName);

      if (!sheet) {
        Logger.log(`Skipping: Tab named "${config.tableName}" not found.`);
        errorLog.push(`Missing Sheet: ${config.tableName}`);
        continue;
      }

      try {
        Logger.log(`--- Starting sync for ${config.tableName} (${config.syncMode}) ---`);

        if (config.syncMode === 'upsert') {
          let sheetData = sheet.getDataRange().getValues();
          let sheetHeaders = sheetData.length > 0 ? sheetData[0] : [];

          const results = stmt.executeQuery(`SELECT * FROM ${config.tableName}`);
          const metaData = results.getMetaData();
          const numCols = metaData.getColumnCount();

          let dbHeaders = [];
          let pkDbIdx = -1;
          let checkDbIdx = -1;

          for (let c = 1; c <= numCols; c++) {
            const colName = metaData.getColumnName(c);
            dbHeaders.push(colName);
            if (colName === config.pkCol) pkDbIdx = c - 1;
            if (colName === config.checkCol) checkDbIdx = c - 1;
          }

          const dbRows = [];
          while (results.next()) {
            let row = [];
            for (let c = 1; c <= numCols; c++) {
              row.push(results.getString(c));
            }
            dbRows.push(row);
          }
          results.close();

          const isSheetEmpty =
            sheetData.length === 0 ||
            (sheetData.length === 1 && String(sheetData[0][0]).trim() === '');

          if (isSheetEmpty) {
            const fullData = [dbHeaders].concat(dbRows);
            sheet.clear();
            sheet.getRange(1, 1, fullData.length, fullData[0].length).setValues(fullData);
            Logger.log(`Success: ${config.tableName} initial full load (${dbRows.length} rows).`);
            continue;
          }

          const pkSheetIdx = sheetHeaders.indexOf(config.pkCol);
          const checkSheetIdx = sheetHeaders.indexOf(config.checkCol);

          const sheetMap = new Map();
          for (let r = 1; r < sheetData.length; r++) {
            sheetMap.set(String(sheetData[r][pkSheetIdx]).trim(), r);
          }

          let updatedCount = 0;
          let addedCount = 0;

          for (let r = 0; r < dbRows.length; r++) {
            const dbRow = dbRows[r];
            const dbPk = String(dbRow[pkDbIdx]).trim();
            const dbCheck = String(dbRow[checkDbIdx]).trim();

            if (sheetMap.has(dbPk)) {
              const sheetRowIdx = sheetMap.get(dbPk);
              const sheetCheck = String(sheetData[sheetRowIdx][checkSheetIdx]).trim();

              if (dbCheck !== sheetCheck) {
                sheetData[sheetRowIdx] = dbRow;
                updatedCount++;
              }
            } else {
              sheetData.push(dbRow);
              addedCount++;
            }
          }

          sheet.clear();
          sheet.getRange(1, 1, sheetData.length, sheetData[0].length).setValues(sheetData);
          Logger.log(`Success: ${config.tableName} upserted ${updatedCount} updated, ${addedCount} added.`);
        } else if (config.syncMode === 'append') {
          const lastRow = sheet.getLastRow();
          let maxDateStr = null;

          if (lastRow > 1 && config.dateColName) {
            const lastDateVal = sheet.getRange(lastRow, config.dateColIndex).getValue();
            if (lastDateVal instanceof Date) {
              const timeZone = Session.getScriptTimeZone();
              maxDateStr = Utilities.formatDate(lastDateVal, timeZone, 'yyyy-MM-dd');
            } else {
              maxDateStr = lastDateVal.toString().trim();
            }
          }

          let query = `SELECT * FROM ${config.tableName}`;
          if (maxDateStr && config.dateColName) {
            query += ` WHERE ${config.dateColName} > '${maxDateStr}'`;
          }
          if (config.dateColName) {
            query += ` ORDER BY ${config.dateColName} ASC`;
          }

          const results = stmt.executeQuery(query);
          const metaData = results.getMetaData();
          const numCols = metaData.getColumnCount();
          const dataBatch = [];

          if (lastRow === 0) {
            let headers = [];
            for (let col = 1; col <= numCols; col++) {
              headers.push(metaData.getColumnName(col));
            }
            dataBatch.push(headers);
          }

          while (results.next()) {
            let row = [];
            for (let col = 1; col <= numCols; col++) {
              row.push(results.getString(col));
            }
            dataBatch.push(row);
          }
          results.close();

          if (dataBatch.length > 0) {
            const startRow = lastRow === 0 ? 1 : lastRow + 1;
            sheet.getRange(startRow, 1, dataBatch.length, dataBatch[0].length).setValues(dataBatch);
            Logger.log(`Success: ${config.tableName} appended ${lastRow === 0 ? dataBatch.length - 1 : dataBatch.length} rows.`);
          } else {
            Logger.log(`Skipped: ${config.tableName} has no new records.`);
          }
        }
      } catch (tableError) {
        Logger.log(`Error on ${config.tableName}: ${tableError.toString()}`);
        errorLog.push(`Error on ${config.tableName}: ${tableError.toString()}`);
      }
    }

    stmt.close();
    conn.close();

    if (errorLog.length > 0) {
      const sheetUrl = ss.getUrl();
      const body = `Your database sync completed, but some tables failed.\n\nErrors:\n${errorLog.join('\n')}\n\nSheet:\n${sheetUrl}`;
      MailApp.sendEmail(alertEmail, 'Partial Database Sync Failure', body);
    }
  } catch (e) {
    Logger.log('Critical connection error: ' + e.toString());
    MailApp.sendEmail(
      alertEmail,
      'Critical Database Connection Failure',
      `Error:\n${e.toString()}\n\nSheet:\n${SpreadsheetApp.getActiveSpreadsheet().getUrl()}`
    );
  }
}
```
