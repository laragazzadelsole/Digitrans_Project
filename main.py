import streamlit as st
import json
from fixed_components import *
from changing_components import *
from utils import initialize_session_state
from components import sidebar, survey_introduction, consent_form, personal_information, instructions, create_question, double_question, risk_aversion_question, cost_benefit_question
import numpy as np

## NICE TO HAVE:
#   - switch/match case for questions
#   - set as variable the names like user_full_name, etc...

# Set page configuration
st.set_page_config(layout="wide")

# Load JSON configuration
config = json.load(open('config.json', encoding="utf8"))

# Initializing session state if not already initialized
if 'initialized' not in st.session_state:
    initialize_session_state()

# Define sidebar radio selection buttons
sidebar_page_selection = sidebar()

# Personal information page
if sidebar_page_selection == "Úvod":
    survey_introduction(config)
    consent_form()

elif sidebar_page_selection == "Osobné údaje":
    personal_information()

# Instructions page
elif sidebar_page_selection == "Inštrukcie":
    instructions()

# Question 1
elif sidebar_page_selection == "Otázka 1":
    q1_config = config['question1']
    create_question(q1_config)
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:
        effect_size_question(q1_config, 1)
        
# Question 2
elif sidebar_page_selection == "Otázka 2":
    q2_config = config['question2']
    create_question(q2_config)
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:
        effect_size_question(q2_config, 2)
# Question 3
elif sidebar_page_selection == "Otázka 3":
    q3_config = config['question3']
    create_question(q3_config)
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:
        effect_size_question(q3_config, 3)
# Question 4
elif sidebar_page_selection == "Otázka 4":
    q4_config = config['question4']
    double_question(q4_config)
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:
        effect_size_question(q4_config, 4)

# Question 5
elif sidebar_page_selection == "Otázka 5":
    q5_config = config['question5']
    double_question(q5_config)
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:
        effect_size_question(q5_config, 5)
# Question 6
elif sidebar_page_selection == "Otázka 6":
    q6_config = config['question6']
    double_question(q6_config)
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:
        effect_size_question(q6_config, 6)

# Question 7
elif sidebar_page_selection == "Otázka 7":
    q7_config = config['question7']
    create_question(q7_config)

    
# Question 8
elif sidebar_page_selection == "Otázka 8":
    q8_config = config['question8']
    create_question(q8_config)


# Question 9
elif sidebar_page_selection == "Otázka 9":
    q9_config = config['question9']
    create_question(q9_config)
    _, col2, _, _ = st.columns(4)
    with col2:
        st.image("SatSunGraph.png", width=700)
    st.write("Nižšie uvádzame graf zobrazujúci koreláciu medzi teplotami v soboty a v nedele pre každý víkend roku 2022 vo Washingtone. Ako sa dalo očakávať, existuje silná korelácia medzi teplotou v sobotu a teplotou v nedeľu, pretože niektoré časti roka sú horúce a iné chladnejšie. V tomto prípade je korelácia 0,88, čo naznačuje veľmi silný pozitívny vzťah.")

# Question 10
elif sidebar_page_selection == "Otázka 10":
    q10_config = config['question10']
    create_question(q10_config)

# Question 11 - Cost/Benefit
elif sidebar_page_selection == "Otázka 11":
    cost_benefit_question()

# Question 12 - Risk Aversion
elif sidebar_page_selection == "Otázka 12":
    risk_aversion_question()
    if safe_var('professional_category') in ['Verejná správa', 'Výskumný tím']:    
        RCT_questions()

# Add some spacing in the sidebar
for _ in range(4):
    st.sidebar.write("")

st.sidebar.write("Prosím, prejdite si všetky otázky, aby ste sa uistili, že ste ich všetky vyplnili, predtým ako kliknete na Odoslať.")

st.sidebar.button('Odoslať', on_click=click_submit)

