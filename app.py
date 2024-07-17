import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
from dashboard import dashboard_page

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Define a function to get Firestore database
def get_db():
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="vextera-test")
    return db

def validate_user(username, password, _db):
    # Create a reference to the document with the username
    doc_ref = _db.collection("users").document(username)
    doc = doc_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        if user_data["password"] == password:
            return True
    return False

def main():
    db = get_db()

    if st.session_state.logged_in:
        dashboard_page()
    else:
        # Streamlit login form
        st.title("Login Form")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if validate_user(username, password, db):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
                
            else:
                st.error("Invalid username or password")

if __name__ == '__main__':
    main()
