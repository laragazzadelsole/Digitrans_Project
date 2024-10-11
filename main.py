import streamlit as st
import json
from fixed_components import *
from changing_components import *
import numpy as np

# Set page configuration
st.set_page_config(layout="wide")

# Load JSON configuration
config = json.load(open('config.json'))

initialize_session_state()


st.sidebar.title("Survey Index")
page = st.sidebar.radio("", [
    "Introduction",
    "Personal Information", 
    "Instructions", 
    "Question 1", 
    "Question 2", 
    "Question 3", 
    "Question 4", 
    "Question 5", 
    "Question 6", 
    "Question 7", 
    "Question 8", 
    "Question 9", 
    "Question 10", 
    "Question 11", 
    "Question 12"
])

# Personal information page
if page == "Introduction":
    introduction(config['header'])
    consent_form()

elif page == "Personal Information":
    personal_information()

# Instructions page
elif page == "Instructions":
    instructions()

# Question 1
elif page == "Question 1":
    q1_config = config['question1']
    answers1, percentage_difference1, num_bins1 = create_question(q1_config, safe_var('data1'))
    save_input_to_session_state('data1', answers1)
    

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q1_config, 1)
# Question 2
elif page == "Question 2":
    q2_config = config['question2']
    answers2, percentage_difference2, num_bins2 = create_question(q2_config, safe_var('data2'))
    save_input_to_session_state('data2', answers2)

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q2_config, 2)
# Question 3
elif page == "Question 3":
    q3_config = config['question3']
    answers3, percentage_difference3, num_bins3 = create_question(q3_config, safe_var('data3'))
    save_input_to_session_state('data3', answers3)

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q3_config, 3)
# Question 4
elif page == "Question 4":
    q4_config = config['question4']
    answers4, answers4_1, percentage_difference_1_4, percentage_difference_2_4, num_bins_1_4, num_bins_2_4 = double_question(q4_config, safe_var('data4'), safe_var('data4_1'))
    save_input_to_session_state('data4', answers4)
    save_input_to_session_state('data4_1', answers4_1)

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q4_config, 4)
# Question 5
elif page == "Question 5":
    q5_config = config['question5']
    answers5, answers5_1, percentage_difference_1_5, percentage_difference_2_5, num_bins_1_5, num_bins_2_5 = double_question(q5_config, safe_var('data5'), safe_var('data5_1'))
    save_input_to_session_state('data5', answers5)
    save_input_to_session_state('data5_1', answers5_1)

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q5_config, 5)
# Question 6
elif page == "Question 6":
    q6_config = config['question6']
    answers6, answers6_1, percentage_difference_1_6, percentage_difference_2_6, num_bins_1_6, num_bins_2_6 = double_question(q6_config, safe_var('data6'), safe_var('data6_1'))
    save_input_to_session_state('data6', answers6)
    save_input_to_session_state('data6_1', answers6_1)

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q6_config, 6)
# Question 7
elif page == "Question 7":
    q7_config = config['question7']
    answers7, percentage_difference7, num_bins7 = create_question(q7_config, safe_var('data7'))
    save_input_to_session_state('data7', answers7)
    

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q7_config, 7)
# Question 8
elif page == "Question 8":
    q8_config = config['question8']
    answers8, percentage_difference8, num_bins8 = create_question(q8_config, safe_var('data8'))
    save_input_to_session_state('data8', answers8)
    

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:
        effect_size_question(q8_config, 8)

# Question 9
elif page == "Question 9":
    q9_config = config['question9']
    answers9, percentage_difference9, num_bins9 = create_question(q9_config, safe_var('data9'))
    save_input_to_session_state('data9', answers9)
    _, col2, _, _ = st.columns(4)
    with col2:
        st.image("SatSunGraph.png", width=700)
    st.write("Saturday and Sunday temperatures in Washington DC for each weekend in 2022. As we might expect, there is a strong correlation between the temperature on a Saturday and on the Sunday, since some parts of the year are hot, and others colder. The correlation here is 0.88.")

