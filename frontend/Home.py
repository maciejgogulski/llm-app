import os
import re
import streamlit as st
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/llm")  # default fallback

st.set_page_config(page_title="LLM Frontend", layout="centered")
st.title("Query the LLM")

# Input form
with st.form("query_form"):
    prompt = st.text_area("Prompt", height=100)
    mode = st.selectbox("Mode", ["prompt", "rag"])
    submitted = st.form_submit_button("Submit")

def extract_think_tag(text):
    match = re.search(r"<think>(.*?)</think>", text, re.DOTALL)
    if match:
        think_content = match.group(1).strip()
        # Remove the <think>...</think> section from the original text
        main_response = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        return main_response, think_content
    return text.strip(), None

if submitted:
    if not prompt.strip():
        st.error("Prompt cannot be empty.")
    else:
        endpoint = f"{API_BASE_URL}/{mode}"
        try:
            response = requests.post(endpoint, json={"prompt": prompt})
            response.raise_for_status()
            response_json = response.json()
            full_result = response_json.get("response", {}).get("result", "")

            main_text, think_text = extract_think_tag(full_result)

            if main_text:
                st.success("Main Response:")
                st.markdown(
                    f"""
                        {main_text}
                    """,
                    unsafe_allow_html=True
                )

            if think_text:
                st.info("🧠 Thought:")
                st.markdown(
                    f"""
                        {think_text}
                    """,
                    unsafe_allow_html=True
                )

            if not main_text and not think_text:
                st.warning("No result returned in response.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

