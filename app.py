import os
from dotenv import load_dotenv

import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# LangSmith Tracking (optional)
os.environ["LANGSMITH_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("human", "Question: {question}")
    ]
)

# Streamlit UI
st.title("BrainWave AI")
input_text = st.text_input("What question do you have in mind?")

# ✅ Replace Ollama with Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=st.secrets["GROQ_API_KEY"]
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

if input_text:
    response = chain.invoke({"question": input_text})
    st.write(response)
