import streamlit as st
import pymongo
import os
from dotenv import load_dotenv
import base64
from config import *
import time

st.set_page_config(
    page_title='Mother\'s Day Poem Lists',
    layout='centered',
    page_icon='🌸',
    initial_sidebar_state='collapsed',
)

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

img_path = os.path.join(os.path.dirname(__file__), '..', 'data', BACKGROUND_IMAGE, )
set_bg(img_path)

def rerun(wait_time = 1):
    start_time = time.time()
    while True:
        waiting_time = time.time() - start_time
        # print(waiting_time)
        if waiting_time > wait_time:
            print('restarting')
            st.rerun()


@st.cache_resource
def initialize_db():
    load_dotenv()
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('MONGO_DB')]
    collection = db[os.getenv('MONGO_COLLECTION')]
    return collection


def get_responses():
    collection = st.session_state['collection']
    all_responses = list(collection.find().sort('timestamp', -1))
    return all_responses


if 'collection' not in st.session_state:
    st.session_state['collection'] = initialize_db()

responses = get_responses()

if not responses:
    st.info('Waiting for first poem...')

else:
    for response in responses:
        with st.container():
            st.markdown(f'### for {response['name']}')
            st.markdown(response['respose'])
            st.divider()


rerun()