import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import json
from google.oauth2 import service_account
from google.cloud import firestore

# Define a function to fetch user data from Firestore
@st.cache_data
def get_user_data(username, _db):
    # Fetch data specific to the user from the 'amazon' collection
    user_data_ref = _db.collection("amazon").where("users", "==", username)
    docs = user_data_ref.stream()
    user_data = [doc.to_dict() for doc in docs]
    
    # Log the query and results
    if not user_data:
        st.write(f"No documents found for user: {username}")
    
    return user_data

def get_db():
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="vextera-test")
    return db

# Dashboard page function
def dashboard_page(db):
    st.sidebar.header(f"Hello, {st.session_state['username']}!")
    with st.sidebar:
        selected = option_menu(None, ["Dashboard"], 
                               icons=['house-door-fill'],
                               orientation="vertical",
                               styles={"container": {"background-color": "#282434"}})
        
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.experimental_rerun()
    
    if selected == "Dashboard":
        st.title('Dashboard')
        st.text('Below is the analysis from noon, amazon and shopify platform')
        st.divider()
        
        user_data = get_user_data(st.session_state.username, db)
        
        if user_data:
            df = pd.DataFrame(user_data)
            st.write(df.dtypes)  # Print data types of the DataFrame columns for debugging
            st.table(df)
        else:
            st.write("No data available for the user.")
            
        st.divider()

# Initialize Firestore and render the dashboard
if "logged_in" in st.session_state and st.session_state.logged_in:
    db = get_db()
    dashboard_page(db)
else:
    st.write("Please log in.")
