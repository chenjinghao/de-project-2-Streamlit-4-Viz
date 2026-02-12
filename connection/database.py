import streamlit as st
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from google.oauth2 import service_account
import os
import json

def get_engine():
    env = None
    try:
        if st.secrets['mode']['ENVIRONMENT']:
            env = "development"
    except Exception:
        pass

    if not env:
        env = os.environ.get("ENVIRONMENT")

    if env == "development":
        local_url = st.secrets["local_db"]["url"]
        return sqlalchemy.create_engine(local_url)
    
    elif env == "PRODUCTION":
        return sqlalchemy.create_engine(os.environ.get("DATABASE_URL"))
    
    elif env == "CLOUD_SQL":
        # 1. Setup credentials once
        sa_info = json.loads(os.environ.get("gcp_service_acc"))
        creds = service_account.Credentials.from_service_account_info(sa_info)
        
        # 2. Initialize the connector
        connector = Connector(credentials=creds)

        # 3. Define the function that SQLAlchemy will call to get NEW connections
        def getconn():
            return connector.connect(
                os.environ.get("instance_connection_name"),
                "pg8000",
                user=os.environ.get("db_user"),
                password=os.environ.get("db_pass"),
                db=os.environ.get("db_name"),
                ip_type=IPTypes.PUBLIC 
            )

        # 4. Pass the FUNCTION name (getconn), not the result of a call
        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://", 
            creator=getconn
        )
        return engine