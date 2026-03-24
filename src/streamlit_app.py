import base64
import io
import os

import streamlit as st
import prompt_generator
from google import genai
from dotenv import load_dotenv
from PIL import Image
import time

def set_bg(img_file):
    with open(img_file, 'rb') as f:
        img_data = f.read()
    img_encoded = base64.b64encode(img_data)

    style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/archive;base64,{img_encoded.decode()}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """

    st.markdown(style, unsafe_allow_html=True)


def text_animation(text, speed=0.01):
    placeholder = st.empty()
    typed = ''
    for c in text:
        typed += c
        placeholder.markdown(
            f"{typed}",
            unsafe_allow_html=True
        )
        time.sleep(speed)


st.set_page_config(
    page_title='Mother\'s Day Poem',
    layout='centered',
    page_icon='🌸'
)


@st.cache_resource
def initialize_client():
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=gemini_api_key)
    return client


if 'client' not in st.session_state:
    st.session_state['client'] = initialize_client()
if 'generate_button_clicked' not in st.session_state:
    st.session_state['generate_button_clicked'] = False
if 'response_exists' not in st.session_state:
    st.session_state['response_exists'] = False
if 'response_written' not in st.session_state:
    st.session_state['response_written'] = False
if 'response' not in st.session_state:
    st.session_state['response'] = None

img_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'letter.jpg', )
set_bg(img_path)

st.title('Mother\'s Day Poem')

name = st.text_input('Mother\'s Name')

traits_list = ['Loving',
               'Adoring',
               'Flower Lover',
               'Great Cook',
               'Caring',
               'Book Worm',
               'Adventurous',
               'Patient',
               'Emotionally Supportive',
               'Selfless',
               'Role Model',
               'Inspiring']

selected_trait = st.multiselect('Select Trait', traits_list)

custom_traits_string = st.text_input('Custom Traits (comma separated)')
custom_traits = [trait.title() for trait in custom_traits_string.split(',')]

poem_length = st.sidebar.slider('Poem Length', min_value=2, max_value=10, value=(4, 8))

languages = ['English',
             'Arabic',
             'German']
selected_language = st.sidebar.selectbox('Select Language', languages, index=0)

generate_button = st.button('Generate Poem')

if generate_button:
    st.session_state['generate_button_clicked'] = True

if st.session_state['generate_button_clicked']:
    all_traits = selected_trait + custom_traits if custom_traits else []

    if name != '':
        all_traits.append('NAME == ' + name)

    if len(all_traits) > 0:
        prompt = prompt_generator.create_prompt_poem(all_traits, poem_length=poem_length, language=selected_language)

        st.session_state['response'] = st.session_state['client'].models.generate_content(model='gemini-3-flash-preview',
                                                                      contents=prompt).text
        st.session_state['response_exists'] = True
        st.session_state['response_written'] = False


    else:
        st.session_state['generate_button_clicked'] = False
        st.session_state['response_exists'] = False


if st.session_state['response_exists']:
    response = st.session_state['response']
    if not st.session_state['response_written']:
        text_animation(response)
        st.session_state['response_written'] = True
    else:
        st.markdown(response)
