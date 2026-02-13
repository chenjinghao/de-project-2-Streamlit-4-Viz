# Data Engineering Capstone - Visualization Suite

## 📈 Tickers Analysis Dashboard
> 🌐 **Live Demo:** [JINGHAOdata.engineer](https://www.jinghaodata.engineer/)

### 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Setup](#-local-setup)
- [Reference](#-reference)


### 🚀 Project Overview

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

![Project Architecture Diagram](static\img_project-de-workflow_v2-2.png)

<details>

<summary>Infrastructure v1 (Legacy)</summary>

### Google composer + cloud SQL

> *Note: This infrastructure costs approximately USD 50+ per month.*

![Project Architecture Diagram](static\img_project-de-workflow.png)

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
