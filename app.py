import numpy as np
import pandas as pd
# import streamlit as st 
from resume_scoring import predict_resume_scoring

# def main():
#     st.title("Welcome to Resume Scoring Process of Stratlytic")
#     html_temp = """
#     <div style="background-color:tomato;padding:10px">
#     <h2 style="color:white;text-align:center;">Resume Scoring App </h2>
#     <p style="color:white;text-align:center;">Please fill up following inputs </p>
#     </div>
#     """
#     st.markdown(html_temp,unsafe_allow_html=True)
#     job_title = st.text_input("Job Title","Enter job title you are looking for")
#     skill = st.text_input("Skills(comma-seperated)","Enter all required skills you are looking for")
#     education= st.selectbox("Education", ["Bachelor's Degree", "Master's Degree", "PhD"])
#     experience = st.slider("Experience (in years)", min_value=0, max_value=20, value=0)
#     result=""
#     if st.button("Predict"):
#         result=predict_resume_scoring(job_title,skill,education,experience)
#     st.success('The output is {}'.format(result))
#     if st.button("About"):
#         st.text("Lets LEarn")
#         st.text("Built with Streamlit")

# if __name__=='__main__':
#     main()


# from flask import Flask, render_template, request

# app = Flask(__name__)
# # app.config.from_object(__name__)

# @app.route('/')
# def welcome():
#     return render_template('form.html')

# @app.route('/', methods=['POST'])
# def result():
#     var_1 = request.form.get("var_1", type=int, default=0)
#     var_2 = request.form.get("var_2", type=int, default=0)
#     job_title = request.form.get("var_1")
#     skill = request.form.get("var_2")
#     education= request.form.get("education")
#     experience = int(request.form.get('experience'))   
#     result=predict_resume_scoring(job_title,skill,education,experience)
#     entry = result
#     return render_template('form.html', entry=entry)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
# from resume_scoring import predict_resume_scoring

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', output=''),render_template('form.html', output='')

@app.route('/predict', methods=['POST'])
def predict():
    job_title = request.form.get('job_title')
    skill = request.form.get('skill')
    education = request.form.get('education')
    experience = int(request.form.get('experience'))

    result=predict_resume_scoring(job_title,skill,education,experience)

    return render_template('index.html', output='The output is {}'.format(result))

if __name__ == '__main__':
    app.run()
