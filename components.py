import streamlit as st
from utils import save_input_to_session_state, safe_var, update_dataframe_session_state
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Sidebar constants
SIDEBAR_TITLE = "Spis Treści"
NUMBER_OF_QUESTIONS = 12
INFORMATION_PAGES = ["Wprowadzenie", "Dane osobowe", "Instrukcje"]
QUESTION_PAGES = [f"Pytanie {question_number}" for question_number in range(1, NUMBER_OF_QUESTIONS + 1)]

# Consent constants
CONSENT_TITLE = "Przesyłając poniższy formularz, wyrażają Państwo zgodę na wykorzystanie Państwa odpowiedzi do celów badawczych."
CONSENT_SENTENCE = "Wyrażam zgodę."
CONSENT_SUCCESS = "Dziękujemy za współpracę i czekamy na Państwa odpowiedzi!"

# Personal information constants
PERSONAL_INFORMATION_PAGE_TITLE = "Dane osobowe"
PERSONAL_INFORMATION_CONFIG = {
    "user_full_name": "Imię i nazwisko:",
    "user_position": "Stanowisko:",
    "user_professional_category": "Grupa:",
    "user_years_of_experience": "Proszę wpisać liczbę lat doświadczenia,  które posiada Pan/Pani we wspieraniu cyfryzacji sektora prywatnego:"
}
PROFESSIONAL_CATEGORY_OPTIONS = ("Administracja publiczna", "Instytucja wdrażająca instrument", "Zespół badawczy")

# Instructions constants
INSTRUCTIONS_TITLE = "Instrukcje"
INSTRUCTIONS_SUBTITLE = """
    Poniższy przykład ma na celu pomóc Państwu zrozumieć format pytań w tej ankiecie oraz dowiedzieć się, w jaki sposób udzielać odpowiedzi dotyczące wpływu uczestnictwa w programie Digitrans na działalność beneficjentów. \\
    Dla każdego pytania znajdą Państwo tabelę z interwałami, taką jak ta poniżej. Odpowiadając na pytanie proszę przydzielić prawdopodobieństwo każdej z sytuacji, wpisując liczbę w poszczególnych komórkach, w zależności od prawdopodobieństwa, że Państwa zdaniem wystąpi określone zdarzenie. Proszę pamiętać, że suma prawdopodobieństw przyporządkowana wszystkim styuacjom nie może przekroczyć 100%.\\
    Na przykład wyobraźmy sobie, że pytamy o Państwa przekonania dotyczące maksymalnej temperatury w stopniach Celsjusza w Państwa mieście lub miejscowości jutro, biorąc pod uwagę, że jest lato, a prognoza pogody przewiduje ulewne deszcze od rana. Poniższa tabela zawiera przykładowe odpowiedzi.
"""
INSTRUCTIONS_CAPTION = """
    Na przykład wyobraźmy sobie, że pytamy o Państwa przekonania dotyczące maksymalnej temperatury w stopniach Celsjusza w Państwa mieście lub miejscowości jutro, biorąc pod uwagę, że jest lato, a prognoza pogody przewiduje ulewne deszcze od rana. Poniższa tabela zawiera przykładowe odpowiedzi.
    """
INSTRUCTION_TABLE_TITLE = "Prognoza temperatury"
INSTRUCTION_TABLE_SUBTITLE = "_Przewiń tabelę, aby zobaczyć wszystkie dostępne opcje._"

# This config are shared across all plots in the survey
PLOT_CONFIG = {
    "title": {
                "text": "Rozkład prawdopodobieństwa",
                "y":0.9,
                "x":0.5,
                "xanchor": "center",
                "yanchor": "top"
            },
    "x_axis": dict(
                tickangle=-45,
                showline=True,
                linewidth=2,
                linecolor="white",
                mirror=True
            ),
    "y_axis": dict(
                range=[0, 100], 
                gridcolor="rgba(255, 255, 255, 0.2)",  # Light grid on dark background
                showline=True,
                linewidth=2,
                linecolor="white",
                mirror=True
            )
}
PLOT_MARKER_COLOR = "rgba(50, 205, 50, 0.9)"  # A nice bright green
PLOT_MARKER_LINE_COLOR = "rgba(0, 128, 0, 1.0)"  # Dark green outline for contrast
PLOT_MARKER_LINE_WIDTH = 2  # Width of the bar outline
PLOT_TEXT_POSITION = "auto"

