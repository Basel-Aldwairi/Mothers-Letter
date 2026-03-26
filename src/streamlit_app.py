import base64
import os
import streamlit as st

import prompt_generator
from google import genai
from dotenv import load_dotenv
import time
from config import *
import pymongo
from datetime import datetime
import streamlit.components.v1 as components


def set_bg(img_file):
    with open(img_file, 'rb') as f:
        img_data = f.read()
    img_encoded = base64.b64encode(img_data)

    style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_encoded.decode()}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* --- STREAMLIT BUTTON OVERRIDE --- */
        div.stButton > button:first-child {{
            background-color: #FF5C77 !important; /* Your Primary Color */
            color: #FFFFFF !important;           /* White text */
            border: none !important;
            border-radius: 0.5rem !important;
            padding: 0.5rem 1rem !important;
            transition: background-color 0.3s ease !important;
        }}

        /* Match the darker hover effect */
        div.stButton > button:first-child:hover {{
            background-color: #E04B63 !important; /* Darker version of primary */
            color: #FFFFFF !important;           /* Keep text white */
            border: none !important;
        }}

        /* The 'Active' state when clicked */
        div.stButton > button:first-child:active {{
            background-color: #C13A51 !important;
            color: #FFFFFF !important;
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


def save_poem(name, traits, language, prompt, response):
    data = {
        'name': name,
        'traits': traits,
        'language': language,
        'prompt': prompt,
        'respose': response,
        'timestamp': datetime.now()
    }

    st.session_state['collection'].insert_one(data)


import streamlit.components.v1 as components


def trigger_copy_to_clipboard(text):
    # This renders a tiny, invisible piece of JS that copies then self-destructs
    js_code = f"""
        <script>
        const text = `{text}`;
        navigator.clipboard.writeText(text);
        </script>
    """
    # Use a small height so it doesn't create a gap in your UI
    components.html(js_code, height=0)


def copy_button_component(text):
    clean_text = text.replace('#', '').replace("`", "'").replace('\n ', '\n').strip()

    html_code = f"""
            <div style="display: flex; justify-content: flex-start; padding-left: 0px;">
                <button id="copyBtn" style="
                    background-color: #FF5C77; 
                    color: #FFFFFF;
                    border: none;
                    padding: 0.6rem 1.2rem;
                    border-radius: 0.5rem;
                    cursor: pointer;
                    font-family: 'Source Sans Pro', sans-serif;
                    font-size: 1rem;
                    font-weight: 500;
                    width: fit-content;
                    transition: background-color 0.3s ease;
                    margin-top: 10px;
                ">
                    Copy Poem to Clipboard
                </button>
            </div>

            <script>
            const btn = document.getElementById('copyBtn');
            btn.onmouseover = () => btn.style.backgroundColor = '#E04B63'; 
            btn.onmouseout = () => btn.style.backgroundColor = '#FF5C77'; 

            btn.addEventListener('click', function() {{
                const text = `{clean_text}`;
                navigator.clipboard.writeText(text).then(() => {{
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: true}}, '*');
                }});
            }});
            </script>
        """
    # Keep the height enough to show the button clearly
    return components.html(html_code, height=75)


st.set_page_config(
    page_title='Mother\'s Day Poem',
    layout='centered',
    page_icon='🌸',
    initial_sidebar_state='collapsed',
)


@st.cache_resource
def initialize_client():
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=gemini_api_key)
    return client


@st.cache_resource
def initialize_db():
    load_dotenv()
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('MONGO_DB')]
    collection = db[os.getenv('MONGO_COLLECTION')]
    return collection


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
if 'collection' not in st.session_state:
    st.session_state['collection'] = initialize_db()

img_path = os.path.join(os.path.dirname(__file__), '..', 'data', BACKGROUND_IMAGE, )
set_bg(img_path)

st.title('Mother\'s Day Poem')

name = st.text_input('Mother\'s Name')

traits_list = ['Loving',
               'Adoring',
               'Flower Lover',
               'Nurturing',
               'Wise',
               'Master Chef',
               'Caring',
               'Book Worm',
               'Adventurous',
               'Patient',
               'Traveler',
               'German Speaker',
               'Sarcastic Legend',
               'Emotionally Supportive',
               'Selfless',
               'Role Model',
               'Inspiring',
               'Traveler']


selected_trait = st.multiselect('Select Traits', traits_list, max_selections=5)

custom_traits_string = st.text_input('Custom Traits (comma separated)')
custom_traits = [trait.title() for trait in custom_traits_string.split(',')]

poem_length = st.sidebar.slider('Poem Length', min_value=2, max_value=10, value=(4, 8))

languages = ['English',
             'Arabic',
             'German',
             'Russian']
selected_language = st.sidebar.selectbox('Select Language', languages, index=0)

writing_speed_ms = st.sidebar.slider('Writing Speed in ms', min_value=10, max_value=1000, value=50)
writing_speed_s = writing_speed_ms / 1000

generate_button = st.button('Generate Poem')

if generate_button:
    st.session_state['generate_button_clicked'] = True

if st.session_state['generate_button_clicked']:
    st.session_state['generate_button_clicked'] = False

    all_traits = selected_trait + custom_traits if custom_traits else []

    if name != '':
        all_traits.append('NAME == ' + name)

    if len(all_traits) > 0:
        prompt = prompt_generator.create_prompt_poem(all_traits, poem_length=poem_length, language=selected_language)

        with st.spinner('Generating Poem...'):

            try:
                response = st.session_state['client'].models.generate_content(model=GEMINI_MODEL,
                                                                              contents=prompt).text
                st.session_state['response'] = response
                st.session_state['response_exists'] = True
                st.session_state['response_written'] = False

                save_poem(name, all_traits, selected_language, prompt, response)


            except Exception as e:
                error_text = '''
                #### Error Generating Poem
                #### Try again shortly
                '''
                st.error(error_text)
                st.session_state['response_exists'] = False

                print(e)



    else:
        st.session_state['response_exists'] = False

if st.session_state['response_exists']:
    response = st.session_state['response']
    if not st.session_state['response_written']:
        text_animation(response, writing_speed_s)
        st.session_state['response_written'] = True
    else:
        st.markdown(response)

    copy_button = copy_button_component(response)


st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

st.markdown("---")  # Visual divider
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.5);
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
    <div class="footer">
        Developed by Basel Al-Dwairi | GJU AI Club 
    </div>
    """,
    unsafe_allow_html=True
)
