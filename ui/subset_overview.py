import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ui.templates import display_centered_header, display_metric, display_pie_chart_header

def display_overview_charts(total_customers, num_selected_customers, total_sales, subset_sales, sales_history):
    """Display the overview charts of the customer subset with metrics and 100% stacked bar charts."""
    fig1 = create_customers_bar_chart(total_customers, num_selected_customers)
    fig2 = create_sales_bar_chart(total_sales, subset_sales)
    fig3 = create_orders_bar_chart(sales_history)
    
    display_centered_header('📊 Subset Overview')
    col1, col2, col3 = st.columns(3)

    with col1:
        display_metric("👥 Customers", num_selected_customers, total_customers)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        display_metric("💵 Sales", f"${subset_sales:,.0f}", f"${total_sales:,.0f}")
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        total_orders = st.session_state.get('total_orders', 0)
        subset_orders = len(sales_history['OrderID'].unique())
        display_metric("📦 Orders", subset_orders, total_orders)
        st.plotly_chart(fig3, use_container_width=True)

def create_stacked_bar_chart(x_label, total_value, subset_value, total_label, subset_label):
    """Create a 100% stacked vertical bar chart with percentage labels."""
    total_percent = (subset_value / total_value) * 100

    fig = go.Figure(data=[
        go.Bar(name=subset_label, x=[x_label], y=[subset_value], marker_color='dodgerblue'),
        go.Bar(name=total_label, x=[x_label], y=[total_value - subset_value], marker_color='lightgrey')
    ])
    fig.update_layout(
        barmode='stack', 
        yaxis={'categoryorder': 'total descending'}, 
        showlegend=False,
        height=180,
        margin=dict(l=40, r=40, t=0, b=5)
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    # Add annotation for the subset percentage
    fig.add_annotation(x=x_label, y=subset_value / 2, text=f"{total_percent:.1f}%",
                       showarrow=False, font=dict(color='white', size=12))

    return fig

def create_customers_bar_chart(total_customers, num_selected_customers):
    """Create a 100% stacked vertical bar chart showing the proportion of selected customers."""
    return create_stacked_bar_chart('👥 Customers', total_customers, num_selected_customers, 'Other Customers', 'Selected Customers')

def create_sales_bar_chart(total_sales, subset_sales):
    """Create a 100% stacked vertical bar chart showing the proportion of subset sales."""
    return create_stacked_bar_chart('Sales', total_sales, subset_sales, 'Other Sales', 'Subset Sales')

def create_orders_bar_chart(sales_history):
    """Create a 100% stacked vertical bar chart showing the proportion of subset orders."""
    total_orders = st.session_state.get('total_orders', 0)
    subset_orders = len(sales_history['OrderID'].unique())
    return create_stacked_bar_chart('🛍️ Orders', total_orders, subset_orders, 'Other Orders', 'Subset Orders')

def display_summary_statistics(sales_history, total_spent):
    """Display summary statistics of the subset's purchase history."""
    col1, col2, col3, col4, col5 = st.columns([1,1.5,1,1.5,1])
    total_orders = len(sales_history['OrderID'].unique())
    avg_order_value = total_spent / total_orders if total_orders > 0 else 0
    
    total_quantity = sales_history['Quantity'].sum()
    avg_items_per_order = total_quantity / total_orders if total_orders > 0 else 0
    
    total_avg_order_value = st.session_state.get('avg_order_value', 0)
    total_avg_items_per_order = st.session_state.get('avg_items_per_order', 0)
    
    with col2:
        st.metric(label='Avg Order Value', value=f"${avg_order_value:.2f}", delta=f"{avg_order_value - total_avg_order_value:.2f}")
    with col4:
        st.metric(label='Avg Items per Order', value=f"{avg_items_per_order:.2f}", delta=f"{avg_items_per_order - total_avg_items_per_order:.2f}")

def display_spending_charts(sales_history):
    """Display pie charts for the subset's spending by category and sales channel."""
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
    fig_pie.update_layout(height=180, margin=dict(r=10, l=10, t=0, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

def display_orders_over_time(sales_history):
    """Display a bar chart of the subset's orders over time."""
    display_centered_header('📅 Orders Over Time')
    orders_over_time = sales_history.groupby(pd.Grouper(key='OrderDate', freq='ME')).size().reset_index(name='Orders')
    fig_bar = px.bar(orders_over_time, x='OrderDate', y='Orders')
    fig_bar.update_layout(
        height=250, 
        margin=dict(r=10, l=10, t=0, b=5), 
        xaxis_title=None, 
        yaxis_title=None
    )
    st.plotly_chart(fig_bar, use_container_width=True)
