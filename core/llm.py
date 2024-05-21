import os
import replicate
import streamlit as st
from datetime import datetime

# Set the Replicate API token from Streamlit secrets
os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]

def load_prompt(prompt_filename):
    """Load a prompt from a file."""
    try:
        with open(f'prompts/{prompt_filename}', 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"Prompt file {prompt_filename} not found.")
        return ""

# Load the prompts from the prompts directory
sql_prompt = load_prompt('sql_query_prompt.md')
promotion_prompt = load_prompt('promotion_message_prompt.md')
explain_sql_prompt = load_prompt('sql_explanation_prompt.md')

def run_arctic_llm(prompt, user_request, temperature=0.2):
    """Run the Arctic LLM using Replicate API with the given prompt and user request."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_day = datetime.now().strftime('%A')
    input_data = {
        "prompt": f"{prompt}\nCurrent Date: {current_date}\nCurrent Day: {current_day}\nUser Request: {user_request}\n",
        "temperature": temperature
    }
    
    output = replicate.run(
        "snowflake/snowflake-arctic-instruct",
        input=input_data
    )
    
    # Ensure output is a clean string
    return ''.join(output).strip()

def handle_subset_criteria(criteria, temperature=0.2):
    """Handle the subset criteria using the Arctic LLM."""
    with st.spinner("Generating SQL Query..."):
        sql_query = process_sql_query(criteria, temperature)
        explanation = process_sql_explanation(sql_query, temperature)
    return sql_query, explanation

def process_sql_query(criteria, temperature=0.2):
    """Process the SQL query using the Arctic LLM."""
    return run_arctic_llm(sql_prompt, f"SQL Query:\n{criteria}", temperature)

def process_sql_explanation(sql_query, temperature=0.2):
    """Process the SQL query explanation using the Arctic LLM."""
    return run_arctic_llm(explain_sql_prompt, f"SQL Query:\n{sql_query}", temperature)

def process_promotion_info(promotion_info, temperature=0.2):
    """Process the promotional information using the Arctic LLM."""
    with st.spinner("Writing Message..."):
        return run_arctic_llm(promotion_prompt, f"Promotional Message:\n{promotion_info}", temperature)
