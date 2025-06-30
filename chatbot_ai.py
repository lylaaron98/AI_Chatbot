import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from groq_config import get_groq_llm

st.title("AIE/ASE Personal Assistant")

st.markdown("""
    <div style='height:6px; background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet); border-radius: 3px; margin-bottom: 20px;'></div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="Personal Assistant:")]

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="images/PA_image.jpg"):
            st.markdown(message.content)

prompt = st.chat_input("Enter a prompt")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(prompt))

    llm = get_groq_llm()

    result = llm.invoke(st.session_state.messages).content

    with st.chat_message("assistant", avatar="images/PA_image.jpg"):
        st.markdown("""
            <span style='font-weight: bold; color: #ff9800; font-size: 1.15em;'>Personal Assistant:</span> {result}
        """.format(result=result), unsafe_allow_html=True)
    st.session_state.messages.append(AIMessage(result))
