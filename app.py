import re
import nltk
import os
from io import StringIO
import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import numpy as np
import os
import shutil
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server
import time

app = Flask(__name__)


def predict_resume_scoring(job_title,skill,education,experience):
    
    database = pd.read_csv('full_database.csv')
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
    #selected_resume.to_csv("03_Selected_CVs_File\selected_resume.csv")
    #database.to_csv("03_Selected_CVs_File\resulted_resume.csv")
    #origin = r'01_Raw_CVs/'
    #target = r'04_Matched_CVs_pdf/'

    #files = selected_resume['Matched_CV'].to_list()
    
    #for file in files:
       # shutil.copy(origin + file ,target + file)

    #print(selected_resume)
   
    return selected_resume


def cv_parser():
    
    
    put_info("-----<< Welcome to CV Parser Application >>-----")
    count=0
    add_more = True
    
    while add_more: 
        put_text("** Note: This is a demo application works only for Job Titles related to Data Science **")
        info = input_group("Enter Details : ",[
          input("Enter Job Title :", name='job_title'),
          input("Enter Skillset :", name='skill'),
          input("Enter Education :", name='education'),
          input("Enter years of experience :", name='experience',type=FLOAT)
        ])
        print(info['job_title'], info['skill'],info['education'],info['experience'])
        job_title=info['job_title']
        skill=info['skill']
        education = info['education']
        experience = info['experience']
        
            
        put_text('You have searched for Job Tile : ',job_title)
        put_text('Selected Skillset :' ,skill)
        put_text('Required Degree :' ,education)
        put_text('Required experience :' ,experience)
        put_text('------------------------------------------------')
        #put_text(df)
        with put_loading():
            put_code("Plz Wait.. While we work our charm !! Fetching top CVs for you..")
            time.sleep(3)  # Some time-consuming operations
        put_text("Matched Results : ")
        
        
        selected_resume = predict_resume_scoring(job_title,skill,education,experience)
        put_table([
                    {"Job_Title":job_title,"SkillSet":skill,"TopCVFound":selected_resume}
                ], header=["Job_Title", "SkillSet","TopCVFound"]) 

        #put_code("**Note: All the matched CVs are stored in 04_Matched_CVs_pdf folder")   
        
        add_more = actions(label="Would you like to search more ?", 
                        buttons=[{'label': 'Yes', 'value': True}, 
                                 {'label':'No', 'value': False}])
        
        count= count+1
        put_text("--------------------------")
        put_text(f"You have searched for {count} CVs | Search history shown above. ")
        
        put_text("--------------------------")
        #clear(scope=- 1) 
      
    put_code("----- Thank You for using the CV Parser Application -----")



app.add_url_rule('/cv_parser_v1', 'webio_view', webio_view( cv_parser),
            methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    app.run(debug=True)
