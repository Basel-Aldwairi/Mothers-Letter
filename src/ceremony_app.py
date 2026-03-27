import streamlit as st
import pymongo
import os
from dotenv import load_dotenv
import base64
import time
from config import *


st.set_page_config(page_title='Grand Ceremony', layout='wide', page_icon='🌸')


def set_styling(img_file):
    with open(img_file, 'rb') as f:
        img_encoded = base64.b64encode(f.read()).decode()

    style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Glassmorphism Card */
        .poem-card {{
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(15px);         
            -webkit-backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            color: #333333;
            min-height: 250px;
            font-family: 'Source Sans Pro', sans-serif;
        }}

        .poem-header {{
            color: #FF5C77;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 15px;
        }}

        .poem-content {{
            font-size: 1.1rem;
            line-height: 1.4;
            white-space: pre-line; /* Keeps the poem line breaks without #### */
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


@st.cache_resource
def initialize_db():
    load_dotenv()
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    return client[os.getenv('MONGO_DB')][os.getenv('MONGO_COLLECTION')]


db_collection = initialize_db()

img_path = os.path.join(os.path.dirname(__file__), '..', 'data', BACKGROUND_IMAGE,)
set_styling(img_path)

st.title("Mother's Day Poems Gallery")

responses = list(db_collection.find().sort('timestamp', -1))

if responses:
    num_cols = 3
    res_list = list(responses)

    for i in range(0, len(res_list), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(res_list):
                res = res_list[i + j]
                clean_poem = res['respose'].replace('#', '').replace('`', '').strip()

                with cols[j]:
                    st.markdown(f"""
                        <div class="poem-card">
                            <div class="poem-header">For {res['name']}</div>
                            <div class="poem-content">{clean_poem}</div>
                            <div style="font-size: 0.8rem; color: #666; margin-top: 15px;">
                                {res['timestamp'].strftime('%H:%M | %d-%m-%Y ')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)


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




time.sleep(10)
st.rerun()