PROBABILITY_TEXT_STYLE = """font-family:sans-serif; color:{}; font-size: 20px;"""
MISSING_PROBABILITY_TEXT = f"""<b style="{PROBABILITY_TEXT_STYLE.format('Green')}">Do przydzielenia nadal pozostaje {{}}% prawdopodobieństwa.</b>"""
TOTAL_PROBABILITY_TEXT = f"""<b style="{PROBABILITY_TEXT_STYLE.format('Green')}">Przydzielony został całkowity zakres prawdopodobieństwa.</b>"""
EXCEEDING_PROBABILITY_TEXT = f"""<b style="{PROBABILITY_TEXT_STYLE.format('Red')}">Wprowadzone zostało {{}}% prawdopodobieństwa ponad 100%, proszę sprawdzić Państwa odpowiedzi!</b>"""

COST_BENEFIT_QUESTION_TITLE = "Pytanie 11 – Stosunek kosztów do korzyści"
COST_BENEFIT_QUESTION_SUBTITLE = "Stosunek korzyści do kosztów pozwala na porównania kosztów działania lub projektu z korzyściami, jakie przynosi. Na przykład: \n\n- Jeśli program kosztuje 100 000 zł, a wartość pieniężna jego korzyści wynosi 150 000 zł, stosunek korzyści do kosztów wynosiłby 1:1,5. \n- Oznacza to, że na każdą wydaną złotówkę program przynosi półtora złotego korzyści. \n- Wyższy stosunek wskazuje na większą efektywność i opłacalność programu. \n\nBiorąc pod uwagę powyższe wyjaśnienie, chcielibyśmy poznać Państwa opinię: Przy jakim stosunku korzyści do kosztów uznaliby Państwo, że program pilotażowy Digitrans powinien zostać wdrożony na większą skalę? \nProszę wziąć pod uwagę następujące założenia: \n\n- 'Korzyści to efekty zaobserwowane po 2 latach działania programu (obejmujące m.in. dodatkowe przychody i zysk wypracowane przez firmy w Grupie 2 oraz ekwiwalent pieniężny dodatkowych miejsc pracy. \n- 'Koszty obejmują całkowite wydatki poniesione na wdrożenie, funkcjonowanie i utrzymanie programu (w tym koszty administracyjne i ogólne)."

RISK_AVERSION_QUESTION_TITLE = "Pytanie 12 - Niechęć do ryzyka"
RISK_AVERSION_QUESTION_SUBTITLE = "Na zakończenie naszej ankiety chcielibyśmy poznać Państwa ogólną skłonność do podejmowania ryzyka. Informacja ta pomoże nam lepiej zrozumieć kontekst Państwa wcześniejszych odpowiedzi. \nJak oceniają Państwo swoją ogólną skłonność do podejmowania ryzyka na skali od 1 do 10? \n\n- 1 oznacza całkowitą niechęć do podejmowania ryzyka. \n- 10 oznacza pełną gotowość do podejmowania ryzyka."
SLIDER_DESCRIPTION = "Proszę przesunąć suwak, aby wskazać Państwa ocenę."

def sidebar():
    st.sidebar.title(SIDEBAR_TITLE)
    return st.sidebar.radio("", INFORMATION_PAGES + QUESTION_PAGES)

def survey_introduction(config):
    config_header = config["header"]
    st.title(config_header["survey_title"])
    st.write(config_header["survey_description"])

def consent_form():
    # Auxiliary function to change session state on_click
    def add_consent():
        st.session_state["consent"] = True

    # Ask and act on consent given
    st.markdown(CONSENT_TITLE)
    is_consent = st.button(CONSENT_SENTENCE, on_click = add_consent)
    if is_consent:
        st.markdown(CONSENT_SUCCESS)

def get_professional_category_index(professional_category_string):
    # Used to return a default value in case of no value inserted
    try:
        return PROFESSIONAL_CATEGORY_OPTIONS.index(professional_category_string)
    except ValueError:
        return 0

