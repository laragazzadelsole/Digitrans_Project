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



def initialize_session_state():
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
        st.session_state['continue'] = False
        #st.session_state['professional_category'] = 'Government Official/Donor'
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    return None

def create_question(jsonfile_name, existing_data=None):
    minor_value = str(jsonfile_name['minor_value'])
    min_value = jsonfile_name['min_value_graph']
    max_value = jsonfile_name['max_value_graph']
    interval = jsonfile_name['step_size_graph']
    major_value = str(jsonfile_name['major_value'])

    # Create a list of ranges based on the provided values
    x_axis = [minor_value] + [f"{round(i, 1)}% to {round((i + interval - 0.01), 2)}%" for i in np.arange(min_value, max_value, interval)] + [major_value]

    # TODO find a way to remove it
    if jsonfile_name['min_value_graph'] == -1:
        x_axis.insert(6, "0%")
        x_axis[1] = '-0.99% to -0.81%'
        x_axis[7] = '0.01% to 0.19%'
    elif jsonfile_name['min_value_graph'] == -30:
        x_axis.insert(7, "0%")
        x_axis[8] = '0.01% to 4.99%'
    elif jsonfile_name['min_value_graph'] == -15:
        x_axis.insert(4, "0%")
        x_axis[5] = '0.01% to 4.99%'
   
    y_axis = np.zeros(len(x_axis))

    data = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[jsonfile_name['column_1'], jsonfile_name['column_2']]) if existing_data is None else existing_data

    st.subheader(jsonfile_name['title_question'])
    st.write(jsonfile_name['subtitle_question'])
    
    data_container = st.container()
    with data_container:
        table, plot = st.columns([0.3, 0.7], gap="large")
        with table:
            bins_grid = st.data_editor(data, key= jsonfile_name['data_editor_1'], hide_index=True, use_container_width=True, disabled=[jsonfile_name['column_1']])
            percentage_difference = 100 - sum(bins_grid[jsonfile_name['column_2']])

            # Display the counter
            if percentage_difference > 0:
                missing_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You still have to allocate {percentage_difference}% probability.</b>'
                st.markdown(missing_prob, unsafe_allow_html=True)
                
            elif percentage_difference == 0:
                total_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You have allocated all probabilities!</b>'
                st.markdown(total_prob, unsafe_allow_html=True)
            else:
                exceeding_prob = f'<b style="font-family:sans-serif; color:Red; font-size: 20px; ">You have inserted {abs(percentage_difference)}% more, please review your percentage distribution.</b>'
                st.markdown(exceeding_prob, unsafe_allow_html=True)
                      
        with plot:
            # Extract the updated values from the second column
            updated_values = bins_grid[jsonfile_name['column_2']]

            # Plot the updated values as a bar plot
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=bins_grid[jsonfile_name['column_1']], 
                y=updated_values, 
                marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
                marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
                marker_line_width=2,  # Width of the bar outline
                text=[f"{p}" for p in bins_grid[jsonfile_name['column_2']]],  # Adding percentage labels to bars
                textposition='auto',
                name='Probability'
            ))

            fig.update_layout(
                title={
                    'text': "Probability distribution",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title="Expectation Range",
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

    return bins_grid, percentage_difference, len(bins_grid)

#####################################################################

def double_question(jsonfile_name, existing_data1=None, existing_data2=None):
    minor_value = str(jsonfile_name['minor_value'])
    min_value = jsonfile_name['min_value_graph']
    max_value = jsonfile_name['max_value_graph']
    interval = jsonfile_name['step_size_graph']
    major_value = str(jsonfile_name['major_value'])

    # Create a list of ranges based on the provided values
    x_axis = [minor_value] + [f"{round(i, 1)}% to {round((i + interval - 0.01), 2)}%" for i in np.arange(min_value, max_value, interval)] + [major_value]

    # TODO find a way to remove it
    if jsonfile_name['min_value_graph'] == -1:
        x_axis.insert(6, "0%")
        x_axis[1] = '-0.99% to -0.81%'
        x_axis[7] = '0.01% to 0.19%'
    elif jsonfile_name['min_value_graph'] == -15:
        x_axis.insert(4, "0%")
        x_axis[5] = '0.01% to 4.99%'

    y_axis = np.zeros(len(x_axis))

    data1 = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[jsonfile_name['column_1'], jsonfile_name['column_2']]) if existing_data1 is None else existing_data1

    st.subheader(jsonfile_name['title_question'])
    st.write(jsonfile_name['subtitle_question'])

    st.markdown("- In comparison to GROUP 1 that receives Financial Subsidy only.")
    data_container = st.container()
    with data_container:
        table, plot = st.columns([0.3, 0.7], gap="large")
        with table:
            bins_grid_1 = st.data_editor(data1, key= jsonfile_name['data_editor_1'], hide_index=True, use_container_width=True, disabled=[jsonfile_name['column_1']])
            percentage_difference_1 = 100 - sum(bins_grid_1[jsonfile_name['column_2']])

            # Display the counter
            if percentage_difference_1 > 0:
                missing_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You still have to allocate {percentage_difference_1}% probability.</b>'
                st.markdown(missing_prob, unsafe_allow_html=True)
                
            elif percentage_difference_1 == 0:
                total_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You have allocated all probabilities!</b>'
                st.markdown(total_prob, unsafe_allow_html=True)
            else:
                exceeding_prob = f'<b style="font-family:sans-serif; color:Red; font-size: 20px; ">You have inserted {abs(percentage_difference_1)}% more, please review your percentage distribution.</b>'
                st.markdown(exceeding_prob, unsafe_allow_html=True)
                      
        with plot:
            # Extract the updated values from the second column
            updated_values = bins_grid_1[jsonfile_name['column_2']]

            # Plot the updated values as a bar plot
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=bins_grid_1[jsonfile_name['column_1']], 
                y=updated_values, 
                marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
                marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
                marker_line_width=2,  # Width of the bar outline
                text=[f"{p}" for p in bins_grid_1[jsonfile_name['column_2']]],  # Adding percentage labels to bars
                textposition='auto',
                name='Probability'
            ))

            fig.update_layout(
                title={
                    'text': "Probability distribution",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title="Expectation Range",
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

    data2 = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[jsonfile_name['column_1'], jsonfile_name['column_2']]) if existing_data2 is None else existing_data2

    st.markdown("- In comparison to GROUP 3 that receives Benchmarking Report.")
    data_container = st.container()
    with data_container:
        table, plot = st.columns([0.3, 0.7], gap="large")
        with table:
            bins_grid_2 = st.data_editor(data2, key= jsonfile_name['data_editor_2'], hide_index=True, use_container_width=True, disabled=[jsonfile_name['column_1']])
            percentage_difference_2 = 100 - sum(bins_grid_2[jsonfile_name['column_2']])

            # Display the counter
            if percentage_difference_2 > 0:
                missing_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You still have to allocate {percentage_difference_2}% probability.</b>'
                st.markdown(missing_prob, unsafe_allow_html=True)
                
            elif percentage_difference_2 == 0:
                total_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You have allocated all probabilities!</b>'
                st.markdown(total_prob, unsafe_allow_html=True)
            else:
                exceeding_prob = f'<b style="font-family:sans-serif; color:Red; font-size: 20px; ">You have inserted {abs(percentage_difference_2)}% more, please review your percentage distribution.</b>'
                st.markdown(exceeding_prob, unsafe_allow_html=True)
                      
        with plot:
            # Extract the updated values from the second column
            updated_values = bins_grid_2[jsonfile_name['column_2']]

            # Plot the updated values as a bar plot
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=bins_grid_2[jsonfile_name['column_1']], 
                y=updated_values, 
                marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
                marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
                marker_line_width=2,  # Width of the bar outline
                text=[f"{p}" for p in bins_grid_2[jsonfile_name['column_2']]],  # Adding percentage labels to bars
                textposition='auto',
                name='Probability'
            ))

            fig.update_layout(
                title={
                    'text': "Probability distribution",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title="Expectation Range",
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


    return bins_grid_1, bins_grid_2, percentage_difference_1, percentage_difference_2, len(bins_grid_1), len(bins_grid_2)

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

'''
def generate_df(updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_1_4_df, updated_bins_question_2_4_df, updated_bins_question_1_5_df, updated_bins_question_2_5_df, updated_bins_question_1_6_df, updated_bins_question_2_6_df, updated_bins_question_7_df, updated_bins_question_8_df, updated_bins_question_9_df, updated_bins_question_10_df):
    """
    This function generates and returns the concatenated DataFrame (concatenated_df) 
    from the given updated bins DataFrames.
    """
    updated_bins_list = pd.DataFrame[updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_1_4_df, updated_bins_question_2_4_df, updated_bins_question_1_5_df, updated_bins_question_2_5_df, updated_bins_question_1_6_df, updated_bins_question_2_6_df, updated_bins_question_7_df, updated_bins_question_8_df, updated_bins_question_9_df, updated_bins_question_10_df]

    def restructure_df(df, i):
        transposed_df = df.transpose()
        transposed_df.columns = [f'Q{i + 1}  {col}' for col in list(transposed_df.iloc[0])]
        transposed_df = transposed_df.iloc[1:]
        return transposed_df

    # Transpose and restructure each DataFrame in the list
    transposed_bins_list = []
    for i, df in enumerate(updated_bins_list):
        transposed_bins_list.append(restructure_df(df, i))
    
    # Concatenate the transposed DataFrames
    questions_df = pd.concat(transposed_bins_list, axis=1)
    questions_df.reset_index(drop=True, inplace=True)

    # Retrieve data from session state
    data = st.session_state['data']
    session_state_df = pd.DataFrame(data)

    # Splitting data into sections
    personal_data_df = session_state_df.iloc[:, :4]
    min_eff_df = session_state_df.iloc[:, 4:]

    # Concatenate the different sections into the final DataFrame
    df = pd.concat([personal_data_df, questions_df.set_index(personal_data_df.index), min_eff_df.set_index(personal_data_df.index)], axis=1)
    
    return df
'''

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
    #backup_sheet = client.create(f'Backup_{df.iloc[4]}_{datetime.now()}', folder_id= secrets_to_json()['folder_id']).sheet1
    #backup_sheet = backup_sheet.append_rows(df.values.tolist()) #(new_bins_df.iloc[:2].values.tolist())
    #backup_sheet.share('', perm_type = 'user', role = 'writer')

