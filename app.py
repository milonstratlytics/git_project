from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server
import time
from resume_scoring import predict_resume_scoring
app = Flask(__name__)
import os
import shutil

def cv_parser():
    
    
    put_code("-----<< Welcome to CV Parser Application >>-----")
    count=0
    add_more = True
    
    while add_more: 
        
        info = input_group("Enter Details : ",[
          input("Enter Job Title you are looking for :", name='job_title'),
          input("Enter Skillset you are looking for :", name='skill'),
          input("Enter Education you are looking for :", name='education'),
          
          input("Enter years of experience you are looking for :", name='experience',type=FLOAT)
        ])
        print(info['job_title'], info['skill'],info['education'],info['experience'])
        job_title=info['job_title']
        skill=info['skill']
        education = info['education']
        experience = info['experience']
        
            
        put_text('You have searched fors Job Tile : ',job_title)
        put_text('Selected Skillset :' ,skill)
        put_text('Required Degree :' ,education)
        put_text('Required experience :' ,experience)
        put_text('------------------------------------------------')
        #put_text(df)
        with put_loading():
            put_code("Plz Wait..We are working on magic !! Fetching top CVs for you..")
            time.sleep(3)  # Some time-consuming operations
        put_text("Matched Results : ")
        
        
        selected_resume = predict_resume_scoring(job_title,skill,education,experience)
        put_table([
                    {"Job_Title":job_title,"SkillSet":skill,"TopCVFound":selected_resume}
                ], header=["Job_Title", "SkillSet","TopCVFound"]) 

        put_code("**Note: All the matched CVs are stored in 04_Matched_CVs_pdf folder")   
        
        add_more = actions(label="Would you like to search more ?", 
                        buttons=[{'label': 'Yes', 'value': True}, 
                                 {'label':'No', 'value': False}])
        
        count= count+1
        put_text("--------------------------")
        put_text(f"You have searched for {count} CVs | Search results shown above. ")
        
        put_text("--------------------------")
        #clear(scope=- 1) 
      
    put_code("----- Thank You for using the CV Parser Application -----")



app.add_url_rule('/cv_parser', 'webio_view', webio_view( cv_parser),
            methods=['GET', 'POST', 'OPTIONS'])



app.run(host='localhost', port=80)