def personal_information():
    st.subheader(PERSONAL_INFORMATION_PAGE_TITLE)
    col1, _ = st.columns(2)
    with col1:
        name = st.text_input(PERSONAL_INFORMATION_CONFIG["user_full_name"], value=st.session_state.get("user_full_name"))
        work = st.text_input(PERSONAL_INFORMATION_CONFIG["user_position"], value=st.session_state.get("user_position"))
        profession = st.radio(PERSONAL_INFORMATION_CONFIG["user_professional_category"], 
                              PROFESSIONAL_CATEGORY_OPTIONS, index = get_professional_category_index(safe_var("professional_category")))
        experience = st.text_input(PERSONAL_INFORMATION_CONFIG["user_years_of_experience"], value=st.session_state.get("years_of_experience"))

        save_input_to_session_state("user_full_name", name)
        save_input_to_session_state("user_position", work)
        save_input_to_session_state("professional_category", profession)
        save_input_to_session_state("years_of_experience", experience) 

def get_distribution_graph(labels_column, values_column, label_column_title, value_column_title):
    figure = go.Figure()

    figure.add_trace(go.Bar(
        x=labels_column, 
        y=values_column, 
        marker_color= PLOT_MARKER_COLOR,
        marker_line_color= PLOT_MARKER_LINE_COLOR,
        marker_line_width= PLOT_MARKER_LINE_WIDTH,
        text=[f"{p}" for p in values_column],  # Adding percentage labels to bars
        textposition= PLOT_TEXT_POSITION,
        name=value_column_title
    ))

    figure.update_layout(
        title= PLOT_CONFIG["title"],
        xaxis_title=label_column_title,
        yaxis_title=value_column_title,
        xaxis=PLOT_CONFIG["x_axis"],
        yaxis=PLOT_CONFIG["y_axis"],
        font=dict(color="white"),  # White font color for readability
    )
    
    return figure

def instructions():
    st.subheader(INSTRUCTIONS_TITLE)
    st.write(INSTRUCTIONS_SUBTITLE)

    st.subheader(INSTRUCTION_TABLE_TITLE)
    st.write(INSTRUCTION_TABLE_SUBTITLE)

    label_column_title = "Temperatury"
    value_column_title = "Prawdopodobieństwo (%)"

    # Generate sample labels and values
    labels_column = ["< 15"] + [str(x) for x in range(16, 25)] + ["> 25"]
    values_column = [0 for _ in labels_column]
    values_column[4:9] = [5, 15, 45, 20, 15]
    values_df = pd.DataFrame({label_column_title: labels_column, value_column_title: values_column})
    
    # Split page into two columns (table, plot)
    table_column, plot_column = st.columns([0.3, 0.7], gap = "large")
       
    with table_column:
        st.data_editor(values_df, use_container_width=True, hide_index=True, disabled=(label_column_title, value_column_title))

    with plot_column:
        fig = get_distribution_graph(labels_column, values_df[value_column_title], label_column_title, value_column_title)
        st.plotly_chart(fig)

    st.write(INSTRUCTIONS_CAPTION)

def generate_question_x_axis(config):
    minor_value = str(config['minor_value'])
    major_value = str(config['major_value'])
    
    min_value = config['min_value_graph']
    max_value = config['max_value_graph']
    interval = config['step_size_graph']

    # Create a list of ranges based on the provided values
    x_axis = [minor_value] + [f"{round(i, 1)}% do {round((i + interval - 0.01), 2)}%" for i in np.arange(min_value, max_value, interval)] + [major_value]

    # TODO find a way to remove it
    if config['min_value_graph'] == -1:
        x_axis.insert(6, "0%")
        x_axis[1] = '-0.99% to -0.81%'
        x_axis[7] = '0.01% to 0.19%'
    elif config['min_value_graph'] == -30:
        x_axis.insert(7, "0%")
        x_axis[8] = '0.01% to 4.99%'
    elif config['min_value_graph'] == -15:
        x_axis.insert(4, "0%")
        x_axis[5] = '0.01% to 4.99%'
    
    return x_axis

