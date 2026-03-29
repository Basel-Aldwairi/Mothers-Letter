import streamlit as st
import pymongo
import os
from dotenv import load_dotenv
from configs import *
from PIL import Image
from utils import *

logo_img_path = os.path.join(os.path.dirname(__file__), '..', 'data', LOGO_IMAGE, )
logo_img = Image.open(logo_img_path)

st.set_page_config(page_title='Grand Ceremony', layout='wide', page_icon=logo_img)


@st.cache_resource
def initialize_db():
    return connect_atlas()


remove_bar()

db_collection = initialize_db()

img_path = os.path.join(os.path.dirname(__file__), '..', 'data', BACKGROUND_IMAGE, )
set_styling(img_path)

logo_title('Mother\'s Day Poems Gallery', logo_img_path)

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

footing()

time.sleep(10)
st.rerun()
