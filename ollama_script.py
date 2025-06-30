from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

#initiate the model
llm = ChatOllama(
    model="llama3.2",
    temperature=1
)

#initiate the 'messages' object
messages=[
    SystemMessage("Act like a Personal Assistant for an internal company department"),
    HumanMessage("Hello, how are you?"),
    AIMessage("Hello, how can I help you today?")
]

# execute the model (with messages)
result = llm.invoke(messages)

#show result in the screen
print(result.content)