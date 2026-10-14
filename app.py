import os
from dotenv import load_dotenv

import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Streamlit UI Configuration
st.set_page_config(page_title="BrainWave AI", page_icon="🧠", layout="centered")
st.title("🧠 BrainWave AI")

from groq import Groq

# Helper to safely retrieve secrets without crashing if secrets.toml is missing
def get_secret(key: str, default=None):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)

# Function to dynamically fetch models accessible with the provided API key
@st.cache_data(ttl=300, show_spinner=False)
def get_accessible_models(api_key: str):
    try:
        client = Groq(api_key=api_key)
        response = client.models.list()
        # Filter for text/chat models
        chat_models = [
            m.id for m in response.data 
            if not m.id.startswith("whisper") and "guard" not in m.id
        ]
        return sorted(chat_models) if chat_models else [m.id for m in response.data], None
    except Exception as e:
        return [], str(e)

# Retrieve Groq API Key from Streamlit secrets, environment, or user input
groq_api_key = get_secret("GROQ_API_KEY")

# Sidebar for settings & model selection
with st.sidebar:
    st.header("⚙️ Configuration")
    if not groq_api_key:
        groq_api_key = st.text_input(
            "Groq API Key:", 
            type="password", 
            help="Enter your Groq API key (starts with gsk_)"
        )
    
    # Dynamically discover models available for this specific API key
    discovered_models = []
    error_msg = None
    if groq_api_key:
        discovered_models, error_msg = get_accessible_models(groq_api_key.strip())

    if discovered_models:
        model_options = discovered_models + ["Enter custom model..."]
        selected_option = st.selectbox("Groq Model:", options=model_options, index=0)
        if selected_option == "Enter custom model...":
            selected_model = st.text_input("Custom Model ID:", value="llama-3.1-8b-instant")
        else:
            selected_model = selected_option
    else:
        if error_msg:
            st.warning(f"⚠️ Could not load models list: {error_msg}")
        # Fallback list if discovery fails or key not yet entered
        fallback_options = [
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama-3.3-70b-versatile"
        ]
        selected_model = st.selectbox("Groq Model:", options=fallback_options, index=0)

# LangSmith Tracking (only enable if a valid LangSmith key is configured)
langsmith_key = get_secret("LANGSMITH_API_KEY")
if langsmith_key:
    os.environ["LANGSMITH_API_KEY"] = langsmith_key
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = get_secret("LANGSMITH_PROJECT", "BrainWave AI")
else:
    os.environ["LANGSMITH_TRACING"] = "false"

# Validate Groq API Key
if not groq_api_key:
    st.info("👋 Welcome! Please enter your **Groq API Key** in the sidebar (or add `GROQ_API_KEY` to your secrets/.env) to get started.")
    st.stop()

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("human", "Question: {question}")
    ]
)

# Initialize ChatGroq LLM
llm = ChatGroq(
    model=selected_model,
    api_key=groq_api_key
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

input_text = st.text_input("What question do you have in mind?")

if input_text:
    try:
        with st.spinner(f"Thinking using {selected_model}..."):
            response = chain.invoke({"question": input_text})
        st.write(response)
    except Exception as e:
        st.error(f"❌ Error communicating with Groq API: {e}")

