import streamlit as st
from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from config import initalize_model, initialize_db, StreamHandler
from langchain.memory import VectorStoreRetrieverMemory

def model(_stream_handler):
    ollama = initalize_model(_stream_handler)

    return ollama

@st.cache_resource
def database():
    db = initialize_db()

    return db

def chat(ollama, db):
    prompt_template = PromptTemplate(
        input_variables=["query"],
        template="As an AI assistant that can help with plant diseases, answer the query: {query}. Answer only with the information that is relevant and add description to give context. Organize your answer into bullet points."
    )

    memory = VectorStoreRetrieverMemory(retriever=db.as_retriever())
    qa = LLMChain(llm=ollama, prompt=prompt_template, memory=memory)

    return qa

db = database()
st.title("Plant Disease Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    stream_handler = StreamHandler(st.empty())
    ollama = model(stream_handler)
    
    qa = chat(ollama, db)
    qa.run(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": stream_handler.text})