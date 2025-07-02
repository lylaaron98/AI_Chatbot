import streamlit as st
from faq_config import get_faq_response
from form_config import handle_booking_flow, render_booking_form
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from groq_config import get_groq_llm

st.set_page_config(page_title="AIE/ASE Personal Assistant", layout="wide")

# Sidebar navigation
with st.sidebar:
    st.markdown("## Navigation")
    nav = st.radio(
        "Go to:",
        ["Chat", "About", "Settings"],
        index=0,
        key="nav_radio"
    )
    st.markdown("---")
    st.markdown("Hide sidebar with the < icon above.")

st.title("AIE/ASE Personal Assistant")

st.markdown("""
    <div style='height:6px; background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet); border-radius: 3px; margin-bottom: 20px;'></div>
""", unsafe_allow_html=True)

if nav == "Chat":
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content="Personal Assistant:")]

    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant", avatar="images/PA_image.jpg"):
                st.markdown(
                    f"<span style='font-weight: bold; color: #ff9800; font-size: 1.15em;'>Personal Assistant:</span> {message.content}",
                    unsafe_allow_html=True
                )


    prompt = st.chat_input("Enter a prompt")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append(HumanMessage(prompt))

        # Step 1: Booking flow check
        booking_response = handle_booking_flow(prompt)
        if booking_response:
            with st.chat_message("assistant", avatar="images/PA_image.jpg"):
                st.markdown(f"<span style='font-weight: bold; color: #ff9800; font-size: 1.15em;'>Personal Assistant:</span> {booking_response}", unsafe_allow_html=True)
            st.session_state.messages.append(AIMessage(booking_response))
        else:
            # Step 2: FAQ check
            faq_answer = get_faq_response(prompt)
            if faq_answer:
                with st.chat_message("assistant", avatar="images/PA_image.jpg"):
                    st.markdown(f"<span style='font-weight: bold; color: #ff9800; font-size: 1.15em;'>Personal Assistant:</span> {faq_answer}", unsafe_allow_html=True)
                st.session_state.messages.append(AIMessage(faq_answer))
            else:
                # Step 3: Groq LLM response
                llm = get_groq_llm()
                result = llm.invoke(st.session_state.messages).content

                with st.chat_message("assistant", avatar="images/PA_image.jpg"):
                    st.markdown(f"<span style='font-weight: bold; color: #ff9800; font-size: 1.15em;'>Personal Assistant:</span> {result}", unsafe_allow_html=True)
                st.session_state.messages.append(AIMessage(result))

    # If booking form needs to be shown after eligibility
    if st.session_state.get("show_booking_form"):
        render_booking_form()

elif nav == "About":
    st.markdown("""
    ### About
    This is a personal assistant chat app powered by GroqAI and Streamlit.
    """)

elif nav == "Settings":
    st.markdown("""
    ### Settings
    (Settings UI can be added here.)
    """)
