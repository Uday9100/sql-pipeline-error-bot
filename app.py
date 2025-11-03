import streamlit as st
import openai
import os

# Securely get your OpenAI API key from environment variables (Streamlit Cloud secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("SQL & Pipeline Error Finder Bot")

query_type = st.radio("Select Query Type", ["SQL", "Pipeline"])
user_input = st.text_area("Enter SQL/pipeline code or describe the error:")

def get_fix(input_text, query_type):
    prompt = (
        f"Find errors and suggest fixes for this {query_type}:\n{input_text}\n"
        "Explain the errors and provide corrected code or suggestions."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in SQL and data pipelines."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=700,
        temperature=0.2,
    )
    return response.choices[0].message.content

if st.button("Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text or code!")
    else:
        with st.spinner("Analyzing your input…"):
            result = get_fix(user_input, query_type)
            st.markdown(result)
