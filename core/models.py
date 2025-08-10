import streamlit as st
import torch
from transformers import pipeline

@st.cache_resource
def load_models():
    model_dict = {}
    try:
        model_dict['en'] = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
    except Exception as e:
        st.error(f"Error loading English model: {str(e)}")
        model_dict['en'] = None
    
    try:
        model_dict['multi'] = pipeline(
            "text-classification",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            device=0 if torch.cuda.is_available() else -1
        )
    except Exception as e:
        st.error(f"Error loading multilingual model: {str(e)}")
        model_dict['multi'] = None
    
    return model_dict
