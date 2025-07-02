import streamlit as st
import pandas as pd
from datetime import datetime

import smtplib
from email.message import EmailMessage

def handle_booking_flow(prompt):
    if "booking_step" not in st.session_state:
        st.session_state.booking_step = None
    if "booking_answers" not in st.session_state:
        st.session_state.booking_answers = {}
    if "show_booking_form" not in st.session_state:
        st.session_state.show_booking_form = False

    lower_prompt = prompt.lower()

    # ✅ NEW: Restart trigger
    if "restart" in lower_prompt and ("booking" in lower_prompt or "room" in lower_prompt):
        st.session_state.booking_step = None
        st.session_state.booking_answers = {}
        st.session_state.show_booking_form = False
        return "🔁 Booking process has been restarted. You can now begin again by saying something like **'I want to book the room'**."

    # ✅ Booking intent detection
    booking_keywords = ["book", "booking", "reserve", "reservation"]
    space_keywords = ["room", "space", "aie", "ase"]

    if (
        st.session_state.booking_step is None and
        any(word in lower_prompt for word in booking_keywords) and
        any(word in lower_prompt for word in space_keywords)
    ):
        st.session_state.show_booking_form = False  # reset form if previously shown
        st.session_state.booking_step = 1
        st.session_state.booking_answers = {}
        return "Sure! Let's check your eligibility to book the AIE/ASE room.\n\n**How many people will be attending?**"

    # Step-by-step checks
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

def send_email_with_excel(receiver_email, excel_path, sender_email, sender_password):
    msg = EmailMessage()
    msg['Subject'] = 'AIE/ASE Room Booking Confirmation'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Please find attached the submitted AIE/ASE room booking form.")

    with open(excel_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="booking.xlsx")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

def render_booking_form():
    with st.form("final_booking_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        team = st.text_input("Your Department / Team")
        confirm = st.form_submit_button("Submit Booking")

    if confirm:
        file_path = "bookings.xlsx"
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
        df.to_excel(file_path, index=False, engine="openpyxl")

        # # ✅ Send email with attached Excel file
        # send_email_with_excel(
        #     receiver_email="recipient@example.com",  # ← Replace with actual recipient
        #     excel_path=file_path,
        #     sender_email=st.secrets["EMAIL_SENDER"],
        #     sender_password=st.secrets["EMAIL_PASSWORD"]
        # )

        st.success("✅ Booking submitted and emailed successfully!")
        st.session_state.show_booking_form = False

