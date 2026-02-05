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