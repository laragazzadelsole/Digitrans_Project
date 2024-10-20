import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from requests_oauthlib import OAuth2Session
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from fixed_components import *
import plotly.graph_objs as go
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    return None

def effect_size_question(jsonfile_name, question_number):
        st.markdown(jsonfile_name['effect_size'])
        st.markdown("- In comparison to GROUP 1 that receives the Financial Subsidy only.")
        answer_1 = st.text_input("Please insert a number or write 'I don't know'.", key = jsonfile_name['num_input_question_1'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_1', ''))
        st.markdown("- In comparison to GROUP 3 that receives the Benchmarking Report.")
        answer_2 = st.text_input("Please insert a number or write 'I don't know'.", key = jsonfile_name['num_input_question_2'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_2', ''))
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_1', answer_1)
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_2', answer_2)


def get_rct1_index(RCT_Q1):
    if RCT_Q1 == 'More interested in using RCTs for evaluation of other government projects':
        return 0
    elif RCT_Q1 == 'Just as interested in using RCTs for evaluation of other government projects as I was before starting this one':
        return 1
    elif RCT_Q1 == 'Less interested in using RCTs for evaluation of other government projects':
        return 2
    else:
        return 0
    
def get_rct2_index(RCT_Q2):
    if RCT_Q2 == 'The RCT improved the design of the intervention relative to projects without an RCT':
        return 0
    elif RCT_Q2 == 'The RCT did not change the design':
        return 1
    elif RCT_Q2 == 'The RCT led the intervention to be designed less well than projects without an RCT':
        return 2
    else:
        return 0
    
def get_rct3_index(RCT_Q3):
    if RCT_Q3 == 'The RCT sped up implementation of the project':
        return 0
    elif RCT_Q3 == 'The RCT did not change the speed':
        return 1
    elif RCT_Q3 == 'The RCT slowed down the speed of implementation':
        return 2
    else:
        return 0

def get_rct4_index(RCT_Q4):
    if RCT_Q4 == 'I will trust estimates of the programs impacts from this RCT more than of other programs that use our standard M&E':
        return 0
    elif RCT_Q4 == "I will trust estimates of this program's impacts equally as much as other programs that use our standard M&E":
        return 1
    elif RCT_Q4 == "I will trust estimates of this program's impacts from the RCT less than those of other programs that use our standard M&E":
        return 2
    else:
        return 0

def RCT_questions():
    st.subheader('Questions on RCTs Evaluation')
    st.write('We would like to know your opinion regarding RCTs programs.')
    st.write('1. After my experience in being involved in this project, I am:')
    RCT_Q1 = st.radio('Choose one of the following options:', ['More interested in using RCTs for evaluation of other government projects', 'Just as interested in using RCTs for evaluation of other government projects as I was before starting this one', 'Less interested in using RCTs for evaluation of other government projects'], index = get_rct1_index(safe_var('RCT_Q1')))
    save_input_to_session_state('RCT_Q1', RCT_Q1)
    
    st.write('2. We would like you to compare your experiences on this project that we are evaluating through an experiment to similar government projects you have worked on that have not had such an evaluation. Can you please compare this project to similar projects without an experimental evaluation in terms of:')
    st.write('- Design of the intervention')
    RCT_Q2 = st.radio('Choose one of the following options:', ['The RCT improved the design of the intervention relative to projects without an RCT', 'The RCT did not change the design', 'The RCT led the intervention to be designed less well than projects without an RCT'], index = get_rct2_index(safe_var('RCT_Q2')))
    save_input_to_session_state('RCT_Q2', RCT_Q2)

    st.write('- Speed of Implementation')
    RCT_Q3 = st.radio('Choose one of the following options:', ['The RCT sped up implementation of the project', 'The RCT did not change the speed', 'The RCT slowed down the speed of implementation'],  index = get_rct3_index(safe_var('RCT_Q3')))
    save_input_to_session_state('RCT_Q3', RCT_Q3)

    st.write('- Trustiworthiness of program impacts')
    RCT_Q4 = st.radio('Choose one of the following options:', ['I will trust estimates of the programs impacts from this RCT more than of other programs that use our standard M&E', "I will trust estimates of this program's impacts equally as much as other programs that use our standard M&E", "I will trust estimates of this program's impacts from the RCT less than those of other programs that use our standard M&E"],  index = get_rct4_index(safe_var('RCT_Q4')))
    save_input_to_session_state('RCT_Q4', RCT_Q4)

    st.write('- Do you think that thanks to the RCT you reached new beneficiaries? Do you think that it helped you disburse more funds than you originally planned?')
    input_RCT_Q5 = st.text_input('Please, write about your experience (max 500 characters).', max_chars=500, key = 'RCT_question5', value=st.session_state.get('input_RCT_Q5', ''))
    save_input_to_session_state('input_RCT_Q5', input_RCT_Q5)

    st.write('- Do you think allocating grants randomly amongst equally eligible potential beneficiaries is ethical? Did you think so before engaging in the RCT?')
    input_RCT_Q6 = st.text_input('Please, write about your experience (max 500 characters).', max_chars=500, value=st.session_state.get('input_RCT_Q6', ''))
    save_input_to_session_state('input_RCT_Q6', input_RCT_Q6)


def add_submission(df):
      
    st.session_state['submit'] = True
    
    #save data to google sheet
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    client = gspread.authorize(creds)
 
    sheet = client.open("Digitrans_Prior_Survey_Answers").sheet1

    column_names_list = df.columns.tolist()
    #column_names = sheet.append_row(column_names_list)

    sheet_row_update = sheet.append_rows(df.values.tolist()) #.values.tolist())
    
    #Navigate to the folder in Google Drive. Copy the Folder ID found in the URL. This is everything that comes after “folder/” in the URL.
    backup_sheet = client.create(f'Backup_{df.iloc[0, 0]}_{datetime.now()}', folder_id= secrets_to_json()['folder_id']).sheet1
    backup_sheet = backup_sheet.append_rows(df.values.tolist()) #(new_bins_df.iloc[:2].values.tolist())
    #backup_sheet.share('', perm_type = 'user', role = 'writer')

