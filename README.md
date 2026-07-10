# Financial Market Analytics Dashboard
![Tech Stack](https://skills.syvixor.com/api/icons?perline=15&i=googlecloud,python,postgresql,streamlit,tableau,docker,github)

[Live Streamlit Dashboard](https://www.jinghaodata.engineer/) | [Tableau Public Backup](https://public.tableau.com/views/TickersAnalysisDashboard/Dashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) | [Microsoft Fabric & Power BI Version](https://github.com/chenjinghao/ms_fabric_project) | [Backend ELT Repository](https://github.com/chenjinghao/de-project-1-airflow-dbt-4-ELT) | [Portfolio](https://adamchenjinghao.notion.site)

A data engineering portfolio project that turns processed stock-market data into an interactive analytics dashboard. This repository contains the Streamlit visualization layer for a larger end-to-end platform: backend ingestion and transformation happen in a companion Airflow/dbt project, while this app focuses on analysis delivery, dashboard UX, deployment, and stakeholder-facing communication.


**YouTube Demo video:**
[![Watch the video](https://img.youtube.com/vi/HWq92IGbM04/0.jpg)](https://www.youtube.com/watch?v=HWq92IGbM04)


## Why This Project Matters

Hiring managers can use this project to evaluate how I approach a practical data product from raw data to a user-facing dashboard.

- **Data engineering thinking**: Connects a visualization app to a separate ELT pipeline built with Airflow, dbt, and PostgreSQL.
- **Analytics delivery**: Converts price, volume, sentiment, and company metadata into a dashboard that can be explored by date and ticker.
- **Cloud deployment**: Packages the app with Docker and deploys it to Google Cloud Run through Cloud Build.
- **Operational awareness**: Includes environment-based database switching, a Tableau Public fallback path, and error handling for missing ETF/company/news data.
- **Communication**: Presents technical architecture, business context, and interactive analytics in a way that non-engineering stakeholders can inspect.

## Project Overview

This repository hosts the **Frontend Visualization Suite** for my data engineering capstone. The app displays the top 3 most actively traded tickers for a selected trading date and gives users a compact view of market movement, company context, analyst ratings, news sentiment, and relevant articles.

The visualization suite complements my backend ELT repository:

- **Backend ELT repository**: ingests market/news data, transforms it with dbt, and stores modeled tables in PostgreSQL.
- **Frontend visualization repository**: reads modeled PostgreSQL tables and presents the results through Streamlit and Plotly.

Together, the two repositories demonstrate a full-cycle workflow: data ingestion, transformation, storage, deployment, and decision-ready visualization.

## Demo

The primary app is deployed at [JINGHAOdata.engineer](https://www.jinghaodata.engineer/).

If the Streamlit app is unavailable, the Tableau Public version provides an alternate dashboard view:
[Tickers Analysis Dashboard on Tableau Public](https://public.tableau.com/views/TickersAnalysisDashboard/Dashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link).

<details>
<summary>Dashboard screenshots</summary>

Expanded company and sentiment sections:

![Dashboard with expanders open](static/screencapture-jinghaodata-engineer-expander-on.png)

Compact dashboard view:

![Dashboard with expanders closed](static/screencapture-jinghaodata-engineer-expander-off.png)

</details>

## Skills Demonstrated

- **Python application development** with Streamlit
- **Data visualization** with Plotly charts, metrics, tabs, and interactive sections
- **SQL and data access** with SQLAlchemy and PostgreSQL
- **Data manipulation** with Pandas
- **Cloud deployment** using Docker, Cloud Build, and Google Cloud Run
- **API integration** with Google Sheets API and Google service account authentication
- **Dashboard design** for technical and non-technical users
- **System design** across frontend visualization, backend ELT, and fallback BI reporting

## Key Features

### Streamlit Dashboard

- Select a trading date and inspect the top 3 tickers ranked by trading volume.
- Compare closing price, price change, volume, and 100-day averages.
- View candlestick and volume charts for recent price movement.
- Inspect news sentiment and analyst rating distributions.
- Open relevant news articles for the selected ticker and date.
- Keep detailed company information inside expanders so the dashboard stays readable.

### Portfolio Experience

- Includes an "About Me" page with project links, career profile, resume link, and recent milestones.
- Uses a Google Sheets-backed "High Five" counter as a lightweight live API integration.
- Provides a Tableau Public version for viewers who prefer a traditional BI dashboard.

### Reliability and Edge Cases

- Handles tickers such as ETFs that may not have the same company metadata as individual stocks.
- Displays fallback messages when company information, sentiment data, analyst ratings, or news articles are unavailable.
- Supports separate local and deployed database connection modes through environment configuration.

## Architecture

![Project Architecture Diagram](static/img_project-de-workflow_v2-2.png)

The current version uses a lower-cost cloud architecture compared with the original Google Composer and Cloud SQL setup. The Streamlit app is containerized, deployed to Cloud Run, and connected to a PostgreSQL database that stores modeled outputs from the backend ELT pipeline.

<details>
<summary>Legacy infrastructure</summary>

The first architecture used Google Composer and Cloud SQL.

Approximate cost: USD 50+ per month.

![Legacy Project Architecture Diagram](static/img_project-de-workflow.png)

</details>

## Tech Stack

| Area | Tools |
| --- | --- |
| App framework | Streamlit |
| Language | Python |
| Visualization | Plotly |
| Data manipulation | Pandas |
| Database | PostgreSQL |
| Database access | SQLAlchemy, psycopg2, Cloud SQL Python Connector |
| API integration | Google Sheets API, gspread, Google OAuth2 service accounts |
| Deployment | Docker, Google Cloud Build, Google Cloud Run |
| BI fallback | Tableau Public, Google Sheets, Google Apps Script |

## Project Structure

```text
de-project-2-Streamlit-4-Viz/
├── home.py                    # Streamlit entry point and page navigation
├── pages/
│   ├── dashboard.py           # Main financial analytics dashboard
│   ├── about_project.py       # Architecture and project context page
│   └── about_me.py            # Portfolio page and Google Sheets counter
├── components/
│   ├── get_data.py            # PostgreSQL query helpers
│   └── visualization.py       # Streamlit and Plotly rendering functions
├── connection/
│   └── database.py            # Local, production, and legacy Cloud SQL connections
├── static/                    # Architecture diagrams, screenshots, and profile image
├── docs/
│   └── tableau_google_sheets_sync.md  # Tableau fallback sync notes
├── cloudbuild.yaml            # Google Cloud Build and Cloud Run deployment steps
├── Dockerfile                 # Container definition for Cloud Run
├── requirements.txt           # Python dependencies
└── README.md
```

## Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL database populated by the backend ELT project
- Google service account credentials for the Google Sheets counter

### 1. Clone the Repository

```bash
git clone https://github.com/chenjinghao/de-project-2-Streamlit-4-Viz.git
cd de-project-2-Streamlit-4-Viz
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Secrets

Create `.streamlit/secrets.toml` in the project root.

```toml
[mode]
ENVIRONMENT = "development"

[local_db]
url = "postgresql://username:password@localhost:5000/database_name"

[service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-client-cert-url"
```

The local PostgreSQL database should contain the modeled tables produced by the backend ELT project, including:

- `mart_price_news__analysis`
- `biz_info_lookup`
- `mart_price_vol_chgn`
- `stg_price`
- `mart_news__recent`

### 5. Run the Application

```bash
streamlit run home.py
```

## Deployment Notes

The app is designed for Google Cloud Run deployment.

- `Dockerfile` builds a Python 3.11 Streamlit container.
- `cloudbuild.yaml` builds and pushes the image, then deploys it to Cloud Run.
- Production mode expects these deployed secrets or environment variables:
  - `ENVIRONMENT=PRODUCTION`
  - `DATABASE_URL`
  - `gcp_service_acc`

## Tableau Public Fallback

Tableau Public cannot connect directly to a private PostgreSQL database. To provide an alternate dashboard, I built a Google Apps Script sync that periodically extracts modeled PostgreSQL tables into Google Sheets. Tableau Public then connects to the Google Sheet as its data source.

The sync process supports:

- Weekend skips to avoid unnecessary refreshes
- Append logic for date-based fact tables
- Upsert logic for company metadata
- Email alerts for partial or critical failures

See [Tableau Google Sheets Sync Notes](docs/tableau_google_sheets_sync.md) for the implementation details.

## References

- [Backend ELT Repository](https://github.com/chenjinghao/de-project-1-airflow-dbt-4-ELT)
- [Streamlit documentation](https://docs.streamlit.io)
- [Google Cloud Run Streamlit quickstart](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-streamlit-service)
- [Connect Streamlit to a private Google Sheet](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet)

## Connect With Me

- Portfolio: [adamchenjinghao.notion.site](https://adamchenjinghao.notion.site)
- Email: [Adam_CJH@outlook.com](mailto:Adam_CJH@outlook.com)
- LinkedIn: [linkedin.com/in/adam-cjh](https://www.linkedin.com/in/adam-cjh)
