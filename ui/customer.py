import streamlit as st
from core.query_database import get_customer_sales_history
import pandas as pd
from datetime import datetime
import humanize
from ui.customer_overview import display_customer_information, display_summary_statistics, display_spending_charts, display_orders_over_time
from ui.customer_history import display_purchase_history

@st.experimental_dialog("Customer Information", width="large")
def display_customer_info(customer_id):
    """Display detailed customer information and purchase history."""
    sales_history, total_spent, first_order_date, most_recent_order_date = get_customer_sales_history(customer_id)
    customer_info = st.session_state['customers_data'].loc[st.session_state['customers_data']['CustomerID'] == customer_id].iloc[0]
    
    sales_history['OrderDate'] = pd.to_datetime(sales_history['OrderDate'])

    first_order_relative_humanized = humanize.naturaltime(datetime.now() - pd.to_datetime(first_order_date))
    most_recent_order_relative_humanized = humanize.naturaltime(datetime.now() - pd.to_datetime(most_recent_order_date))

    tabs = st.tabs(['📊 Overview', '💸 Spending Breakdown', '📅 Orders Over Time', '🧾 Purchase History'])
    
    with tabs[0]:
        display_customer_information(
            customer_info,
            first_order_date,
            first_order_relative_humanized,
            most_recent_order_date,
            most_recent_order_relative_humanized,
        )
        display_summary_statistics(sales_history, total_spent)
    
    with tabs[1]:
        display_spending_charts(sales_history)

    with tabs[2]:
        display_orders_over_time(sales_history)

    with tabs[3]:
        display_purchase_history(sales_history)

    if st.button('Close'):
        st.session_state['selected_customer_id'] = None
        st.rerun()
