import streamlit as st

# Constant values
LINKEDIN_URL = "https://www.linkedin.com/in/adam-cjh/"
PERSONAL_WEBSITE_URL = "https://adamchenjinghao.notion.site/my-Portfolio-52dd63a53c104c568898f130767f23b4"
GITHUB_URL_PROJECT_ELT = "https://github.com/chenjinghao/de-project-1-airflow-dbt-4-ELT.git"
GITHUB_URL_PROJECT_VIZ = "https://github.com/chenjinghao/de-project-2-Streamlit-4-Viz.git"

# Configure the default settings of the page.
st.set_page_config(
    page_title="JINGHAO's Data Engineering Project",
    page_icon=":material/code_blocks:",
)

# Page content
st.title("About Projects")

st.markdown(
    body="""
![Skills](https://skills.syvixor.com/api/icons?perline=15&i=docker,googlecloud,python,airflow,postgresql,dbt,streamlit,github)
    """,
    width='stretch',
    text_alignment='justify'
)

st.markdown("""
<div style="font-family: sans-serif; line-height: 1.6;">
  <p>This capstone project showcases my evolution as a Data Engineer, synthesizing the full spectrum of skills I have acquired into a cohesive, production-ready solution.</p>
  
  <p>I divided the architecture into two core components:</p>
  <ul>
    <li><strong>Backend ELT Process:</strong> Handles data ingestion and transformation.</li>
    <li><strong>Frontend Visualization Suite:</strong> Derives meaning from the numbers.</li>
  </ul>

  <p>This dual-focus approach highlights not only my technical capability to handle complex workflows but also my understanding of how data engineering directly supports business intelligence and decision-making.</p>
</div>
""", unsafe_allow_html=True)

## Project Repositories section
col_viz, col_elt = st.columns([1,1])
with col_viz:
    st.link_button(
    label="Visit the Repository for Visualization Project",
    url=GITHUB_URL_PROJECT_VIZ,
    type="primary",
    width='content',
    use_container_width=True,
    )
with col_elt:
    st.link_button(
    label="Visit the Repository for ETL Project",
    url=GITHUB_URL_PROJECT_ELT,
    type="primary",
    width='content',
    use_container_width=True,
    )
##Project Architecture Diagram
st.image(image="static/img_project-de-workflow.png", caption="Project Architecture Diagram")


## Know about me section
st.subheader("To view my other projects", divider="gray")

st.link_button(
    label=":man_technologist: Visit my Personal Website",
    url=PERSONAL_WEBSITE_URL,
    use_container_width=True,
)