#SUBMISSION
if st.session_state.get('submit'):

    table_answers = {
    "answers1": st.session_state.get(config['question1']["session_state_dataframe_name"]),
    "answers2": st.session_state.get(config['question2']["session_state_dataframe_name"]),
    "answers3": st.session_state.get(config['question3']["session_state_dataframe_name"]),
    "answers4": st.session_state.get(config['question4']["session_state_dataframe_name_1"]),
    "answers4_1": st.session_state.get(config['question4']["session_state_dataframe_name_2"]),
    "answers5": st.session_state.get(config['question5']["session_state_dataframe_name_1"]),
    "answers5_1": st.session_state.get(config['question5']["session_state_dataframe_name_2"]),
    "answers6": st.session_state.get(config['question6']["session_state_dataframe_name_1"]),
    "answers6_1": st.session_state.get(config['question6']["session_state_dataframe_name_2"]),
    "answers7": st.session_state.get(config['question7']["session_state_dataframe_name"]),
    "answers8": st.session_state.get(config['question8']["session_state_dataframe_name"]),
    "answers9": st.session_state.get(config['question9']["session_state_dataframe_name"]),
    "answers10": st.session_state.get(config['question10']["session_state_dataframe_name"])
    }

    def get_answer_df(question_number, colname):
        question_df = pd.DataFrame([list(table_answers[f'answers{question_number}'][colname]), list(table_answers[f'answers{question_number}']['Pravdepodobnosť (%)'])])
        return question_df.rename(columns=question_df.iloc[0], copy=False).iloc[1:].reset_index(drop=True)

    df1 = get_answer_df('1', 'Percentuálne body')
    df2 = get_answer_df('2', 'Percentuálne body')
    df3 = get_answer_df('3', 'Percento')
    df4 = get_answer_df('4', 'Percento')
    df4_1 = get_answer_df('4_1', 'Percento')
    df5 = get_answer_df('5', 'Percento')
    df5_1 = get_answer_df('5_1', 'Percento')
    df6 = get_answer_df('6', 'Percento')
    df6_1 = get_answer_df('6_1', 'Percento')
    df7 = get_answer_df('7', 'Percento')
    df8 = get_answer_df('8', 'Percento')
    df9 = get_answer_df('9', 'Korelácia')
    df10 = get_answer_df('10', 'Korelácia')


    df_list = [df1, df2, df3, df4, df4_1, df5, df5_1, df6, df6_1, df7, df8, df9, df10]

    #questions_df = pd.read_csv('question_df.csv', header=None)
    questions_df = pd.concat(df_list, axis=1)

    data = {
        "user_name": st.session_state.get('user_full_name'),
        "user_position": st.session_state.get('user_position'),
        "user_profession": st.session_state.get('professional_category'),
        "user_experience": st.session_state.get('years_of_experience'),
        "min_eff_size1_1": st.session_state.get('effect_size_question_1_answer_1'),
        "min_eff_size1_2": st.session_state.get('effect_size_question_1_answer_2'),
        "min_eff_size2_1": st.session_state.get('effect_size_question_2_answer_1'),
        "min_eff_size2_2": st.session_state.get('effect_size_question_2_answer_2'),
        "min_eff_size3_1": st.session_state.get('effect_size_question_3_answer_1'),
        "min_eff_size3_2": st.session_state.get('effect_size_question_3_answer_2'),
        "min_eff_size4_1": st.session_state.get('effect_size_question_4_answer_1'),
        "min_eff_size4_2": st.session_state.get('effect_size_question_4_answer_2'),
        "min_eff_size5_1": st.session_state.get('effect_size_question_5_answer_1'),
        "min_eff_size5_2": st.session_state.get('effect_size_question_5_answer_2'),
        "min_eff_size6_1": st.session_state.get('effect_size_question_6_answer_1'),
        "min_eff_size6_2": st.session_state.get('effect_size_question_6_answer_2'),
        "cost_benefit_answer": st.session_state.get('cost_benefit_question'),
        "risk_aversion_answer": st.session_state.get('risk_aversion_question'),
        "RCT_Q1_answer": st.session_state.get('RCT_Q1'),
        "RCT_Q2_answer": st.session_state.get('RCT_Q2'),
        "RCT_Q3_answer": st.session_state.get('RCT_Q3'),
        "RCT_Q4_answer": st.session_state.get('RCT_Q4'),
        "RCT_Q5_answer": st.session_state.get('input_RCT_Q5'),
        "RCT_Q6_answer": st.session_state.get('input_RCT_Q6'),
    }

    personal_data_df = pd.DataFrame([data]).iloc[:, : 4]
    additional_questions_df = pd.DataFrame([data]).iloc[:, 4: ]
    final_df = pd.concat([personal_data_df, questions_df, additional_questions_df], axis=1)

    add_submission(final_df)
   
    st.sidebar.success(f"Ďakujeme, že ste vyplnili prieskum! Vaše odpovede boli zaregistrované.")

