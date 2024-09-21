import streamlit as st
import pandas as pd


from utils import method_list, work_type_list, industry_name_list, get_jobs, read_pdf

# sidebar
st.sidebar.title("Job Recommendation 📝")
st.sidebar.caption("Find Jobs Belong to You.")
st.sidebar.markdown("Made by [Yucheng Fang](https://www.linkedin.com/in/yucheng-fang-49374b170)")


st.sidebar.markdown("---")

st.sidebar.header("Settings")
work_type = st.sidebar.selectbox("Work Type", work_type_list)
industry_name = st.sidebar.selectbox("Industry", industry_name_list)
job_number = int(st.sidebar.number_input("Job Number", min_value=1, max_value=30, value=5, step=1, help="Number of jobs returned."))
method = st.sidebar.selectbox("Method", method_list, help="Method to use for finding relevant jobs")
click = st.sidebar.button("Recommend Jobs")


# main page
job_posts = pd.read_csv("./postings_df.csv")

st.title("Job Recommendation")
st.text("simple explaination of the project")
resume_tab, job_description_tab = st.tabs(["Find Jobs by Resume", "Find Jobs by Resume Job Post"])
with resume_tab:
    file = st.file_uploader("Upload a Resume", key="file_uploader")
    if file is not None:
        try:
            # parse resume file here
            query = read_pdf(file)
        except:
            st.error("Please try upload a PDF file.")

with job_description_tab:
    st.text("Copy paste a job description and find similar jobs")
    query = st.text_input("Enter job description here...")

if click:
    st.session_state["jobs_df"] = get_jobs(job_posts, work_type, industry_name, job_number, method, query)
    jobs_df = st.session_state["jobs_df"]
    st.dataframe(jobs_df,
                 column_config={
                     "title": "Job Title",
                     "company_name": "Company",
                     "job_posting_url": st.column_config.NumberColumn(
                         "Job Post URL",
                         help="Link to the original job post")
                     }
                 )
else:
    st.info("👈  Click on 'Recommend Jobs' to show the jobs.")

