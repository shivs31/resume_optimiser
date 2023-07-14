
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
import string

st.markdown(
    """
<style>
    /* Increase font size for just for the main container by factor 1.1 */
    section.main div.block-container {
        font-size: 1.5em;
    }

</style>
""",
    unsafe_allow_html=True,
)

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
            "Resume Optimizer",
            "Job description",
            "Suggestions for your resume",
            #"Your project skills matched with job description",
            #"Suggestions for your resume"
            ]
        ) 

if page == "Resume Optimizer":
    # slogan
    st.subheader("Welcome to the Resume Optimizer")
    # blank space
    st.write("")
    # image
    st.subheader("Let's get started!")
    st.image('friends.jpeg', width=600)


elif page == "Job description":
    # title
    st.header("Upload your job description")
    jobdesc = st.file_uploader("Choose your job description", type=['html'])
    #skills = st.file_uploader("Choose your file", type=['json'])

    if jobdesc is not None:
        html = jobdesc.read()
        st.write("filename:", jobdesc.name)
        filter_keywords = extract_keywords_from_job(html)
        keywords = [string.capwords(keyword) for keyword in filter_keywords]
        keywords_print = ", ".join(keywords)
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
        styled_text = f"{css_styles}<div class='black-text'>{keywords_print}</div>"

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
elif page == "Suggestions for your resume":
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
        
        #st.success("Your skills loaded successfully.")

    if not Path("./data/project_dict.json").is_file():
        st.warning("Please upload your skills first.")
    
    else:
        with open("./data/project_dict.json", "r") as file:
            projects = json.load(file)
        
        st.success("Your skills and projects loaded successfully.")

        col1, col2, col3 = st.columns(3)

        #skills = st.file_uploader("Choose your skills file", type=['json'])
        if skills is not None:
            #skills_data = json.load(skills)
            # #st.write(skills)

            matched_skills, unmatched_skills = job_dskills(jd_keywords_data, skills)
            with col1:
                st.write("")
                #show_button = st.button(label="Matched skills") 
                #if show_button:
                with st.expander("Matched Skills"):
                    #st.subheader("Matched Skills:")
                    for skill in matched_skills:
                        st.markdown(f"""<span style="font-size: 1.5em;">{string.capwords(skill)}</span>""", unsafe_allow_html=True)
                        #st.write(md_skills)
                #else:
                #    st.subheader("Unmatched Skills:")
                #    for skill in unmatched_skills:
                #        st.write(skill)
                #    st.write(unmatched_skills)
            
        if projects is not None:
            selected_skills, selected_projects = choose_skills_from_projects(projects, list(jd_keywords_data))

            with col2:
                st.write("")
                #show_button = st.button(label="Projects Suggestions")
                #if show_button:
                with st.expander("Suggested Projects"):
                    #st.header("\nSuggested Projects:")
                    for project in selected_projects:
                        #st.write(string.capwords(project))
                        st.markdown(f"""<span style="font-size: 1.5em;">{string.capwords(project)}</span>""", unsafe_allow_html=True)
                        #st.write(prj_skill)

            #with col3:
            #    st.write("")
                #show_button = st.button(label="Skills Suggestions")
                #if show_button: 
            #    with st.expander("Suggested Skills"):
                    #st.header("Suggested Skills:")
            #        for skill in selected_skills:
                        # Use the <h1> tag to increase the font size
                        #st.write(f"<h1>{string.capwords(skill)}</h1>", unsafe_allow_html=True)
                        # Increase font size using CSS styling
                        #st.write('<style>div.stButton > button {font-size: 24px !important;}</style>', unsafe_allow_html=True)
                        #st.write(string.capwords(skill))
            #            st.markdown(f"""<span style="font-size: 1.5em;">{string.capwords(skill)}</span>""", unsafe_allow_html=True)
                        
                        

#elif page == "Your project skills matched with job description":
    # title
#    st.header("Import your projects")

    # Check if file exists
#    if not Path("./data/jd_keywords.json").is_file():
#        st.warning("Please upload your job description first.")
    
#    else:
#        with open("./data/jd_keywords.json", "r") as file:
#            jd_keywords_data = json.load(file)
        
#        st.success("Job Description keywords loaded successfully.")
        
    
#        projects = st.file_uploader("Choose your file", type=['json'])
#        if projects is not None:
#            project_data = json.load(projects)
            #st.write(skills_data)

#            proj_jd_key = job_projskills(project_data, jd_keywords_data)
#            st.subheader("Matched Skills:")
#            for project, matches in proj_jd_key.items():
#                st.write(f"Project: {project}")
#                st.write(f"Matching Keywords: {matches}")

#elif page == "Suggestions for your resume":

    # title
    #st.header("Import your resume")

    # Check if file exists
#    if not Path("./data/jd_keywords.json").is_file():
#        st.warning("Please upload your job description first.")
    
#    else:
#        with open("./data/jd_keywords.json", "r") as file:
#            jd_keywords_data = json.load(file)
        
#        st.success("Job Description keywords loaded successfully.")
        
    
#        projects = st.file_uploader("Choose your project file", type=['json'])
#        if projects is not None:
#            project_data = json.load(projects)
#            selected_skills, selected_projects = choose_skills_from_projects(project_data, list(jd_keywords_data))

#            st.header("Suggested Skills:")
#            for skill in selected_skills:
#                st.write(skill)
            

#            st.header("\nSuggested Projects:")
#            for project in selected_projects:
#                st.write(project)

        #to save the suggested skills and projects
#            if st.button("save suggestions"):
#                with open("./data/suggested_projects.json", "w") as file:
#                    json.dump(selected_projects, file)
#                    st.success("Suggested skills and projects saved successfully.")



