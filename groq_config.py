from langchain_groq import ChatGroq
import streamlit as st


DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"


def get_groq_llm(model=None, temperature=1):
    selected_model = model or st.secrets.get("GROQ_MODEL", DEFAULT_GROQ_MODEL)
    return ChatGroq(
        model=selected_model,
        temperature=temperature,
        api_key=st.secrets["GROQ_API_KEY"],
    )

