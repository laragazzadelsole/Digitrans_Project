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
        st.markdown("- W porównaniu z GRUPĄ 1, która otrzymuje jedynie Voucher Finansowy.")
        answer_1 = st.text_input("Proszę wpisać liczbę lub napisać 'Nie wiem'.", key = jsonfile_name['num_input_question_1'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_1', ''))
        st.markdown("- W porównaniu z GRUPĄ 3, która otrzymuje jedynie Raport Benchmarkingowy.")
        answer_2 = st.text_input("Proszę wpisać liczbę lub napisać 'Nie wiem'.", key = jsonfile_name['num_input_question_2'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_2', ''))
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_1', answer_1)
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_2', answer_2)


def get_rct1_index(RCT_Q1):
    if RCT_Q1 == 'Jestem bardziej zainteresowany/a wykorzystaniem RCT do ewaluacji innych instrumentów wsparcia':
        return 0
    elif RCT_Q1 == 'Moje zainteresowanie wykorzystaniem RCT do ewaluacji innych instrumentów wsparcia nie zmieniło się':
        return 1
    elif RCT_Q1 == 'Jestem mniej zainteresowany/a wykorzystaniem RCT do ewaluacji innych instrumentów wsparcia ':
        return 2
    else:
        return 0
    
def get_rct2_index(RCT_Q2):
    if RCT_Q2 == 'RCT wprowadzilo do instrumentu wsparcia korzystne zmiany w porównaniu z instrumentami wsparcia bez RCT':
        return 0
    elif RCT_Q2 == 'RCT nie zmieniło sposobu, w jaki jest zaprojektowany instrument wsparcia':
        return 1
    elif RCT_Q2 == 'RCT spowodowało, że interwencja została zaprojektowana gorzej niż instrumenty bez RCT':
        return 2
    else:
        return 0
    
def get_rct3_index(RCT_Q3):
    if RCT_Q3 == 'RCT przyspieszyło wdrażanie instrumentu':
        return 0
    elif RCT_Q3 == 'RCT nie zmieniło tempa wdrażania instrumentu':
        return 1
    elif RCT_Q3 == 'RCT spowolniło tempo wdrażania instrumentu':
        return 2
    else:
        return 0

def get_rct4_index(RCT_Q4):
    if RCT_Q4 == 'Będę bardziej ufać danym o wpływie instrumentu mierzonego przy pomocy metodologii RCT niż w przypadku ewaluacji innych instrumentów, które wykorzystują standardowe metodologie w monitorowanie i ewaluacji (M&E)':
        return 0
    elif RCT_Q4 == "Będę w takim samym stopniu ufać danym o wpływie instrumentu mierzonego przy pomocy metodologii RCT niż w przypadku ewaluacji innych instrumentów, które wykorzystują standardowe metodologie M&E":
        return 1
    elif RCT_Q4 == "Będę mniej ufać danym o wpływie instrumentu mierzonego przy pomocy metodologii RCT niż w przypadku ewaluacji innych instrumentów, które wykorzystują standardowe metodologie M&E":
        return 2
    else:
        return 0

def RCT_questions():
    st.subheader('Pytania dot. randomizowanych ewaluacji')
    st.write('Ta sekcja jest przeznaczona wyłącznie dla przedstawicieli Administracji Publicznej. Chcielibyśmy poznać Państwa opinię na temat randomizowanych badań kontrolnych (RCT) w kontekście programu Digitrans.')
    st.write('1. Po moich dotychczasowych doświadczeniach związanych z udziałem w tym projekcie:')
    RCT_Q1 = st.radio('Proszę wybrać jedną z poniższych opcji:', ['Jestem bardziej zainteresowany/a wykorzystaniem RCT do ewaluacji innych instrumentów wsparcia', 'Moje zainteresowanie wykorzystaniem RCT do ewaluacji innych instrumentów wsparcia nie zmieniło się', 'Jestem mniej zainteresowany/a wykorzystaniem RCT do ewaluacji innych instrumentów wsparcia'], index = get_rct1_index(safe_var('RCT_Q1')))
    save_input_to_session_state('RCT_Q1', RCT_Q1)
    
    st.write('2. Prosimy o porównanie Państwa doświadczeń z instrumentu wsparcia Digitrans, który oceniamy za pomocą metodologii RCT, z podobnymi instrumentami, w których uczestniczyli Państwo, a które nie były poddane takiej ewaluacji. Prosimy o porównanie tego projektu z podobnymi projektami bez eksperymentalnej ewaluacji pod względem:')
    st.write('- Projektowania interwencji')
    RCT_Q2 = st.radio('Proszę wybrać jedną z poniższych opcji:', ['RCT wprowadzilo do instrumentu wsparcia korzystne zmiany w porównaniu z instrumentami wsparcia bez RCT', 'RCT nie zmieniło sposobu, w jaki jest zaprojektowany instrument wsparcia', 'RCT spowodowało, że interwencja została zaprojektowana gorzej niż instrumenty bez RCT'], index = get_rct2_index(safe_var('RCT_Q2')))
    save_input_to_session_state('RCT_Q2', RCT_Q2)

    st.write('- Szybkości wdrażania')
    RCT_Q3 = st.radio('Proszę wybrać jedną z poniższych opcji:', ['RCT przyspieszyło wdrażanie instrumentu', 'RCT nie zmieniło tempa wdrażania instrumentu', 'RCT spowolniło tempo wdrażania instrumentu'],  index = get_rct3_index(safe_var('RCT_Q3')))
    save_input_to_session_state('RCT_Q3', RCT_Q3)

    st.write('- Wiarygodności informacji o rezultatach instrumentu (wplywie na dzialalność firm)')
    RCT_Q4 = st.radio('Proszę wybrać jedną z poniższych opcji:', ['Będę bardziej ufać danym o wpływie instrumentu mierzonego przy pomocy metodologii RCT niż w przypadku ewaluacji innych instrumentów, które wykorzystują standardowe metodologie w monitorowanie i ewaluacji (M&E),', "Będę w takim samym stopniu ufać danym o wpływie instrumentu mierzonego przy pomocy metodologii RCT niż w przypadku ewaluacji innych instrumentów, które wykorzystują standardowe metodologie M&E", "Będę mniej ufać danym o wpływie instrumentu mierzonego przy pomocy metodologii RCT niż w przypadku ewaluacji innych instrumentów, które wykorzystują standardowe metodologie M&E"],  index = get_rct4_index(safe_var('RCT_Q4')))
    save_input_to_session_state('RCT_Q4', RCT_Q4)

    st.write('- Czy uważają Państwo, że dzięki RCT udało się dotrzeć do nowych beneficjentów? Czy sądzą Państwo, że pomogło to w rozdysponowaniu większej ilości środków niż pierwotnie planowano?')
    input_RCT_Q5 = st.text_input('Miejsce na pole tekstowe', max_chars=500, key = 'RCT_question5', value=st.session_state.get('input_RCT_Q5', ''))
    save_input_to_session_state('input_RCT_Q5', input_RCT_Q5)

    st.write('- Czy mają Państwo jakiekolwiek inne przemyślenia dotyczące RCT, którymi chcieliby się Państwo podzielić?')
    input_RCT_Q6 = st.text_input('Miejsce na pole tekstowe.', max_chars=500, value=st.session_state.get('input_RCT_Q6', ''))
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

