import streamlit as st

# Navigation setup with multiple pages on the top position

pg = st.navigation([st.Page("pages/dashboard.py", title="Dashboard"), 
                    st.Page("pages/about_project.py", title="About this Project"), 
                    st.Page("pages/about_me.py", title="About Me"), 
                    st.Page("https://public.tableau.com/views/TickersAnalysisDashboard/Dashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link", title="Tableau Version"),
                    st.Page("https://github.com/chenjinghao/ms_fabric_project", title="Microsoft Fabric & Power BI Version"), 
                    st.Page("https://youtu.be/HWq92IGbM04?si=xr0Wqnz_ILZ7tGdF", title="Video Demo (In case of breakdown)")],
                    position='top', expanded=True)

pg.run()
