import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io
import numpy as np
import requests
import plotly.graph_objs as go

def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    return None
    
# Insert consent
def add_consent():
    st.session_state['consent'] = True

def click_submit():
    st.session_state['submit'] = True

def consent_form():
    st.markdown("""
    By submitting the form below you agree to your data being used for research purposes. 
    """)
    agree = st.button("I understand and consent.", on_click = add_consent)
    if agree:
        st.markdown("You can now start the survey! Please move to questions by clicking on the buttons in the sidebar on the left.")


def save_input_to_session_state(key, value):
    """Helper function to save input into session state."""
    st.session_state[key] = value

def initialize_session_state():
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
        st.session_state['continue'] = False

def get_profession_index(profession):
    if profession == 'Government Official/Donor':
        return 0
    elif profession == 'Program Implementer/Practitioner':
        return 1
    elif profession == 'Researcher':
        return 2
    else:
        return 0
    

def personal_information():
    st.subheader("Personal Data")
    col1, _ = st.columns(2)
    with col1:
        name = st.text_input("Please, enter your full name and surname:", value=st.session_state.get('user_full_name', ''))
        save_input_to_session_state('user_full_name', name)
        work = st.text_input("Please, enter your working title:", value=st.session_state.get('user_position', ''))
        save_input_to_session_state('user_position', work)
        profession = st.radio('Please, specify your professional category:', ('Government Official/Donor', 'Program Implementer/Practitioner', 'Researcher'), key = 'profession', index = get_profession_index(safe_var('professional_category')))
        save_input_to_session_state('professional_category', profession)
        experience = st.text_input('Please, insert the years of experience you have working on digitalization:', value=st.session_state.get('years_of_experience', ''))
        save_input_to_session_state('years_of_experience', experience)

def secrets_to_json():
    return {
        "folder_id": st.secrets["folder_id"],
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"],
        
    }

# EXAMPLE 

TITLE_INSTRUCTIONS = '''Instructions'''

SUBTITLE_INSTRUCTIONS = '''This example is designed to help you understand how to effectively respond to this survey. \\
For each question, you have a table with two columns. Please allocate probabilities based on the likelihood that you think a specific event will happen under the "Probability" column. The plot next to it will show the distribution of your answers. As an example, suppose we asked about your beliefs regarding tomorrow's maximum temperature in degrees Celsius in your city or town.'''

CAPTION_INSTRUCTIONS = '''In this case, your prediction indicates a 45\% chance of the maximum temperature reaching 26 degrees Celsius, 20\% chance of it reaching 26 degrees Celsius, and so on.'''


def introduction(header_config):
    st.title(header_config['survey_title'])
    st.write(header_config['survey_description'])

def instructions():

    st.subheader(TITLE_INSTRUCTIONS)
    st.write(SUBTITLE_INSTRUCTIONS)

    st.subheader("Temperature Forecast Tomorrow in Your City")
    st.write('_Please scroll on the table to see all available options._')

    #with data_container:
    table, plot = st.columns([0.4, 0.6], gap = "large")
    
    with table:
        # Create some example data as a Pandas DataFrame
        values_column = ['< 15'] + list(range(16, 25)) + ['> 25']
        zeros_column = [0 for _ in values_column]
        zeros_column[4:9] = [5, 15, 45, 20, 15]

        data = {'Temperature': values_column, 'Probability (%)': zeros_column}
        df = pd.DataFrame(data)

        df['Temperature'] = df['Temperature'].astype('str')
    
        st.data_editor(df, use_container_width=True, hide_index=True, disabled=('Temperature', "Probability (%)"))

    st.write(CAPTION_INSTRUCTIONS)

    with plot:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=values_column, 
            y=df['Probability (%)'], 
            marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
            marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
            marker_line_width=2,  # Width of the bar outline
            text=[f"{p}" for p in df['Probability (%)']],  # Adding percentage labels to bars
            textposition='auto',
            name='Probability (%)'
        ))

        fig.update_layout(
            title={
                'text': "Probability distribution",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Temperature",
            yaxis_title="Probability (%)",
            yaxis=dict(
                range=[0, 100], 
                gridcolor='rgba(255, 255, 255, 0.2)',  # Light grid on dark background
                showline=True,
                linewidth=2,
                linecolor='white',
                mirror=True
            ),
            xaxis=dict(
                tickangle=-45,
                showline=True,
                linewidth=2,
                linecolor='white',
                mirror=True
            ),
            font=dict(color='white'),  # White font color for readability
        )
        st.plotly_chart(fig)
    
def submit(): 
    st.session_state['submit'] = True

'''
answers_df = generate_df(
    answers1, answers2, answers3, answers4, answers4_1, 
    answers5, answers5_1, answers6, answers6_1, 
    answers7, answers8, answers9, answers10
)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
answers_df = generate_df(answers1, answers2, answers3, answers4, answers4_1, answers5, answers5_1, answers6, answers6_1, answers7, answers8, answers9, answers10)
st.sidebar.button("Submit", on_click=add_submission, args=(answers_df))
if st.session_state.get('submit'):
    st.success(f"Thank you for completing the Survey on {config['header']['survey_title']}!")
    

# Submission button + saving data
if ('percentage_difference1' in locals()) and ('percentage_difference2' in locals()) and ('percentage_difference3' in locals()) and ('percentage_difference4' in locals()) and ('percentage_difference5' in locals()) and ('percentage_difference6' in locals()) and ('percentage_difference7' in locals()) and ('percentage_difference8' in locals()) and ('percentage_difference9' in locals()) and ('percentage_difference10' in locals()):
    
    answers_df = generate_df(answers1, answers2, answers3, answers4, answers4_1, answers5, answers5_1, answers6, answers6_1, answers7, answers8, answers9, answers10)
    st.sidebar.button("Submit", on_click=add_submission, args=([answers_df, ]))


    if st.session_state.get('submit'):
        st.success(f"Thank you for completing the Survey on {config['header']['survey_title']}!")
    # TODO: Add download button
# st.write("You can now download your answers as csv file.")
# concatenated_csv = convert_df(concatenated_df)
'''