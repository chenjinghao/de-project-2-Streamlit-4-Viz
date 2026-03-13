# Data Engineering Capstone - Visualization Suite

## 📈 Tickers Analysis Dashboard
> 🌐 **Live Demo:** [JINGHAOdata.engineer](https://www.jinghaodata.engineer/)
Or visit alternative option: [Dashboard make with Tableau Public](https://public.tableau.com/views/TickersAnalysisDashboard/Dashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

<details>

<summary>About the Tableau version of dashboard</summary>
Since Tableau public free version is not able to connect with database directly, hence I use Google Sheet Apps Script scheduled to extract latest available information from the database. 

Then connect the Tableau dashboard with Google Sheet. 

Google Sheet Apps Script is here: 
```javascript
#Extract Stock Info from postgres database
function importPostgresData() {
  // 1. Skip Weekends
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
  
  // 2. 🔴 YOUR MASTER CONTROL CENTER
  // Added 'syncMode' to determine how the table is processed.
  const syncConfigs = [
    { tableName: 'mart_price_news__analysis', syncMode: 'append', dateColName: 'date', dateColIndex: 1 },
    { tableName: 'biz_info_lookup',           syncMode: 'upsert', pkCol: 'Symbol', checkCol: 'LatestQuarter' },
    { tableName: 'mart_price_vol_chgn',       syncMode: 'append', dateColName: 'extraction_date', dateColIndex: 1 },
    { tableName: 'stg_price',                 syncMode: 'append', dateColName: 'extraction_date', dateColIndex: 1 },
    { tableName: 'mart_news__recent',         syncMode: 'append', dateColName: 'extraction_date', dateColIndex: 1 }
  ];

  const dbUrl = `jdbc:postgresql://${address}/${dbName}`;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let errorLog = []; 
  
  try {
    // 3. Open ONE connection for all tables
    const conn = Jdbc.getConnection(dbUrl, user, password);
    const stmt = conn.createStatement();
    
    // 4. Loop through each table configuration
    for (let i = 0; i < syncConfigs.length; i++) {
      const config = syncConfigs[i];
      const sheet = ss.getSheetByName(config.tableName);
      
      if (!sheet) {
        Logger.log(`Skipping: Tab named "${config.tableName}" not found.`);
        errorLog.push(`Missing Sheet: ${config.tableName}`);
        continue; 
      }

      try {
        Logger.log(`--- Starting Sync for: ${config.tableName} (${config.syncMode}) ---`);
        
        // ==========================================
        //         MODE 1: UPSERT LOGIC
        // ==========================================
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

          // Empty sheet fallback (Apps Script returns [['']] for a totally blank sheet)
          const isSheetEmpty = sheetData.length === 0 || (sheetData.length === 1 && String(sheetData[0][0]).trim() === "");
          
          if (isSheetEmpty) {
            const fullData = [dbHeaders].concat(dbRows);
            sheet.clear(); // Wipe the ghost cell
            sheet.getRange(1, 1, fullData.length, fullData[0].length).setValues(fullData);
            Logger.log(`✅ Success: ${config.tableName} - Initial full load (${dbRows.length} rows).`);
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
          Logger.log(`✅ Success: ${config.tableName} - Upserted: ${updatedCount} updated, ${addedCount} added.`);

        // ==========================================
        //         MODE 2: APPEND LOGIC
        // ==========================================
        } else if (config.syncMode === 'append') {
          const lastRow = sheet.getLastRow();
          let maxDateStr = null;
          
          if (lastRow > 1 && config.dateColName) { 
            const lastDateVal = sheet.getRange(lastRow, config.dateColIndex).getValue();
            if (lastDateVal instanceof Date) {
              const timeZone = Session.getScriptTimeZone();
              maxDateStr = Utilities.formatDate(lastDateVal, timeZone, "yyyy-MM-dd");
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
            Logger.log(`✅ Success: ${config.tableName} - Appended ${lastRow === 0 ? dataBatch.length - 1 : dataBatch.length} new rows.`);
          } else {
            Logger.log(`➡️ Skipped: ${config.tableName} - No new records found.`);
          }
        }
        
      } catch (tableError) {
        Logger.log(`❌ Error on ${config.tableName}: ${tableError.toString()}`);
        errorLog.push(`Error on ${config.tableName}: ${tableError.toString()}`);
      }
    } // End of loop
    
    stmt.close();
    conn.close();
    
    if (errorLog.length > 0) {
      const sheetUrl = ss.getUrl();
      const body = `Your database sync completed, but some tables failed.\n\nErrors:\n${errorLog.join('\n')}\n\nSheet:\n${sheetUrl}`;
      MailApp.sendEmail(alertEmail, '⚠️ Partial Database Sync Failure', body);
    }
    
  } catch (e) {
    Logger.log('Critical Connection Error: ' + e.toString());
    MailApp.sendEmail(alertEmail, '🚨 Critical Database Connection Failure', `Error:\n${e.toString()}\n\nSheet:\n${SpreadsheetApp.getActiveSpreadsheet().getUrl()}`);
  }
}
```


</details>


<details>

<summary>Screenshot of the Dashboard</summary>

#### :exclamation: In case the app is down.

<details>

<summary>When the expanders are on: </summary>

![When the expanders are on](static/screencapture-jinghaodata-engineer-expander-on.png)

</details>

<details>

<summary>When the expanders are off: </summary>

![Project Architecture Diagram](static/screencapture-jinghaodata-engineer-expander-off.png)

</details>

</details>

### 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Setup](#-local-setup)
- [Reference](#-reference)


### 🚀 Project Overview
![Tech Stack](https://skills.syvixor.com/api/icons?perline=15&i=googlecloud,python,postgresql,streamlit,tableau,github)

This repository hosts the **Frontend Visualization Suite** for my Data Engineering Capstone Project. It serves as the user-facing layer of a comprehensive data platform, transforming raw financial data processed by my backend pipeline into actionable insights.

This project complements the **Backend ELT Repository**, which handles the ingestion (Airflow), transformation (dbt), and storage (PostgreSQL) of the data visualized here. 
👉 [View Backend Repository](https://github.com/chenjinghao/de-project-1-airflow-dbt-4-ELT)


Together, they demonstrate a full-cycle data engineering workflow—from raw data to decision-ready visualizations.


### 🌟 Features

#### 1. Dashboard UI
The dashboard visualizes the top 3 most actively traded tickers for a selected date.
*   **Automated Data Fetching**: Automatically extracts and renders the latest available data from the database.
*   **Key Metrics**: Visualizes trading volume, price changes, and sentiment analysis.
*   **Layout**: Organized into clear sections (Header, Date Selection, Ticker Data, Disclaimer).
*   **#1 Display**: Always highlights the **#1** most traded ticker by default.
*   **Clean Interface**: Uses `st.expander()` to organize detailed company information, keeping the view uncluttered.


#### 2. Infrastructure

![Project Architecture Diagram](static/img_project-de-workflow_v2-2.png)

<details>

<summary>Infrastructure v1 (Legacy)</summary>

### Google composer + cloud SQL

> *Note: This infrastructure costs approximately USD 50+ per month.*

![Project Architecture Diagram](static/img_project-de-workflow.png)

</details>

#### 3. Additional Capabilities
*   **Interactive "High Five" Counter**: A real-time engagement feature on the 'About Me' page, integrated with the **Google Sheets API**.
*   **Robust Error Handling**: Gracefully handles edge cases for tickers (like ETFs) that may lack specific company metadata or news coverage.
*   **Flexible Environment Switching**: Adapts database connections based on the `ENVIRONMENT` variable in `.streamlit/secrets.toml`.
    *   `development`: Connects to a local PostgreSQL database (Docker).
    *   `production`: Connects to the production PostgreSQL database (Google Cloud VM).

### 🛠️ Tech Stack

*   **Frontend Framework**: Streamlit
*   **Language**: Python
*   **Visualization**: Plotly
*   **Data Manipulation**: Pandas
*   **Database Connectivity**: SQLAlchemy (PostgreSQL)
*   **APIs & Integrations**: 
    *   **Google Sheets API** (`gspread`): For the "High Five" counter.
    *   **Google OAuth2**: Secure service account authentication.
*   **Infrastructure**: Docker (Containerization), Google Cloud Platform (Hosting).

### 📂 Project Structure

```text
de-project-2-Streamlit-4-Viz/
├── home.py                  # Application entry point & Navigation
├── pages/
│   ├── dashboard.py         # Main data visualization dashboard
│   ├── about_project.py     # Architecture documentation
│   └── about_me.py          # Portfolio & High Five counter logic
├── static/                  # Images for dashboard and github repo
├── connection/              
│   ├── database.py          # Database connection logic
├── components/
│   ├── get_data.py          # Data extraction functions
│   └── visualization.py     # Visualization rendering functions
└── README.md
```

### ⚙️ Local Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/chenjinghao/de-project-2-Streamlit-4-Viz.git
    cd de-project-2-Streamlit-4-Viz
    ```
2. **Other components setup**
    * PostgreSQL database running on port 5000 (Separate with Airflow metadatabase)
    * Private Google Sheet (Check reference below) 
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Secrets (Google Sheets Integration)**
    The "High Five" counter requires Google Cloud Service Account credentials.
    
    Create a file named `.streamlit/secrets.toml` in the root directory and add your service account details:

    ```toml
    [mode]
    ENVIRONMENT = "development" # or "production"

    [local_db]
    url = "postgresql://[username]:[password]@[localhost/ip address]:[port]/[database name]"

    [service_account]
    type = "service_account"
    project_id = "your-project-id"
    private_key_id = "your-key-id"
    private_key = "-----BEGIN PRIVATE KEY-----\n..."
    client_email = "your-email@your-project.iam.gserviceaccount.com"
    client_id = "your-client-id"
    # ... include other standard service account fields
    ```

5.  **Run the Application**
    ```bash
    streamlit run home.py
    ```

### Reference
* [Quickstart: Build and deploy a Python (Streamlit) web app to Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-streamlit-service)
* [Streamlit Documentation](https://docs.streamlit.io)
* [Connect Streamlit to a private Google Sheet](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet)

## Connect with me
To know more about me and my projects, please visit my personal website: 
:globe_with_meridians: [https://adamchenjinghao.notion.site](https://adamchenjinghao.notion.site)

:email: [Adam_CJH@outlook.com](mailto:Adam_CJH@outlook.com)
:raising_hand_man: [Linkedin.com/in/chenjinghao/](https://www.linkedin.com/in/adam-cjh)