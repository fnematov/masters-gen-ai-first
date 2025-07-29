import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from ticket import create_mock_ticket

load_dotenv()
openai_key = os.environ.get("OPENAI_API_KEY")

st.set_page_config(page_title="SaaS Support Bot")
st.title("🤖 SaaS Product Support Chatbot")

@st.cache_resource
def load_qa_chain():
    documents = []
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(f"data/{file}")
            docs = loader.load_and_split()
            for doc in docs:
                doc.metadata["source"] = file
            documents.extend(docs)

    # Use local HuggingFace model for embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embedding_model)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(openai_api_key=openai_key),
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
        output_key="answer"
    )
    return chain

chain = load_qa_chain()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask a question about your SaaS documentation:")

if user_input:
    result = chain({"question": user_input})
    answer = result["answer"]
    sources = result.get("source_documents", [])

    st.session_state.history.append((user_input, answer, sources))

for q, a, srcs in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")
    for doc in srcs:
        st.markdown(f"> 📄 _Source: {doc.metadata.get('source', 'Unknown')} page {doc.metadata.get('page', '?')}_")

    if "I don't know" in a or "unsure" in a.lower():
        if st.button(f"Create support ticket for: '{q}'"):
            create_mock_ticket(user_name="John Doe", email="john@example.com", summary=q, description=a)