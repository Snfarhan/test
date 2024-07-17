import streamlit as st
import pandas as pd
import json
import duckdb as duck
from streamlit_option_menu import option_menu  # Import the correct function or class
from google.cloud import firestore
from google.oauth2 import service_account

def get_db():
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="vextera-test")
    return db

# Define a function to fetch user data from Firestore
@st.cache_data
def get_user_data(username, _db):
    # Fetch data specific to the user from the 'amazon' collection
    user_data_ref = _db.collection("amazon").where("users", "==", username)
    docs = user_data_ref.stream()
    user_data = [doc.to_dict() for doc in docs]
    user_data_df = pd.DataFrame(user_data)
    
    # Log the query and results
    if user_data_df.empty:
        st.write(f"No documents found for user: {username}")
    
    return user_data_df

# Dashboard page function
def dashboard_page():
    # Sidebar navigation
    st.sidebar.header(f"Hello, {st.session_state['username']}!")
    with st.sidebar:
        selected = option_menu(None, ["Dashboard", "Amazon"], 
                               icons=['house-door-fill'],
                               orientation="vertical",
                               styles={"container": {"background-color": "#282434"}})
        
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()
    
    # Main content based on selected option
    if selected == "Dashboard":
        st.title('Dashboard')
        st.text('Below is the analysis from noon, amazon and shopify platform')
        st.divider()
        
        st.title(f"Dashboard")
        db = get_db()
        user_data = get_user_data(st.session_state.username, db)
        
        st.write("data available.")
        query2 = duck.sql("select date,ordered_product_sales,units_ordered from user_data ").df()
        st.write(query2) 
      
            
        st.divider()
    
    elif selected == "Amazon":
        from amazon import amazon_page  # Import inside function for better control
        amazon_page()  # Call the function directly
