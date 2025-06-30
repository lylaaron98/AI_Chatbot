import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

st.title("AIE/ASE Personal Assistant ChatApp")

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat message from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

#create the input form
prompt = st.chat_input("Enter a prompt")

#if input provided, add it to the screen
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append(HumanMessage(prompt))
    
    # echo (response) and add it to the screen
    response = f"Echo: {prompt}"

    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append(AIMessage(response))