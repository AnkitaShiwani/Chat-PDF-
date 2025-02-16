import streamlit as st
import tempfile
from pathlib import Path
import PyPDF2
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import io
import base64
import json

# Load supported languages
with open('languages.json', 'r', encoding='utf-8') as f:
    LANGUAGES = json.loads(f.read())

# Styling
st.set_page_config(page_title="ChatPDF", page_icon="📚", layout="wide")

def initialize_session_state():
    """Initialize session state variables"""
    session_vars = [
        'uploaded_files', 'processed_pdfs', 'chat_history', 
        'vector_store', 'conversation_chain'
    ]
    for var in session_vars:
        if var not in st.session_state:
            st.session_state[var] = [] if var in ['uploaded_files', 'processed_pdfs', 'chat_history'] else None
    
    # Initialize language with a default value
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'en'

def main():
    initialize_session_state()
    
    # Sidebar for file upload and settings
    with st.sidebar:
        st.title("📚 ChatPDF")
        api_key = st.text_input("Enter OpenAI API Key:", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Language selection
        selected_language = st.selectbox(
            "Select Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            index=0  # Set default index to 0 (English)
        )
        st.session_state.current_language = selected_language

if __name__ == "__main__":
    main()
