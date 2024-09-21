import pandas as pd
import streamlit as st
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


method_list = ["Sentence Transformers (SBERT)",
               "TF-IDF"]

work_type_list = ["FULL_TIME",
                  "CONTRACT",
                  "PART_TIME",
                  "TEMPORARY",
                  "INTERNSHIP",
                  "OTHER",
                  "VOLUNTEER"]

industry_name_list = ['Real Estate', 'Law Practice', 'Hospitality',
       'Food and Beverage Services', 'Hospitals and Health Care',
       'Non-profit Organizations', 'Civil Engineering',
       'Staffing and Recruiting', 'Medical Practices',
       'Wellness and Fitness Services', 'IT Services and IT Consulting',
       'Construction', 'Advertising Services',
       'Technology, Information and Internet',
       'Medical Equipment Manufacturing', 'Higher Education', 'Banking',
       'Telecommunications', 'Software Development',
       'Chemical Manufacturing', 'Financial Services', 'Insurance',
       'Business Consulting and Services',
       'Food and Beverage Manufacturing', 'Manufacturing',
       'Pharmaceutical Manufacturing', 'Biotechnology Research',
       'Retail Apparel and Fashion', 'Government Administration',
       'Retail', 'Appliances, Electrical, and Electronics Manufacturing',
       'Motor Vehicle Manufacturing', 'Oil and Gas',
       'Aviation and Aerospace Component Manufacturing',
       'Industrial Machinery Manufacturing',
       'Transportation, Logistics, Supply Chain and Storage',
       'Environmental Services', 'Utilities', 'Accounting',
       'Defense and Space Manufacturing',
       'Technology, Information and Media', 'Information Services']

experience_keywords =["work experience",
                      "professional experience",
                      "experience",
                      "employment history",
                      "career experience",
                      "relevant experience",
                      "work history",
                      "job experience",
                      "research experience",
                      "project experience", 
                      "projects",
                      "reseach",
                      "publications",
                      "skills",
                      "certifications",
                      "knowledge",
                      "credentials",
                      "technical skills",
                      "proficiencies",
                      "programming languages",
                      "competencies"]


@st.cache_data
def get_jobs(job_posts, work_type, industry_name, job_number, method, query):
    job_posts = job_posts[job_posts['work_type'] == work_type]
    job_posts = job_posts[job_posts['industry_name'] == industry_name]

    if method == "Sentence Transformers (SBERT)":
        results = sbert_search(job_posts, query)

    elif method == "TF-IDF":
        results = tfidf_search(job_posts, query)

    return results.head(job_number)[['title', 'company_name', 'job_posting_url']]

def sbert_search(job_posts, query):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embd = model.encode(query)
    
    # calculate consine similarity between query sentence and job posts
    for index, row in job_posts.iterrows():
        jd_embd = model.encode(row['title_description'])
        
        # reshape the embeddings to 2D arrays 
        query_embd = query_embd.reshape(1, -1)
        jd_embd = jd_embd.reshape(1, -1)
        cosine_similarities = cosine_similarity(query_embd, jd_embd)
        job_posts.loc[index, 'similarity_score'] = cosine_similarities.flatten()[0]

    # Sort job posts by similarity scores
    job_posts_sorted = job_posts.sort_values(by='similarity_score', ascending=False)

    return job_posts_sorted 

def tfidf_search(job_posts, query):
    # Initialize TfidfVectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(list(job_posts['title_description']))
    query_vector = vectorizer.transform([query])
    
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    job_posts['similarity_score'] = cosine_similarities

    job_posts_sorted = job_posts.sort_values(by='similarity_score', ascending=False)

    return job_posts_sorted

def get_experience(resume_lines):
    headers = []
    indices = []
    experience = []
    for i, line in enumerate(resume_lines):
        if line[0].islower():
            continue

        line_lower = line.lower()
        for keyword in experience_keywords:
            if line_lower.startswith(keyword):
                headers.append(keyword)
                indices.append(i)
    
    section_num = len(headers)
    for i in range(section_num - 1):
        start_index = indices[i]
        end_index = indices[i+1] - 1
        experience.append(" ".join(resume_lines[start_index:end_index]))
    
    start_index = indices[section_num-1]
    experience.append(" ".join(resume_lines[start_index:]))

    experience = " ".join(experience)
    return experience

def read_pdf(pdf_file):
    pdf = pdfplumber.open(pdf_file)
    full_string= ""
    for page in pdf.pages:
        full_string += page.extract_text() + "\n"
    pdf.close()

    full_string = re.sub(r"\n+", "\n", full_string)
    full_string = full_string.replace("\r", "\n")
    full_string = full_string.replace("\t", " ")

    # Remove LaTeX characters
    full_string = re.sub(r"\uf0b7", " ", full_string)
    full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
    full_string = re.sub(r"• ", " ", full_string)

    # Split text by \n and remove \n
    resume_lines = full_string.splitlines(True)
    resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
    
    experience = get_experience(resume_lines)

    return experience
