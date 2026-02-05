import streamlit as st
from connection.database import get_engine
import sqlalchemy

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

st.title("PostgreSQL + VPC Data")

engine = get_engine()

query = "SELECT * FROM mart_price_news__analysis LIMIT 10"
try:
    with engine.connect() as conn:
        df = conn.execute(sqlalchemy.text(query)).fetchall()
        st.write(df)
except Exception as e:
    st.error(e)
    st.stop()