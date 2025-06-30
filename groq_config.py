from langchain_groq import ChatGroq
import streamlit as st

def get_groq_llm(model="llama3-8b-8192", temperature=1):
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=st.secrets["GROQ_API_KEY"]
    )

