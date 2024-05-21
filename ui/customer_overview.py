import streamlit as st
import pandas as pd
import plotly.express as px
from ui.templates import display_centered_header, display_metric, display_pie_chart_header

def display_customer_information(
    customer_info,
    first_order_date,
    first_order_relative_humanized,
    most_recent_order_date,
    most_recent_order_relative_humanized,
):
    """Display the customer information section."""
    display_centered_header('🧑‍🤝‍🧑 Customer Information')
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**📛 Name:** {customer_info['Name']}")
        st.write(f"**📞 Phone:** {customer_info['Phone']}")
    with col2:
        st.write(f"**🗓️ First Order Date:** {first_order_date} ({first_order_relative_humanized})")
        st.write(f"**🗓️ Most Recent Order Date:** {most_recent_order_date} ({most_recent_order_relative_humanized})")

    st.markdown('---')

def display_summary_statistics(sales_history, total_spent):
    """Display summary statistics of the customer's purchase history."""
    display_centered_header('📊 Summary Statistics')
    col1, col2, col3, col4 = st.columns(4)
    total_orders = len(sales_history['OrderID'].unique())
    avg_order_value = total_spent / total_orders if total_orders > 0 else 0
    avg_items_per_order = sales_history['Quantity'].mean()
    with col1:
        st.metric(label='💵 Total Spent', value=f"${total_spent:.2f}")
    with col2:
        st.metric(label='📦 Total Orders', value=total_orders)
    with col3:
        st.metric(label='📈 Avg Order Value', value=f"${avg_order_value:.2f}")
    with col4:
        st.metric(label='📊 Avg Items per Order', value=f"{avg_items_per_order:.2f}")

def display_spending_charts(sales_history):
    """Display pie charts for the customer's spending by category and sales channel."""
    display_centered_header('💸 Spending Breakdown')
    col1, col2, col3, col4, col5 = st.columns([1,9,1,9,1])

    with col2:
        create_spending_pie_chart(sales_history, 'Category', "By Category")

    with col4:
        create_spending_pie_chart(sales_history, 'SalesChannel', "By Sales Channel")

def create_spending_pie_chart(sales_history, group_by_column, header_text):
    """Create and display a pie chart for the specified grouping."""
    display_pie_chart_header(header_text)
    spending_data = sales_history.groupby(group_by_column)['TotalItemPrice'].sum().reset_index()
    fig_pie = px.pie(spending_data, values='TotalItemPrice', names=group_by_column)
    fig_pie.update_layout(height=200, margin=dict(r=20, l=20, t=5, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

def display_orders_over_time(sales_history):
    """Display a bar chart of the customer's orders over time."""
    display_centered_header('📅 Orders Over Time')
    orders_over_time = sales_history.groupby(pd.Grouper(key='OrderDate', freq='ME')).size().reset_index(name='Orders')
    fig_bar = px.bar(orders_over_time, x='OrderDate', y='Orders')
    fig_bar.update_layout(
        height=280, 
        margin=dict(r=10, l=10, t=0, b=5), 
        xaxis_title=None, 
        yaxis_title=None
    )
    st.plotly_chart(fig_bar, use_container_width=True)
