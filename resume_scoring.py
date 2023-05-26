import re
import nltk
#from nltk.corpus import stopwords
#stop = stopwords.words('english')
#from nltk.corpus import wordnet
import os
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import numpy as np
import os
import shutil


def predict_resume_scoring(job_title,skill,education,experience):
    
    database = pd.read_csv(r'02_Database\full_database.csv')
    job_title = job_title.lower()
    skill = skill.lower()
    education = education.lower()
    experience = float(experience)
    database = database.set_index('file_name')
    database = database[database['Job Role']== job_title]
    limit = len(database)
    
    education_match = process.extract(str(education),database['Qualification'], limit= limit  , scorer=fuzz.token_set_ratio)
    edu_result_df = pd.DataFrame()
    for i in range(limit):

        education_score = education_match[i][1]
        file = education_match[i][2]
        match_df = pd.DataFrame([[file,education_score]],columns = ['file_name','education_score'])
        edu_result_df = pd.concat([edu_result_df,match_df])
    
    skill_match = process.extract(str(skill),database['professional_skill'], limit= limit  , scorer=fuzz.token_set_ratio)
    skill_result_df = pd.DataFrame()
    for i in range(limit):
        skill_score = skill_match[i][1]
        file = skill_match[i][2]
        match_df = pd.DataFrame([[file,skill_score]],columns = ['file_name','skill_score'])
        skill_result_df = pd.concat([skill_result_df,match_df])

    
    database = database.reset_index()
    database = pd.merge(database,edu_result_df,how = 'left',on = 'file_name')
    database = pd.merge(database,skill_result_df,how = 'left',on = 'file_name')
    

    database['Work Experience'] = database['Work Experience'].astype('float')
    database['experience_score']=np.where(database['Work Experience']>=experience,100,np.where(np.logical_and(database['Work Experience']>=experience-1,database['Work Experience']<experience),50,0))
    
    database['Total_Score'] = (database['education_score'] + database['skill_score'] + database['experience_score'])/3
    database['Total_Score'] = np.round(database['Total_Score'])
    
    selected_resume = database[database['Total_Score']>= 60]
    selected_resume = selected_resume[['file_name','Total_Score']]
    selected_resume.columns = ['Matched_CV','Score']
    selected_resume = selected_resume.sort_values(by = ['Score'],ascending=False)
    selected_resume = selected_resume.reset_index(drop=True)
    selected_resume.index =  selected_resume.index + 1 
    selected_resume.to_csv("03_Selected_CVs_File\selected_resume.csv")
    #database.to_csv("03_Selected_CVs_File\resulted_resume.csv")
    origin = r'01_Raw_CVs/'
    target = r'04_Matched_CVs_pdf/'

    files = selected_resume['Matched_CV'].to_list()
    
    for file in files:
        shutil.copy(origin + file ,target + file)

    print(selected_resume)
   
    return selected_resume