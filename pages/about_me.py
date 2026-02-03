import streamlit as st

# Constant values

LINKEDIN_URL = "hhttps://www.linkedin.com/in/adam-cjh/"
PERSONAL_WEBSITE_URL = "https://adamchenjinghao.notion.site/beyond"


# Page content
st.title("JINGHAO CHEN")
st.markdown("Data enthusiast | Problem Solver | Lifelong Learner")
left, right = st.columns([1,1])
with left:
    st.image(r"static\my_photo.jpg", width='stretch', caption="Promoting Homeless shelter app at Langara Applied Research Day 2025")
with right:
    st.subheader("About me", divider="gray")
    st.markdown(
        body="""
        Data Analyst combining 7+ years of international business and finance experience with a Post-Degree Diploma in Data Analytics. Adept at leveraging Python, machine learning, and AI to solve real-world problems, having developed a grant-funded web application and an award-winning energy optimization model. Offers a unique blend of technical expertise, project management, and strategic thinking to drive data-informed decisions.
        """,
        width='stretch',
        text_alignment='justify'
    )
    st.link_button(
        label=":page_facing_up: Download my Resume",
        type="primary",
        url=r"https://adamchenjinghao.notion.site/my-Resume-3b113ebf370a4ef1952ee5acd8ed0923",
        use_container_width=True,
    )

## Skills section
st.markdown(body="**Technical Skills**", width='stretch', text_alignment='left')
st.markdown(
    body="""
![Skills](https://skills.syvixor.com/api/icons?perline=15&i=docker,googlecloud,python,airflow,postgresql,dbt,dlthub,scikitlearn,powerbi,streamlit,github,notion)
    """,
    width='stretch',
    text_alignment='justify'
)

## Know about me section
st.subheader("Know more about me", divider="gray")

linkedin, website, contact_me = st.columns(3)
with linkedin:
    st.link_button(
        label=":globe_with_meridians: LinkedIn Profile",
        url=LINKEDIN_URL,
        use_container_width=True,
    )
with website:
    st.link_button(
        label=":man_technologist: Personal Website",
        url=PERSONAL_WEBSITE_URL,
        use_container_width=True,
    )
with contact_me:
    st.link_button(
        label=":email: Contact Me",
        url="mailto:adam_cjh@outlook.com",
        use_container_width=True,
    )


## Milestones section
st.subheader("Recent milestones")
st.markdown(
    body="""
    - The project: Real-Time Access to Essential Services for Communities received College and Community Social Innovation Fund grants from Natural Sciences and Engineering Research Council of Canada on 31 OCT 2025 [[Check here](https://nserc-crsng.canada.ca/en/funding-decisions/result/2267)]. 
    - Mentioned in [Langara College News](https://langara.ca/news-events/stories/meet-winners-applied-research-day) for developing a web application to help homeless individuals find essential services in real-time.
    - Received the award for Student-involved project that highlights innovation/innovative practices at Langara Applied Research Day 2025 [[Project details here](https://ai4hvac.notion.site/)].
    - Presented our project with Roxanne Alvarez at the IEEE Canada CCECE 2024 event at Queen’s University [Check the post](https://www.linkedin.com/posts/adam-cjh_ccece2024-activity-7228522973136138240-u7bd?utm_source=share&utm_medium=member_desktop&rcm=ACoAADtikWYBakf2A5nkYwXEa9fj4-17kbdDzVI)!""",
    width='stretch',
    text_alignment='justify'
)