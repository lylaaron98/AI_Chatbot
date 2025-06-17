import streamlit as st
from crewai import Crew, Agent
from langchain_groq import ChatGroq

# Initialize Groq agent
llm =  ChatGroq(
    groq_api_key="YOUR_GROQ_API_KEY",
    model_name="mixtral-8x7b-32768"
)

# Define an agent
bot_agent = Agent(
    role="AIE/ASE Bot",
    goal="Provide helpful responses to user queries about AIS/ASE topics.",
    backstory="An AI assistant specialized in AIS/ASE topics, ready to assist users with their questions.",
    llm=llm
)

# Create a Crew
bot_crew = Crew(
    agents=[bot_agent],
    process='sequential'
)

# Streamlit UI
st.title("AIS/ASE Groq AI Chatbot Prototype")

# Chat input
user_input = st.text_input("Enter your message:")

# Send input to chat flow and get response
if user_input:
    response = chat_flow.run(user_input)
    st.write("Response from Groq AI:", response)