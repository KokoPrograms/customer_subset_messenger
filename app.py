import streamlit as st
import pandas as pd
from core.query_database import query_database, calculate_subset_sales, get_subset_sales_history
from core.default_input import default_promotion_message_template, default_sql_query, default_sql_explanation
from ui.layout import display_sidebar, display_main_layout
from core.setup_database import setup_database

def initialize_session_state():
    """Initialize the Streamlit session state with default values."""
    st.session_state.setdefault('promotion_message_template', default_promotion_message_template)
    st.session_state.setdefault('sql_query', default_sql_query)
    st.session_state.setdefault('sql_explanation', default_sql_explanation)

def load_initial_data():
    """Load initial data into the session state."""
    st.session_state['customers_data'] = query_database(st.session_state['sql_query'])
    st.session_state['subset_sales'] = calculate_subset_sales(st.session_state['customers_data'])
    st.session_state['sales_history'] = get_subset_sales_history(st.session_state['customers_data'])

def run_main_app():
    """Run the main Streamlit application."""
    st.title('🎯 Targeted Marketing Messenger')
    st.write("Enhance your marketing efforts by precisely segmenting customers and crafting tailored promotional messages with our intuitive tool.")
    
    display_sidebar()

    if 'customers_data' not in st.session_state or st.session_state['customers_data'].empty:
        load_initial_data()

    if st.session_state.get('sql_query_updated', False):
        customers_data = query_database(st.session_state['sql_query'])
        if customers_data.empty:
            st.session_state['customers_data'] = pd.DataFrame()
            st.session_state['subset_sales'] = 0
            st.session_state['sales_history'] = pd.DataFrame()
        else:
            st.session_state['customers_data'] = customers_data
            st.session_state['subset_sales'] = calculate_subset_sales(st.session_state['customers_data'])
            st.session_state['sales_history'] = get_subset_sales_history(st.session_state['customers_data'])
        st.session_state['sql_query_updated'] = False

    display_main_layout(st.session_state['customers_data'])

st.set_page_config(page_title="Targeted Marketing Messenger")
setup_database()
initialize_session_state()
run_main_app()
