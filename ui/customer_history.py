import streamlit as st
from datetime import datetime
import humanize
from ui.templates import display_table_header

def display_purchase_history(sales_history):
    """Display the purchase history tab with detailed order information."""
    orders = sales_history.groupby('OrderID')
    for order_id, order_data in orders:
        with st.container(border=True):
            display_order_header(order_data)
            display_order_metrics(order_data)
            display_order_items(order_data)

def display_order_header(order_data):
    """Display the order date and relative time."""
    order_date = order_data['OrderDate'].iloc[0]
    order_date_formatted = order_date.strftime('%A, %B %d, %Y')
    order_date_relative = humanize.naturaltime(datetime.now() - order_date)

    st.html(f"""
        <div style="text-align: center; font-size: 14px; margin-bottom: 10px;">
            🗓️ Order Date
            &nbsp;&nbsp;
            <strong style="font-size: 20px;">{order_date_formatted}</strong>
            &nbsp;
            <span style="font-style: italic;">({order_date_relative})</span>
        </div>
    """)

def display_order_metrics(order_data):
    """Display sales channel, total amount, and items purchased."""
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3,9,1,9,1,9,3])
    with col2:
        st.metric(label='🛍️ Sales Channel', value=order_data['SalesChannel'].iloc[0])
    with col4:
        st.metric(label='💵 Total Amount', value=f"${order_data['TotalAmount'].iloc[0]:.2f}")
    with col6:
        st.metric(label='📦 Items Purchased', value=order_data['Quantity'].sum())

def display_order_items(order_data):
    """Display the items in the order."""
    display_table_header("🛒 Order Items")
    order_items = order_data[['Description', 'Category', 'Quantity', 'UnitPrice', 'TotalItemPrice']]
    st.dataframe(order_items, use_container_width=True)
