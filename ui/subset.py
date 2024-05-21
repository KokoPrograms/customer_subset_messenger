import streamlit as st
from ui.subset_overview import display_overview_charts, display_spending_charts, display_orders_over_time
from ui.subset_list import display_customer_list
from core.llm import handle_subset_criteria
from ui.templates import display_section_header, display_total_customers_header, display_user_input
from core.default_input import default_subset_criteria, default_sql_explanation

@st.experimental_fragment
def display_customer_subset(customers_data, total_sales, subset_sales, sales_history):
    """Display the customer subset with visualizations and interaction."""
    num_selected_customers = len(customers_data)
    total_customers = st.session_state.get('total_customers', num_selected_customers)

    display_section_header('👥 Customer Subset')
    with st.container(border=True):
        st.html("<style='line-height:0.5;'>")
        display_subset_criteria_input()
        st.html("<style='line-height:0.5;'>")
        try:
            display_subset_data(num_selected_customers, customers_data, total_customers, total_sales, subset_sales, sales_history)
        except Exception as e:
            st.error(f"An error occurred while displaying the subset data: {e}")
        st.html("<style='line-height:0.5;'>")

def display_subset_criteria_input():
    """Display the subset criteria input and button."""
    result = display_user_input(
        '🔍 Input Subset Criteria:',
        default_subset_criteria,
        '🔍 Find Customers',
        handle_subset_criteria
    )
    if result:
        sql_query, explanation = result
        st.session_state['sql_query'] = sql_query
        st.session_state['sql_explanation'] = explanation or default_sql_explanation
        st.session_state['sql_query_updated'] = True
        st.rerun()

def display_subset_data(num_selected_customers, customers_data, total_customers, total_sales, subset_sales, sales_history):
    """Display the subset data with header and tabs or an error message if no customers are found."""
    with st.container(border=True):
        display_header(num_selected_customers)
        if customers_data.empty:
            st.error("No customers found for this criteria.")
        else:
            display_tabs(customers_data, total_customers, num_selected_customers, total_sales, subset_sales, sales_history)

def display_header(num_selected_customers):
    """Display the header with the number of selected customers."""
    col1, col2 = st.columns([5, 2])
    with col1:
        display_total_customers_header(f'🎯 {num_selected_customers} Selected Customers')
    with col2:
        display_sql_query()

def display_sql_query():
    """Display the SQL query and its explanation used for filtering customers."""
    col1, col2 = st.columns([9, 1])
    with col1:
        with st.popover('✨ SQL Query', use_container_width=True):
            st.markdown("**Query Used:**")
            st.code(st.session_state.get('sql_query', ''), language='sql')
            st.markdown("**Explanation:**")
            with st.container(border=True):
                st.write(st.session_state.get('sql_explanation', ''))

def display_tabs(customers_data, total_customers, num_selected_customers, total_sales, subset_sales, sales_history):
    """Display tabs with the overview and customer list."""
    tabs = st.tabs(['📊 Overview', '💸 Spending Breakdown', '📅 Orders Over Time', '🗂 Customer List'])

    with tabs[0]:
        display_overview_charts(total_customers, num_selected_customers, total_sales, subset_sales, sales_history)

    with tabs[1]:
        display_spending_charts(sales_history)

    with tabs[2]:
        display_orders_over_time(sales_history)

    with tabs[3]:
        display_customer_list(customers_data)
