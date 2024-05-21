import streamlit as st
from core.llm import process_promotion_info
from ui.templates import display_section_header, display_user_input
from core.default_input import default_promotion_info

@st.experimental_fragment
def display_promotion_message():
    """Display and handle the promotional message."""
    display_section_header('✉️ Promotional Message')
    with st.container(border=True):
        st.html("<style='line-height:0.5;'>")
        display_promotion_info_input()
        st.html("<style='line-height:0.5;'>")
        display_promotion_message_editor()
        st.html("<style='line-height:0.5;'>")

def display_promotion_info_input():
    """Display the promotional information input and button."""
    result = display_user_input('💬 Input Promotional Information:', default_promotion_info, '💬 Generate Message', process_promotion_info)
    if result:
        st.session_state['promotion_message_template'] = result

def display_promotion_message_editor():
    """Display the editor for the generated promotional message."""
    result = display_user_input('✏️ Edit Promotion Message:', st.session_state['promotion_message_template'], '➡️ Send Messages', lambda x: x)
    if result:
        st.session_state['promotion_message_template'] = result
        st.balloons()
        customer_subset_number = len(st.session_state.get('customers_data', []))
        st.success(f"{customer_subset_number} Messages Sent!")