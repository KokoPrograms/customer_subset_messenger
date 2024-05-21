import streamlit as st

def display_centered_header(header_text):
    """Display a centered header with the specified text."""
    st.html(f"""
        <div style="text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px;">
            {header_text}
        </div>
    """)

def display_main_header(header_text):
    """Display a centered header with the specified text."""
    st.html(f"""
        <div style="text-align: center; font-size: 48px; font-weight: bold; margin-bottom: 10px;">
            {header_text}
        </div>
    """)

def display_section_header(header_text):
    """Display a centered header with the specified text."""
    st.html(f"""
        <div style="text-align: center; font-size: 36px; font-weight: bold; margin-top: 20px; margin-bottom: 0;">
            {header_text}
        </div>
    """)

def display_form_header(header_text):
    """Display a centered header with the specified text."""
    st.html(f"""
        <div style="font-size: 24px; font-weight: bold;">
            {header_text}
        </div>
    """)

def display_total_customers_header(header_text):
    """Display a centered header with the specified text."""
    st.html(f"""
        <div style="font-size: 30px; font-weight: bold; margin-left: 20px; margin-right: 20px; margin-bottom: 10px">
            {header_text}
        </div>
    """)

def display_metric(label, subset_value, total_value):
    """Display a metric with a smaller label and the total number in a smaller gray font next to the subset value."""
    st.html(f"""
        <div style="text-align: center; margin-bottom: -10px;">
            <p style="font-size: 16px; margin-bottom: 0; margin-top: 0;">{label}</p>
            <p style="font-size: 24px; font-weight: bold; display: inline; margin: 0;">{subset_value}</p>
            <span style="font-size: 16px; color: gray;"> / {total_value}</span>
        </div>
    """)

def display_pie_chart_header(header_text):
    """Display a custom pie chart header with the specified text."""
    st.html(f"""
        <div style="text-align: center; font-size: 20px; font-weight: bold; margin-bottom: -10px;">
            {header_text}
        </div>
    """)

def display_table_header(header_text):
    """Display a custom dataframe table header with the specified text."""
    st.html(f"""
        <div style="text-align: center; font-size: 14px; font-weight: bold; margin-bottom: -10px;">
            {header_text}
        </div>
    """)

def display_user_input(label, placeholder, button_text, process_function):
    """Display a text area for user input and a button to process the input."""
    col1, col2, col3 = st.columns([1, 7, 1])
    with col2:
        with st.form(key=f"{label}_form"):
            display_form_header(label)
            user_input = st.text_area(label, placeholder, label_visibility='collapsed')  # Hiding the label but keeping it for accessibility

            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                submitted = st.form_submit_button(button_text, use_container_width=True)
                if submitted:
                    try:
                        processed_result = process_function(user_input)
                        return processed_result
                    except Exception as e:
                        st.error("Whoops, something went wrong. Have you tried unplugging it and plugging it back in?")
                        st.exception(e)
                return None