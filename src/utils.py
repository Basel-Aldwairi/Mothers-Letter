import base64
import streamlit as st
import time
from dotenv import load_dotenv
import os
import pymongo

def read_base64(img_file):
    with open(img_file, 'rb') as f:
        img_data = f.read()
    return base64.b64encode(img_data).decode()


def set_bg(img_file):
    img_encoded = read_base64(img_file)

    style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_encoded}");
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


def footing():
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


def remove_bar():
    st.markdown("""
        <style>
        /* 1. Hide the background and border of the top header */
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0) !important;
            border-bottom: none !important;
        }

        /* 2. Hide the 'Deploy' button and the 'Hamburger' menu (the 3 dots) */
        [data-testid="stAppDeploy"], #MainMenu {
            visibility: hidden !important;
        }

        /* 3. Pull the main content up to fill the gap */
        .block-container {
            padding-top: 2rem !important;
        }

        /* 4. OPTIONAL: Customize the Sidebar's appearance to match your theme */
        [data-testid="stSidebar"] {
            background-color: #F3CFC6 !important; /* Your secondaryBackgroundColor */
            border-right: 1px solid #FF8A9D;
        }

        /* Change the color of the sidebar text and labels */
        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
            color: #333333 !important;
        }
        </style>
        """, unsafe_allow_html=True)


def logo_title(text, img_path):
    logo_base64 = read_base64(img_path)

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="100" style="vertical-align: middle;">
            <h1 style="margin: 0; color: #333333; font-family: 'Source Sans Pro', sans-serif;">
                {text}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def get_secret(key):
    try:
        # This only works if secrets are actually set up
        return st.secrets.get(key)
    except (FileNotFoundError, KeyError, Exception):
        # Fallback if secrets aren't initialized
        return None

def connect_atlas():
    load_dotenv()

    # 2. Priority: Check Streamlit Secrets (Cloud), then Environment (Local)
    # Streamlit Cloud looks at 'secrets' first
    mongo_uri = get_secret("ATLASDB_URI") or os.getenv("ATLASDB_URI")
    db_name = get_secret("MONGO_DB") or os.getenv("MONGO_DB", "mothers_day_db")
    coll_name = get_secret("MONGO_COLLECTION") or os.getenv("MONGO_COLLECTION", "poems")

    if not mongo_uri:
        st.error("MongoDB URI not found! Check your Secrets/Env.")
        return None

    try:
        # 3. Connect with a timeout so it doesn't hang forever if the Wi-Fi is down
        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Trigger a quick check to see if the connection is actually alive
        client.admin.command('ping')

        db = client[db_name]
        return db[coll_name]

    except Exception as e:
        st.error(f"Database Connection Failed: {e}")
        return None