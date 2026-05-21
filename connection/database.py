import streamlit as st
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from google.oauth2 import service_account
import os
import json

def _get_secret(section, key=None, default=None):
    try:
        value = st.secrets.get(section, default)
        if key is None:
            return value
        return value.get(key, default) if value else default
    except Exception:
        return default

def _is_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y"}

def get_engine():
    env = _get_secret("mode", "ENVIRONMENT") or os.environ.get("ENVIRONMENT") or "development"
    env = str(env).strip().upper()

    if env == "DEVELOPMENT":
        use_cloud_test = _is_truthy(_get_secret("local_test_cloud_db", "cloud_test", False))
        local_url = (
            _get_secret("local_test_cloud_db", "url")
            if use_cloud_test
            else _get_secret("local_db", "url")
        )

        if not local_url:
            raise RuntimeError(
                "Missing local database URL. Set [local_db].url in .streamlit/secrets.toml."
            )

        return sqlalchemy.create_engine(local_url)
    
    elif env == "PRODUCTION":
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise RuntimeError("Missing DATABASE_URL environment variable for PRODUCTION mode.")

        return sqlalchemy.create_engine(database_url)
    
    # At first, the project was previously deployed on GCP Cloud SQL
    elif env == "CLOUD_SQL":
        # 1. Setup credentials once
        gcp_service_acc = os.environ.get("gcp_service_acc")
        if not gcp_service_acc:
            raise RuntimeError("Missing gcp_service_acc environment variable for CLOUD_SQL mode.")

        sa_info = json.loads(gcp_service_acc)
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

    raise RuntimeError(
        f"Unsupported ENVIRONMENT value: {env}. Use DEVELOPMENT, PRODUCTION, or CLOUD_SQL."
    )