def percentage_difference_warning(percentage_difference):
    # Show text (and warnings) based on missing/exceeding probability
    if percentage_difference > 0:
        st.markdown(MISSING_PROBABILITY_TEXT.format(percentage_difference), unsafe_allow_html=True)
    elif percentage_difference == 0:
        st.markdown(TOTAL_PROBABILITY_TEXT, unsafe_allow_html=True)
    else:
        st.markdown(EXCEEDING_PROBABILITY_TEXT.format(abs(percentage_difference)), unsafe_allow_html=True)

def table_and_plot(dataframe_name, changes_name, label_column, value_column, plot_key):
    # Split page into two columns (table, plot)
    table_column, plot_column = st.columns([0.3, 0.7], gap = "large")

    with table_column:
        bins_grid = st.data_editor(st.session_state[dataframe_name], hide_index=True, use_container_width=True, disabled=[label_column], \
                                   key=changes_name, on_change=update_dataframe_session_state, args=(changes_name, dataframe_name))
        percentage_difference = 100 - sum(bins_grid[value_column])
        percentage_difference_warning(percentage_difference)
                    
    with plot_column:
        fig = get_distribution_graph(bins_grid[label_column], bins_grid[value_column], "Oczekiwane prawdopodobieństwa", "Prawdopodobieństwo (%)")
        st.plotly_chart(fig, key=plot_key)


def create_question(config):
    st.subheader(config['title_question'])
    st.write(config['subtitle_question'])

    x_axis = generate_question_x_axis(config)
    y_axis = np.zeros(len(x_axis))

    dataframe_name = config["session_state_dataframe_name"]
    changes_name = config["session_state_changes_name"]
    label_column = config['label_column']
    value_column = config['value_column']
    plot_key_1 = config['plot_key_1']

    if dataframe_name not in st.session_state:
        st.session_state[dataframe_name] = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[label_column, value_column])
    
    table_and_plot(dataframe_name, changes_name, label_column, value_column, plot_key_1)

def double_question(config):
    st.subheader(config['title_question'])
    st.write(config['subtitle_question'])

    x_axis = generate_question_x_axis(config)
    y_axis = np.zeros(len(x_axis))

    dataframe_name_1 = config["session_state_dataframe_name_1"]
    changes_name_1 = config["session_state_changes_name_1"]
    dataframe_name_2 = config["session_state_dataframe_name_2"]
    changes_name_2 = config["session_state_changes_name_2"]
    label_column = config['label_column']
    value_column = config['value_column']
    plot_key_1 = config['plot_key_1']
    plot_key_2 = config['plot_key_2']

    if dataframe_name_1 not in st.session_state:
        st.session_state[dataframe_name_1] = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[label_column, value_column])

    if dataframe_name_2 not in st.session_state:
        st.session_state[dataframe_name_2] = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[label_column, value_column])

    st.markdown("- In comparison to GROUP 1 that receives Financial Subsidy only.")

    table_and_plot(dataframe_name_1, changes_name_1, label_column, value_column, plot_key_1)

    st.markdown("- In comparison to GROUP 3 that receives Benchmarking Report.")

    table_and_plot(dataframe_name_2, changes_name_2, label_column, value_column, plot_key_2)

def cost_benefit_question():
    st.subheader(COST_BENEFIT_QUESTION_TITLE)
    st.write(COST_BENEFIT_QUESTION_SUBTITLE)
    col1, _ = st.columns(2)
    with col1:
        cost_benefit_list = [f"1:{round(i, 1)}" for i in np.arange(0.6, 3.1, .2)]
        cost_benefit_question = st.select_slider(SLIDER_DESCRIPTION, cost_benefit_list, value=st.session_state.get('cost_benefit_question', min(cost_benefit_list)))
        save_input_to_session_state('cost_benefit_question', cost_benefit_question) 

def risk_aversion_question():
    st.subheader(RISK_AVERSION_QUESTION_TITLE)
    st.write(RISK_AVERSION_QUESTION_SUBTITLE)

    col1, _ = st.columns(2)
    with col1:
        risk_aversion_question =st.slider(SLIDER_DESCRIPTION, 1, 10, key="risk_aversion", value=st.session_state.get('risk_aversion_question', 0))
        save_input_to_session_state('risk_aversion_question', risk_aversion_question)

