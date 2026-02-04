import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Constant values

LINKEDIN_URL = "https://www.linkedin.com/in/adam-cjh/"
PERSONAL_WEBSITE_URL = "https://adamchenjinghao.notion.site/beyond"

# Counter to track button clicks
## connect and update with google sheet
URL = "https://docs.google.com/spreadsheets/d/1eVDB1T-Ded34ycwNqJX36YD5heNIDlrUVGco7zR-X4w/edit?usp=sharing"

def get_creds():
    creds_info = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    }
    return Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])


try:
    client = gspread.authorize(get_creds())
    sheet = client.open("high five counter").sheet1
    val = sheet.acell('A2').value
    current_count = int(val) if val else 0
except gspread.exceptions.SpreadsheetNotFound:
    st.error("Sheet not found! Make sure you shared it with the service account email.")
    st.stop()



# Page content
st.title("JINGHAO CHEN")   
st.markdown("Data enthusiast | Problem Solver | Lifelong Learner")
left, right = st.columns([1,1])
with left:
    st.image("static/my_photo.jpg", width='stretch', caption="Promoting Homeless shelter app at Langara Applied Research Day 2025")
with right:
    st.subheader("About me", divider="gray")
    st.markdown(
        body="""
        Data Analyst combining 7+ years of international business and finance experience with a Post-Degree Diploma in Data Analytics. Adept at leveraging Python, machine learning, and AI to solve real-world problems, having developed a grant-funded web application and an award-winning energy optimization model. Offers a unique blend of technical expertise, project management, and strategic thinking to drive data-informed decisions.
        """,
        width='stretch',
        text_alignment='justify'
    )
counter_left, counter_right = st.columns(2, vertical_alignment ='bottom')
with counter_left:
    if st.button(
        label=":raised_hand: High Five with me",
        type="primary",
        use_container_width=True,
    ):
        new_count = current_count + 1
        sheet.update_acell('A2', new_count)
        st.rerun()   
with counter_right:
    st.write("Total High Fivers", current_count)


## Skills section
st.markdown(body="**Technical Skills**", width='stretch', text_alignment='left')
st.markdown(
    body="""
![Skills](https://skills.syvixor.com/api/icons?perline=15&i=docker,googlecloud,python,airflow,postgresql,dbt,dlthub,scikitlearn,powerbi,streamlit,github,notion)
    """,
    width='stretch',
    text_alignment='justify'
)

## Milestones section
st.subheader("Recent milestones")
st.markdown(
    body="""
    - The project: Real-Time Access to Essential Services for Communities received College and Community Social Innovation Fund grants from Natural Sciences and Engineering Research Council of Canada on 31 OCT 2025 [[Check here](https://nserc-crsng.canada.ca/en/funding-decisions/result/2267 "Search title: Real-Time Access to Essential Services for Communities")]. 
    - Mentioned in [Langara College News](https://langara.ca/news-events/stories/meet-winners-applied-research-day "Meet the winners of the Applied Research Day") for developing a web application to help homeless individuals find essential services in real-time.
    - Received the award for Student-involved project that highlights innovation/innovative practices at Langara Applied Research Day 2025 [[Project details here](https://ai4hvac.notion.site/ "AI-Powered Energy Optimizations at Langara College")].
    - Presented our project with Roxanne Alvarez at the IEEE Canada CCECE 2024 event at Queen’s University [Check the post](https://www.linkedin.com/posts/adam-cjh_ccece2024-activity-7228522973136138240-u7bd?utm_source=share&utm_medium=member_desktop&rcm=ACoAADtikWYBakf2A5nkYwXEa9fj4-17kbdDzVI)!""",
    width='stretch',
    text_alignment='justify'
)

## Know about me section
st.subheader("Know more about me", divider="gray")

linkedin, website, resume = st.columns(3)
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

with resume:
    st.link_button(
    label=":page_facing_up: Download Resume",
    type="primary",
    url=r"https://adamchenjinghao.notion.site/my-Resume-3b113ebf370a4ef1952ee5acd8ed0923",
    use_container_width=True,
    )
# with contact_me:
#     st.link_button(
#         label=":email: Email Me",
#         url="mailto:adam_cjh@outlook.com",
#         use_container_width=True,
#     )