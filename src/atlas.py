from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def get_secret(key, default=None):
    try:
        # This only works if secrets are actually set up
        return st.secrets.get(key)
    except (FileNotFoundError, KeyError, Exception):
        # Fallback if secrets aren't initialized
        return None

# Now use it in your connection logic
mongo_uri = get_secret("ATLASDB_URI") or os.getenv("ATLASDB_URI")
# print(mongo_uri)

# uri = os.getenv('MONGO_URI')
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)