# Question 10
elif page == "Question 10":
    q10_config = config['question10']
    answers10, percentage_difference10, num_bins10 = create_question(q10_config, safe_var('data10'))
    save_input_to_session_state('data10', answers10)

# Question 11 - Cost/Benefit
elif page == "Question 11":
    st.subheader("Question 11 - Cost/Benefit Ratio")
    st.write("In simple terms, a cost-benefit ratio is used to compare the costs of an action or project against the benefits it delivers...")
    col1, _ = st.columns(2)
    with col1:
        cost_benefit_list = [f"1:{round(i, 1)}" for i in np.arange(0.6, 3.1, .2)]
        cost_benefit_question = st.select_slider("Please move the slider to indicate your preference.", cost_benefit_list, value=st.session_state.get('cost_benefit_question', min(cost_benefit_list)))
        save_input_to_session_state('cost_benefit_question', cost_benefit_question)

# Question 12 - Risk Aversion
elif page == "Question 12":
    st.subheader("Question 12 - Risk Aversion")
    st.write("Rate your willingness to take risks in general on a 10-point scale, with 1 completely unwilling and 10 completely willing.")

    col1, _ = st.columns(2)
    with col1:
        risk_aversion_question =st.slider("Please move the slider to indicate your preference.", 1, 10, key="risk_aversion", value=st.session_state.get('risk_aversion_question', 0))
        save_input_to_session_state('risk_aversion_question', risk_aversion_question)

    if safe_var('professional_category') in ['Government Official/Donor', 'Researcher']:    
        RCT_questions()

# Add some spacing in the sidebar
for _ in range(9):
    st.sidebar.write("")

st.sidebar.button('submit', on_click=click_submit)

#SUBMISSION
if st.session_state.get('submit'):

    table_answers = {
    "answers1": st.session_state.get('data1'),
    "answers2": st.session_state.get('data2'),
    "answers3": st.session_state.get('data3'),
    "answers4": st.session_state.get('data4'),
    "answers4_1": st.session_state.get('data4_1'),
    "answers5": st.session_state.get('data5'),
    "answers5_1": st.session_state.get('data5_1'),
    "answers6": st.session_state.get('data6'),
    "answers6_1": st.session_state.get('data6_1'),
    "answers7": st.session_state.get('data7'),
    "answers8": st.session_state.get('data8'),
    "answers9": st.session_state.get('data9'),
    "answers10": st.session_state.get('data10')
    }

    def get_answer_df(question_number, colname):
        question_df = pd.DataFrame([list(table_answers[f'answers{question_number}'][colname]), list(table_answers[f'answers{question_number}']['Probability (%)'])])
        return question_df.rename(columns=question_df.iloc[0], copy=False).iloc[1:].reset_index(drop=True)

    df1 = get_answer_df('1', 'Percentage Points Change')
    df2 = get_answer_df('2', 'Percentage Points Change')
    df3 = get_answer_df('3', 'Percentage Change')
    df4 = get_answer_df('4', 'Percentage Change')
    df4_1 = get_answer_df('4_1', 'Percentage Change')
    df5 = get_answer_df('5', 'Percentage Change')
    df5_1 = get_answer_df('5_1', 'Percentage Change')
    df6 = get_answer_df('6', 'Percentage Change')
    df6_1 = get_answer_df('6_1', 'Percentage Change')
    df7 = get_answer_df('7', 'Percentage Change')
    df8 = get_answer_df('8', 'Percentage Change')
    df9 = get_answer_df('9', 'Correlation')
    df10 = get_answer_df('10', 'Correlation')


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
        "min_eff_size7_1": st.session_state.get('effect_size_question_7_answer_1'),
        "min_eff_size7_2": st.session_state.get('effect_size_question_7_answer_2'),
        "min_eff_size8_1": st.session_state.get('effect_size_question_8_answer_1'),
        "min_eff_size8_2": st.session_state.get('effect_size_question_8_answer_2'),
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
   
    st.success(f"Thank you for completing the Survey on {config['header']['survey_title']}!")

