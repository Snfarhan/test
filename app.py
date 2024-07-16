import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

@st.cache_resource
def get_db():
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="vextera-test")
    return db

def validate_user(username, password, db):
    # Create a reference to the document with the username
    doc_ref = db.collection("users").document(username)
    doc = doc_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        if user_data["password"] == password:
            return True
    return False

# Get Firestore database
db = get_db()

# Streamlit login form
st.title("Login Form")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if validate_user(username, password, db):
        st.success("Login successful!")
    else:
        st.error("Invalid username or password")
