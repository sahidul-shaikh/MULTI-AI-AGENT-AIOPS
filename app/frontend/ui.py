import streamlit as st
import requests

from app.config.settings import settings
from app.common.custom_exception import CustomException
from app.common.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent")

system_prompt = st.text_area("Define your AI Agent", value="You are a helpful assistant.", height=80)
selected_model = st.selectbox("Select AI Model", options=settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("Allow Web Search", value=False)
user_query = st.text_area("Enter your query", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Get Response"):

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": user_query,
        "allow_search": allow_web_search
    }

    try:
        logger.info(f"Sending request to API with model: {selected_model}")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Response received successfully from API")
            st.subheader("AI Agent Response")
            st.markdown(agent_response)
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")

    except Exception as e:
        logger.error(f"Exception during API call: {e}")
        st.error(f"An error occurred: {CustomException('Failed to get response from API', error_detail=e)}")