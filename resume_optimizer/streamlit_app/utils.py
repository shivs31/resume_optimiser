import streamlit as st
import pandas as pd
import numpy as np
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from pprint import pprint
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from rake_nltk import Rake
from fuzzywuzzy import fuzz
import json
    

#to extract keywords from job description
def extract_keywords_from_job(job_post):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(job_post, 'html.parser')

    # Find the element containing the job description
    job_description_element = soup.find('div', {'id': 'JobDescriptionContainer'})

    # Extract the text from the job description element
    if job_description_element is not None:
        job_description = job_description_element.get_text()
    else:
        return ""  # Return an empty string if job description is not found
    
    # List of stop words in English
    stop_words = set(stopwords.words('english'))
        
    # List of stop words in English
    stop_words = set(stopwords.words('english'))

    #custom_stop_words = ["14535", "bmo mr", "tobias fleßner", "e.g.", "end"]

    # Add custom stop words if provided
    #if custom_stop_words is not None:
    #    stop_words.update(custom_stop_words)

    # Tokenize the text and remove stop words
    words = job_description.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Rejoin the words into a string without stop words
    filtered_description = ' '.join(filtered_words)
    
    modified_description = filtered_description.replace('e.g.', ' ').replace('end', ' ').replace('bmo mr', ' ').replace('tobias fleßner', ' ').replace('14535', ' ')

    r = Rake()
    r.extract_keywords_from_text(modified_description)
    keywords = r.get_ranked_phrases()

    # Extract individual keywords
    jd_keywords = set(keyword for keyword in keywords if len(keyword.split()) < 3)

    return jd_keywords

#to check if skills from bootcamp are in job description

def job_dskills(jd_keywords, skill_json):

    matched_skills = []
    unmatched_skills = []

    for key, value in skill_json.items():
        for skill in jd_keywords:
            match_ratio = fuzz.partial_ratio(skill, value)
            if match_ratio > 60:  # Adjust the threshold as needed
                matched_skills.append(skill)
            else:
                unmatched_skills.append(skill)

    return matched_skills, unmatched_skills

#to check if skills from projects are in job description
def job_projskills(project_dict, jd_keywords, threshold=90):
    matching_keywords = {}

    # Compare skills in each project to job description keywords
    for project_name, project_info in project_dict.items():
        skills = project_info['skills'].lower().split(', ')
        matches = set()
        for skill in skills:
            for keyword in jd_keywords:
                if fuzz.ratio(skill, keyword.lower()) >= threshold:
                    matches.add(keyword)
        matching_keywords[project_name] = matches

    return matching_keywords

#to choose skills and projects for job description
def choose_skills_from_projects(project_dict, jd_keywords):
    project_keywords_count = {}  # Track the number of keyword matches for each project

    # Iterate over each project and count the keyword matches
    for project, project_data in project_dict.items():
        project_skills = project_data['skills'].split(', ')
        count = sum(keyword.lower() in project_skills for keyword in jd_keywords)
        project_keywords_count[project] = count

    # Sort projects based on the number of keyword matches in descending order
    sorted_projects = sorted(project_keywords_count, key=project_keywords_count.get, reverse=True)

    selected_skills = set()
    selected_projects = []

    # Select up to 5 skills from the project with the maximum keyword matches
    for project in sorted_projects:
        if len(selected_skills) >3:
        #if selected_skills >=5:
            break

        project_skills = project_dict[project]['skills'].split(', ')
        skills_to_add = [keyword for keyword in jd_keywords if keyword.lower() in project_skills]

        for skill in skills_to_add:
            selected_skills.add(skill)
            selected_projects.append(project)

    return selected_skills, selected_projects[:4]