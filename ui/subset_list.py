import streamlit as st
from ui.customer import display_customer_info

def display_customer_list(customers_data):
    """Display the list of customers with a name filter and buttons to show details."""
    with st.container(height=330):
        filtered_customers = get_filtered_customers(customers_data)

        # Display the filtered list of customers with buttons to show details
        cols = st.columns(3)  # Create three columns for displaying customer names

        for index, row in filtered_customers.iterrows():
            col_index = index % 3  # Determine the column to place the button in
            with cols[col_index]:
                if st.button(f"{row['Name']}", key=f"{row['CustomerID']}_{index}", use_container_width=True):
                    st.session_state['selected_customer_id'] = row['CustomerID']
                    display_customer_info(row['CustomerID'])

def get_filtered_customers(customers_data):
    """Display a text input for the name filter and return the filtered customers."""
    col1, col2, col3 = st.columns([1,5,1])
    with col2:
        name_filter = st.text_input('Filter by name:')
        if name_filter:
            return customers_data[customers_data['Name'].str.contains(name_filter, case=False, na=False)]
        return customers_data
