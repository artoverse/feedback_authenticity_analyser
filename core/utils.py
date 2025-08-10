import streamlit as st
import hashlib
import nltk
from langdetect import detect, DetectorFactory

# Initialize NLTK & langdetect only once
@st.cache_resource
def _init_nlp_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
    DetectorFactory.seed = 0
    return True

_init_nlp_resources()

def ensure_session_state():
    if 'reviews' not in st.session_state:
        st.session_state.reviews = []
    if 'processed_hashes' not in st.session_state:
        st.session_state.processed_hashes = set()

def create_feedback_hash(feedback: str) -> str:
    return hashlib.md5(feedback.encode()).hexdigest()

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return 'hi' if lang == 'hi' else 'te' if lang == 'te' else 'en'
    except Exception:
        return 'en'
