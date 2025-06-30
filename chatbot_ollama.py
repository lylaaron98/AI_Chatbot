import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

st.title("AIE/ASE Personal Assistant ChatApp")

# Add a rainbow line below the header
st.markdown(
    """
    <div style='height:6px; background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet); border-radius: 3px; margin-bottom: 20px;'></div>
    """,
    unsafe_allow_html=True
)

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat message from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="images/PA_image.jpg"):
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

    with st.chat_message("assistant", avatar="images/PA_image.jpg"):
        st.markdown(response)
        st.session_state.messages.append(AIMessage(response))