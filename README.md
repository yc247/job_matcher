# 💻 Job Matcher Project

Job Matcher is an NLP-based tool designed to streamline the job search process by analyzing resumes or job descriptions and recommending similar roles from a curated set of past job postings. 

This project aims to help users quickly identify opportunities that align with their skills and experience, reducing the time spent on mismatched applications.

## 💡 Inspiration

Job hunting can be exhausting, especially when it involves sifting through countless listings and submitting endless applications. The idea for this project came from my own experience applying for data science roles, where I noticed that identical job titles often entail very different responsibilities depending on the company or industry. This makes it challenging and time-consuming to find positions that truly align with one’s skills and interests. Job Matcher is my attempt to make this process easier by providing a tool that streamlines job searching process.

## 🌏 Features Built
- **Resume Parsing**: Built a resume parser to extract professional experience from uploaded resumes, such as skills, experience, and qualifications, allowing the system to match job recommendations more accurately.
- **Text Data Preprocessing**: Implemented a thorough text cleaning pipeline, including normalization, tokenization, and removal of unnecessary characters, to ensure consistent and high-quality input data for analysis.
- **Fine-Tuning TLNK Model**: Adapted the TLNK (Transformer-based model for Named Knowledge) for this specific application by fine-tuning it on relevant job description data, enhancing its ability to identify and recommend the most similar jobs based on user input.
- **Interactive Streamlit App**: Created a Streamlit app for users to upload resumes or job descriptions and receive job recommendations.

## 💾 Data Used 
[LinkedIn Job Postings (2023 - 2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings/data?select=companies)

