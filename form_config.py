import streamlit as st
import pandas as pd
from datetime import datetime

def handle_booking_flow(prompt):
    if "booking_step" not in st.session_state:
        st.session_state.booking_step = None
    if "booking_answers" not in st.session_state:
        st.session_state.booking_answers = {}
    if "show_booking_form" not in st.session_state:
        st.session_state.show_booking_form = False

    # Detect booking intent
    if "book" in prompt.lower() and "room" in prompt.lower():
        st.session_state.booking_step = 1
        st.session_state.booking_answers = {}
        return "Sure! Let's check your eligibility to book the AIE/ASE room.\n\n**How many people will be attending?**"

    # Handle step-by-step questions
    if st.session_state.booking_step:
        step = st.session_state.booking_step
        if step == 1:
            st.session_state.booking_answers["people"] = prompt
            st.session_state.booking_step = 2
            return "**Is this a hybrid event (yes/no)?**"
        elif step == 2:
            st.session_state.booking_answers["hybrid"] = prompt
            st.session_state.booking_step = 3
            return "**What’s the reason for booking?**"
        elif step == 3:
            st.session_state.booking_answers["reason"] = prompt
            st.session_state.booking_step = 4
            return "**When is the booking for? (e.g., 2025-07-10 14:00)**"
        elif step == 4:
            st.session_state.booking_answers["datetime"] = prompt
            st.session_state.booking_step = None
            st.session_state.show_booking_form = True
            return (
                "✅ All checks complete.\n\n"
                "💰 **Booking cost is SGD$5000 per use.**\n\n"
                "Please fill in the final booking form below to confirm."
            )
    return None

def render_booking_form():
    with st.form("final_booking_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        team = st.text_input("Your Department / Team")
        confirm = st.form_submit_button("Submit Booking")

    if confirm:
        data = {
            "Timestamp": [datetime.now()],
            "Name": [name],
            "Email": [email],
            "Team": [team],
            "People": [st.session_state.booking_answers.get("people")],
            "Hybrid": [st.session_state.booking_answers.get("hybrid")],
            "Reason": [st.session_state.booking_answers.get("reason")],
            "Booking Datetime": [st.session_state.booking_answers.get("datetime")],
            "Cost": ["SGD$5000"]
        }
        df = pd.DataFrame(data)
        df.to_excel("bookings.xlsx", index=False, engine="openpyxl")
        st.success("✅ Booking submitted successfully! A confirmation will be sent to your email.")
        st.session_state.show_booking_form = False
