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

def effect_size_question(jsonfile_name, question_number):
        st.markdown(jsonfile_name['effect_size'])
        st.markdown("- В сравнение с ГРУПА 1, която получава само Финансов ваучер.")
        answer_1 = st.text_input("Моля, въведете число или напишете 'Не знам'", key = jsonfile_name['num_input_question_1'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_1', ''))
        st.markdown("- В сравнение с ГРУПА 3, която получава само Доклад за сравнителен анализ.")
        answer_2 = st.text_input("Моля, въведете число или напишете 'Не знам'.", key = jsonfile_name['num_input_question_2'], value=st.session_state.get(f'effect_size_question_{question_number}_answer_2', ''))
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_1', answer_1)
        save_input_to_session_state(f'effect_size_question_{question_number}_answer_2', answer_2)


def get_rct1_index(RCT_Q1):
    if RCT_Q1 == 'Аз съм по-заинтересован/а от използването на RCT за оценка на други инструменти за подкрепа':
        return 0
    elif RCT_Q1 == 'Моят интерес към използването на RCT за оценка на други инструменти за подкрепа не се е променил':
        return 1
    elif RCT_Q1 == 'Аз съм по-малко заинтересован/а от използването на RCT за оценка на други инструменти за подкрепа.':
        return 2
    else:
        return 0
    
def get_rct2_index(RCT_Q2):
    if RCT_Q2 == '•	RCT въведе благоприятни промени в инструмента за подкрепа в сравнение с инструментите за подкрепа без RCT':
        return 0
    elif RCT_Q2 == 'RCT не промени начина, по който е проектиран инструментът за подкрепа':
        return 1
    elif RCT_Q2 == 'RCT доведе до това, че интервенцията беше проектирана по-лошо от инструментите без RCT':
        return 2
    else:
        return 0
    
def get_rct3_index(RCT_Q3):
    if RCT_Q3 == 'RCT ускори внедряването на инструмента':
        return 0
    elif RCT_Q3 == 'RCT не промени темпото на внедряване на инструмента':
        return 1
    elif RCT_Q3 == 'RCT забави темпото на внедряване на инструмента':
        return 2
    else:
        return 0

def get_rct4_index(RCT_Q4):
    if RCT_Q4 == 'Ще имам повече доверие на данните за въздействието на инструмента, измерено с помощта на методологията RCT, отколкото в случай на оценка на други инструменти, които използват стандартни методологии за мониторинг и оценка (M&E)':
        return 0
    elif RCT_Q4 == "Ще имам същото ниво на доверие в данните за въздействието на инструмента, измерено с помощта на методологията RCT, както и в случай на оценка на други инструменти, които използват стандартни методологии за M&E":
        return 1
    elif RCT_Q4 == "Ще имам по-малко доверие в данните за въздействието на инструмента, измерено с помощта на методологията RCT, отколкото в случай на оценка на други инструменти, които използват стандартни методологии за M&E":
        return 2
    else:
        return 0

def RCT_questions():
    st.subheader('Въпроси относно рандомизираните оценки')
    st.write('Тази секция е предназначена само за представители на Публичната администрация. Бихме искали да разберем Вашето мнение относно рандомизираните контролирани изследвания (RCT) в контекста на програмата Digitrans.')
    st.write('1. След моя досегашен опит, свързан с участието в този проект:')
    RCT_Q1 = st.radio('Моля, изберете една от следните опции:', ["Аз съм по-заинтересован/а от използването на RCT за оценка на други инструменти за подкрепа", "Моят интерес към използването на RCT за оценка на други инструменти за подкрепа не се е променил", "Аз съм по-малко заинтересован/а от използването на RCT за оценка на други инструменти за подкрепа."], index = get_rct1_index(safe_var('RCT_Q1')))
    save_input_to_session_state('RCT_Q1', RCT_Q1)
    
    st.write('2. Моля, сравнете Вашия опит с инструмента за подкрепа Digitrans, който оценяваме с помощта на методологията RCT, с подобни инструменти, в които сте участвали, но които не са били подложени на такава оценка. Моля, сравнете този проект с подобни проекти без експериментална оценка по отношение на:')
    st.write('- Проектиране на интервенцията')
    RCT_Q2 = st.radio('Моля, изберете една от следните опции:', ['RCT въведе благоприятни промени в инструмента за подкрепа в сравнение с инструментите за подкрепа без RCT', 'RCT не промени начина, по който е проектиран инструментът за подкрепа', 'RCT доведе до това, че интервенцията беше проектирана по-лошо от инструментите без RCT'], index = get_rct2_index(safe_var('RCT_Q2')))
    save_input_to_session_state('RCT_Q2', RCT_Q2)

    st.write('- Скорост на внедряване')
    RCT_Q3 = st.radio('Моля, изберете една от следните опции:', ['RCT ускори внедряването на инструмента', 'RCT не промени темпото на внедряване на инструмента', 'RCT забави темпото на внедряване на инструмента'],  index = get_rct3_index(safe_var('RCT_Q3')))
    save_input_to_session_state('RCT_Q3', RCT_Q3)

    st.write('- Достоверност на информацията за резултатите от инструмента (въздействие върху дейността на фирмите)')
    RCT_Q4 = st.radio('Моля, изберете една от следните опции:', ['Ще имам повече доверие на данните за въздействието на инструмента, измерено с помощта на методологията RCT, отколкото в случай на оценка на други инструменти, които използват стандартни методологии за мониторинг и оценка (M&E)', "Ще имам същото ниво на доверие в данните за въздействието на инструмента, измерено с помощта на методологията RCT, както и в случай на оценка на други инструменти, които използват стандартни методологии за M&E", "Ще имам по-малко доверие в данните за въздействието на инструмента, измерено с помощта на методологията RCT, отколкото в случай на оценка на други инструменти, които използват стандартни методологии за M&E"],  index = get_rct4_index(safe_var('RCT_Q4')))
    save_input_to_session_state('RCT_Q4', RCT_Q4)

    st.write('- Смятате ли, че благодарение на RCT успяхме да достигнем до нови бенефициенти? Смятате ли, че това помогна за разпределянето на повече средства, отколкото първоначално беше планирано?')
    input_RCT_Q5 = st.text_input('Място за текстово поле', max_chars=500, key = 'RCT_question5', value=st.session_state.get('input_RCT_Q5', ''))
    save_input_to_session_state('input_RCT_Q5', input_RCT_Q5)

    st.write('- Смятате ли, че разпределянето на подкрепата с еднаква вероятност между фирмите, отговарящи на критериите за допустимост, е етично? Имахте ли същото мнение, преди да се запознаете с информацията относно методологията RCT?')
    input_RCT_Q6 = st.text_input('Място за текстово поле', max_chars=500, value=st.session_state.get('input_RCT_Q6', ''))
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

    sheet_row_update = sheet.append_rows(df.values.tolist()) 
    
    #Navigate to the folder in Google Drive. Copy the Folder ID found in the URL. This is everything that comes after “folder/” in the URL.
    backup_sheet = client.create(f'Backup_{df.iloc[0, 0]}_{datetime.now()}', folder_id= secrets_to_json()['folder_id']).sheet1
    backup_sheet = backup_sheet.append_rows(df.values.tolist())

