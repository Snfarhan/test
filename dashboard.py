import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu  # Import the correct function or class

# Define a function to fetch user data from Firestore
@st.cache_data
def get_user_data(username, _db):
    # Fetch data specific to the user from the 'amazon' collection
    user_data_ref = _db.collection("amazon").where("users", "==", username)
    docs = user_data_ref.stream()
    user_data = [doc.df() for doc in docs]
    print(user_data)
    u_data = pd.DataFrame(user_data)
    print(u_data)
    
    # Log the query and results
    if not user_data:
        st.write(f"No documents found for user: {username}")
    
    return user_data

# Dashboard page function
def dashboard_page(db):
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
        user_data = get_user_data(st.session_state.username, db)
        
        if user_data:
            st.dataframe(user_data)
        else:
            st.write("No data available for the user.")
            
        st.divider()
    
    elif selected == "Amazon":
        from amazon import amazon_page  # Import inside function for better control
        amazon_page()  # Call the function directly
