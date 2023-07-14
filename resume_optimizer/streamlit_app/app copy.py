
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
#from pprint import pprint
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from rake_nltk import Rake
from fuzzywuzzy import fuzz
import json
from utils import  extract_keywords_from_job, job_dskills, job_projskills, choose_skills_from_projects
from pathlib import Path

# sidebar
with st.sidebar:
    # title
    st.title("Optimize your resume")
    # image
    st.image('info.jpeg')
    # blank space
    st.write("")
    # selectbox
    page = st.selectbox(
        "what would you like?",
        [
            "Welcome to the Resume Optimizer",
            "Job description",
            "Your skills matched with job description",
            "Your project skills matched with job description",
            "Suggestions for your resume"
            ]
        ) 

if page == "Welcome to the Resume Optimizer":
    # slogan
    st.header("Data will talk if you’re willing to listen to it    — Jim Bergeson")
    # blank space
    st.write("")
    # image
    st.image('data_talks.jpeg')


elif page == "Job description":
    # title
    st.header("Import your job description")
    jobdesc = st.file_uploader("Choose your job description", type=['html'])
    #skills = st.file_uploader("Choose your file", type=['json'])

    if jobdesc is not None:
        html = jobdesc.read()
        st.write("filename:", jobdesc.name)
        filter_keywords = extract_keywords_from_job(html)
        #st.write("")
        st.image('jobdescription.png')
        filtered_description = list(extract_keywords_from_job(html))
        #filtered_description = extract_keywords_from_job(html)
        st.subheader("Keywords from job description:")
            # Add CSS styles to change text color to black and increase font size
        css_styles = """
        <style>
        .black-text {
            color: black;
            font-size: 20px;
        }
        </style>
        """
            # Combine CSS styles and keyword_string using Markdown
        styled_text = f"{css_styles}<div class='black-text'>{filter_keywords}</div>"

        # Render the styled text in Streamlit
        st.markdown(styled_text, unsafe_allow_html=True)
        #st.write(filter_keywords)
            # blank space
        st.write(" ")
        if st.button("save keywords"):
            with open("./data/jd_keywords.json", "w") as file:
                json.dump(filtered_description, file)
            st.success("Job Description keywords saved successfully.")
    else:
        st.write("Please upload your job description")

#To check your skills matched with job description
elif page == "Your skills matched with job description":
    # title
    st.header("Check how many skills matched with job description")
    # image
    st.image('bootcampskills.jpg')
    # blank space
    st.write("")

    # Check if file exists
    if not Path("./data/jd_keywords.json").is_file():
        st.warning("Please upload your job description first.")
    
    else:
        with open("./data/jd_keywords.json", "r") as file:
            jd_keywords_data = json.load(file)
        
        st.success("Job Description keywords loaded successfully.")
        
    if not Path("./data/skill_json.json").is_file():
        st.warning("Please upload your skills first.")
    
    else:
        with open("./data/skill_json.json", "r") as file:
            skills = json.load(file)
        
        st.success("Your skills loaded successfully.")


        #skills = st.file_uploader("Choose your skills file", type=['json'])
        if skills is not None:
            #skills_data = json.load(skills)
            # #st.write(skills)

            matched_skills, unmatched_skills = job_dskills(jd_keywords_data, skills)
            show_button = st.button(label="Matched skills") 
            if show_button:
                st.subheader("Matched Skills:")
                for skill in matched_skills:
                    st.write(skill)
            #else:
                #st.subheader("Unmatched Skills:")
                #for skill in unmatched_skills:
                #    st.write(skill)
                #st.write(unmatched_skills)

elif page == "Your project skills matched with job description":
    # title
    st.header("Import your projects")

    # Check if file exists
    if not Path("./data/jd_keywords.json").is_file():
        st.warning("Please upload your job description first.")
    
    else:
        with open("./data/jd_keywords.json", "r") as file:
            jd_keywords_data = json.load(file)
        
        st.success("Job Description keywords loaded successfully.")
        
    
        projects = st.file_uploader("Choose your file", type=['json'])
        if projects is not None:
            project_data = json.load(projects)
            #st.write(skills_data)

            proj_jd_key = job_projskills(project_data, jd_keywords_data)
            st.subheader("Matched Skills:")
            for project, matches in proj_jd_key.items():
                st.write(f"Project: {project}")
                st.write(f"Matching Keywords: {matches}")

elif page == "Suggestions for your resume":

    # title
    #st.header("Import your resume")

    # Check if file exists
    if not Path("./data/jd_keywords.json").is_file():
        st.warning("Please upload your job description first.")
    
    else:
        with open("./data/jd_keywords.json", "r") as file:
            jd_keywords_data = json.load(file)
        
        st.success("Job Description keywords loaded successfully.")
        
    
        projects = st.file_uploader("Choose your project file", type=['json'])
        if projects is not None:
            project_data = json.load(projects)
            selected_skills, selected_projects = choose_skills_from_projects(project_data, list(jd_keywords_data))

            st.header("Suggested Skills:")
            for skill in selected_skills:
                st.write(skill)
            

            st.header("\nSuggested Projects:")
            for project in selected_projects:
                st.write(project)

        #to save the suggested skills and projects
            if st.button("save suggestions"):
                with open("./data/suggested_projects.json", "w") as file:
                    json.dump(selected_projects, file)
                    st.success("Suggested skills and projects saved successfully.")



