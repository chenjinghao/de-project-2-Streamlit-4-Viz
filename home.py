import streamlit as st

# Configure the default settings of the page.
st.set_page_config(
    page_title="JINGHAO's Data Engineering Project",
    page_icon=":material/code_blocks:",
)


pages = {
    "Dashboard": [
        st.Page("pages/dashboard.py", title="Dashboard")
    ],
    "Projects": [
        st.Page("pages/about_project.py", title="About my project"),
    ],
    "About me": [
        st.Page("pages/about_me.py", title="About Me"),
    ],
}

pg = st.navigation(pages, position='top', expanded=True)
pg.run()


from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from google.oauth2 import service_account
import os
import json

def get_engine():
    sa_info = None
    try:
        if "service_account" in st.secrets:
            sa_info = st.secrets["service_account"]
    except Exception:
        pass

    if sa_info is None:
        sa_info = json.loads(os.environ.get("gcp_service_acc"))

    creds = service_account.Credentials.from_service_account_info(sa_info)
    connector = Connector(credentials=creds)

    def getconn():
        conn = None
        try:
            if "db_credentials" in st.secrets:
                conn = connector.connect(
                    st.secrets["db_credentials"]["instance_connection_name"],
                    "pg8000",
                    user=st.secrets["db_credentials"]["db_user"],
                    password=st.secrets["db_credentials"]["db_pass"],
                    db=st.secrets["db_credentials"]["db_name"],
                    ip_type=IPTypes.PUBLIC 
                )
        except Exception:
            pass

        if conn is None:
            conn = connector.connect(
                os.environ.get("instance_connection_name"),
                "pg8000",
                user=os.environ.get("db_user"),
                password=os.environ.get("db_pass"),
                db=os.environ.get("db_name"),
                ip_type=IPTypes.PUBLIC 
            )
        return conn

    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    return engine

st.title("PostgreSQL + VPC Data")

engine = get_engine()

query = "SELECT * FROM mart_price_news__analysis LIMIT 10"
with engine.connect() as conn:
    rows = conn.execute(sqlalchemy.text(query)).fetchall()
    st.table(rows)