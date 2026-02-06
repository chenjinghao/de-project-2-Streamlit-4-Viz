import streamlit as st

# Navigation setup with multiple pages on the top position
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

