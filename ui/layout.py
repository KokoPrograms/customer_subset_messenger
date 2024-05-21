import streamlit as st
import pandas as pd
from core.setup_database import setup_database
from ui.subset import display_customer_subset
from ui.promotion_message import display_promotion_message

def display_sidebar():
    """Display the sidebar with basci usage information."""

    st.sidebar.markdown("""
        ### About the Dataset

        This dataset is for a fictional Polish food shop and catering company called **Pierogi Party**. Pierogi Party specializes in traditional Polish cuisine, offering a variety of dishes such as `Pierogi`, `Main`, `Soup`, `Side`, `Dessert`, and `Kompot`. The company operates through multiple sales channels, including `Store`, `Market`, and `Catering`.
        
        Use this data to explore customer purchasing behavior, generate targeted marketing messages, and gain insights into sales trends.
    """)

    st.sidebar.markdown('---')

    st.sidebar.markdown("""
        ### Quick Start Guide

        🔍 **Find Customers**
        - Enter criteria to filter customers (e.g., "Spent over $200 in the last 6 months").
        - Click '🔍 Find Customers' to apply the filter.
        - Snowflake's Arctic LLM will generate the SQL query and explain it in plain English for verification.
                        
        📊 **Explore Data**
        - Use the tabs to view customer subsets, spending breakdowns, and order history.
        - Click on a name in the customer list to view individual spending statistics and order history.

        ✉️ **Create Promotional Messages**
        - Input promotional details (e.g., "additional 10% off during happy hour 4-6pm til the end of the month").
        - Click '💬 Generate Message' to draft a message to send to your selected customers.
        - Edit if needed, then click '✅ Send Messages' to finalize.
    """)

    st.sidebar.markdown('---')

    st.sidebar.markdown("""
        ### Searchable Parameters

        **Customer Spending Habits:**
        - `Total Amount Spent`
            - Example: "Spent more than $200."
        - `Average Order Value`
            - Example: "Average order value over $50."

        **Purchase Behavior:**
        - `Product Category`
            - Example: "Bought `Pierogi`."
            - Options: `Pierogi`, `Main`, `Soup`, `Side`, `Dessert`, `Kompot`
        - `Quantity of Items`
            - Example: "Purchased more than 5 items in a single order."
        - `Price per Item`
            - Example: "Bought items priced over $20 each."

        **Sales Channels:**
        - `Sales Channel`
            - Example: "Made purchases through `Market`."
            - Options: `Store`, `Market`, `Catering`

        **Order Timing:**
        - `Recent Orders`
            - Example: "Placed orders in the last month."
        - `Time of Day`
            - Example: "Placed orders during happy hour (4-6 PM)."
        - `Seasonal Trends`
            - Example: "Made orders during the holiday season."
    """)

    if st.sidebar.button('📋 View Menu'):
        show_menu()

@st.experimental_dialog("Menu", width="large")
def show_menu():
    products_df = pd.read_csv('data/products.csv')
    st.dataframe(products_df)

def display_main_layout(customers_data):
    """Display the main layout with customer subset and promotional message."""
    total_sales = st.session_state.get('total_sales', 0)
    subset_sales = st.session_state.get('subset_sales', 0)
    sales_history = st.session_state.get('sales_history', pd.DataFrame())
    
    st.html("<br>")
    display_customer_subset(customers_data, total_sales, subset_sales, sales_history)
    st.html("<br>")
    display_promotion_message()
