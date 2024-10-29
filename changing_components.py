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
        st.markdown("- V porovnaní so SKUPINOU 1, ktorá dostáva len finančný voucher.")
        answer_1 = st.text_input("Prosím, zadajte číslo alebo napíšte 'Neviem'.", key = jsonfile_name['num_input_question_1'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_1', ''))
        st.markdown("- V porovnaní so SKUPINOU 3, ktorá dostáva len benchmarkingovú správu.")
        answer_2 = st.text_input("Prosím, zadajte číslo alebo napíšte 'Neviem'.", key = jsonfile_name['num_input_question_2'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_2', ''))
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_1', answer_1)
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_2', answer_2)


def get_rct1_index(RCT_Q1):
    if RCT_Q1 == 'Som viac zainteresovaný/á využívať RCT na hodnotenie iných podporných nástrojov':
        return 0
    elif RCT_Q1 == 'Môj záujem o využívanie RCT na hodnotenie iných podporných nástrojov sa nezmenil':
        return 1
    elif RCT_Q1 == 'Som menej zainteresovaný/á využívať RCT na hodnotenie iných podporných nástrojov':
        return 2
    else:
        return 0
    
def get_rct2_index(RCT_Q2):
    if RCT_Q2 == 'RCT zaviedlo do podporného nástroja prospešné zmeny v porovnaní s podpornými nástrojmi bez RCT':
        return 0
    elif RCT_Q2 == 'RCT nezmenilo spôsob, akým je podporný nástroj navrhnutý':
        return 1
    elif RCT_Q2 == 'RCT spôsobilo, že intervencia bola navrhnutá horšie ako nástroje bez RCT':
        return 2
    else:
        return 0
    
def get_rct3_index(RCT_Q3):
    if RCT_Q3 == 'RCT urýchlilo implementáciu nástroja':
        return 0
    elif RCT_Q3 == 'RCT nezmenilo tempo implementácie nástroja':
        return 1
    elif RCT_Q3 == 'RCT spomalilo tempo implementácie nástroja':
        return 2
    else:
        return 0

def get_rct4_index(RCT_Q4):
    if RCT_Q4 == 'Budem viac dôverovať údajom o vplyve nástroja meraného pomocou metodológie RCT než v prípade hodnotenia iných nástrojov, ktoré využívajú štandardné metodológie monitorovania a hodnotenia (M&E)':
        return 0
    elif RCT_Q4 == "Budem rovnako dôverovať údajom o vplyve nástroja meraného pomocou metodológie RCT ako v prípade hodnotenia iných nástrojov, ktoré využívajú štandardné metodológie M&E":
        return 1
    elif RCT_Q4 == "Budem menej dôverovať údajom o vplyve nástroja meraného pomocou metodológie RCT než v prípade hodnotenia iných nástrojov, ktoré využívajú štandardné metodológie M&E":
        return 2
    else:
        return 0

def RCT_questions():
    st.subheader('Otázky týkajúce sa randomizovaných hodnotení')
    st.write('Táto časť je určená výlučne pre zástupcov Verejnej správy. Chceli by sme poznať Váš názor na randomizované kontrolované štúdie (Randomized Controlled Trials - RCT) v kontexte programu Digitrans.')
    st.write('1. Po mojich doterajších skúsenostiach spojených s účasťou na tomto projekte:')
    RCT_Q1 = st.radio('Prosím, vyberte jednu z nasledujúcich možností', ['Som viac zainteresovaný/á využívať RCT na hodnotenie iných podporných nástrojov', 'Môj záujem o využívanie RCT na hodnotenie iných podporných nástrojov sa nezmenil', 'Som menej zainteresovaný/á využívať RCT na hodnotenie iných podporných nástrojov'], index = get_rct1_index(safe_var('RCT_Q1')))
    save_input_to_session_state('RCT_Q1', RCT_Q1)
    
    st.write('2. Prosíme Vás o porovnanie Vašich skúseností s podporným nástrojom Digitrans, ktorý hodnotíme pomocou metodológie RCT, s podobnými nástrojmi, na ktorých ste sa zúčastnili, a ktoré neboli podrobené takémuto hodnoteniu. Prosíme o porovnanie tohto projektu s podobnými projektmi bez experimentálneho hodnotenia z hľadiska:')
    st.write('- Navrhovania intervencie')
    RCT_Q2 = st.radio('Prosím, vyberte jednu z nasledujúcich možností', ['RCT zaviedlo do podporného nástroja prospešné zmeny v porovnaní s podpornými nástrojmi bez RCT', 'RCT nezmenilo spôsob, akým je podporný nástroj navrhnutý', 'RCT spôsobilo, že intervencia bola navrhnutá horšie ako nástroje bez RCT'], index = get_rct2_index(safe_var('RCT_Q2')))
    save_input_to_session_state('RCT_Q2', RCT_Q2)

    st.write('- Rýchlosti implementácie')
    RCT_Q3 = st.radio('Prosím, vyberte jednu z nasledujúcich možností', ["RCT urýchlilo implementáciu nástroja", "RCT nezmenilo tempo implementácie nástroja", "RCT spomalilo tempo implementácie nástroja"],  index = get_rct3_index(safe_var('RCT_Q3')))
    save_input_to_session_state('RCT_Q3', RCT_Q3)

    st.write('- Dôveryhodnosť informácií o výsledkoch nástroja (vplyve na činnosť firiem)')
    RCT_Q4 = st.radio('Prosím, vyberte jednu z nasledujúcich možností', ["Budem viac dôverovať údajom o vplyve nástroja meraného pomocou metodológie RCT než v prípade hodnotenia iných nástrojov, ktoré využívajú štandardné metodológie monitorovania a hodnotenia (M&E)", "Budem rovnako dôverovať údajom o vplyve nástroja meraného pomocou metodológie RCT ako v prípade hodnotenia iných nástrojov, ktoré využívajú štandardné metodológie M&E", "Budem menej dôverovať údajom o vplyve nástroja meraného pomocou metodológie RCT než v prípade hodnotenia iných nástrojov, ktoré využívajú štandardné metodológie M&E"],  index = get_rct4_index(safe_var('RCT_Q4')))
    save_input_to_session_state('RCT_Q4', RCT_Q4)

    st.write('- Myslíte si, že vďaka RCT sa podarilo osloviť nových príjemcov programu? Myslíte si, že to pomohlo rozdeliť viac prostriedkov, ako sa pôvodne plánovalo?')
    input_RCT_Q5 = st.text_input('Prosím, napíšte svoje skúsenosti:', max_chars=500, key = 'RCT_question5', value=st.session_state.get('input_RCT_Q5', ''))
    save_input_to_session_state('input_RCT_Q5', input_RCT_Q5)

    st.write('- Myslíte si, že prideľovanie podpory s rovnakou pravdepodobnosťou medzi firmy spĺňajúce kritériá prístupu je etické? Mali ste rovnaký názor pred oboznámením sa s informáciami o metodológii RCT? Máte akékoľvek iné úvahy týkajúce sa RCT, o ktoré by ste sa chceli podeliť?')
    input_RCT_Q6 = st.text_input('Prosím, napíšte svoje skúsenosti:', max_chars=500, value=st.session_state.get('input_RCT_Q6', ''))
    save_input_to_session_state('input_RCT_Q6', input_RCT_Q6)

    st.write('Ďakujeme za Váš venovaný čas a zdieľanie Vašich cenných postrehov o pilotnom nástroji Digitrans.')


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

