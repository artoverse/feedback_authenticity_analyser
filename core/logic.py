import pandas as pd
from textblob import TextBlob
import streamlit as st

from .utils import create_feedback_hash, detect_language

def analyze_sentiment(text: str, language: str, models: dict):
    if language == 'en':
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment_label = "POSITIVE" if polarity > 0.2 else "NEGATIVE" if polarity < -0.2 else "NEUTRAL"
        return sentiment_label, f"{polarity:.2f}"
    else:
        if models.get('multi') is None:
            return "NEUTRAL", "0.00"
        result = models['multi'](text)[0]
        rating = int(result['label'][0])  # '1 star'..'5 stars' style
        if rating >= 4:
            return "POSITIVE", f"{(rating-3)/2:.2f}"
        elif rating <= 2:
            return "NEGATIVE", f"{(rating-3)/2:.2f}"
        else:
            return "NEUTRAL", "0.00"

def analyze_feedback(feedback: str, selected_language: str = 'auto', models: dict = None):
    if models is None:
        return None, "Models not loaded"
    
    feedback_hash = create_feedback_hash(feedback)
    if feedback_hash in st.session_state.processed_hashes:
        return None, "This feedback has already been analyzed."
    
    try:
        language = detect_language(feedback) if selected_language == 'auto' else selected_language
        
        # Authenticity via classifier
        if language == 'en':
            if models.get('en') is None:
                return None, "English analysis not available"
            auth_result = models['en'](feedback)[0]
            # Heuristic mapping: negative -> FAKE (as per your original logic)
            classification = "FAKE" if auth_result['label'].lower() in ['negative', 'fake'] else "GENUINE"
        else:
            if models.get('multi') is None:
                return None, "Multilingual analysis not available"
            auth_result = models['multi'](feedback)[0]
            classification = "FAKE" if auth_result['score'] < 0.6 else "GENUINE"
        
        confidence = auth_result['score']
        sentiment_label, polarity = analyze_sentiment(feedback, language, models)
        
        result = {
            "id": len(st.session_state.reviews) + 1,
            "text": feedback,
            "language": "Hindi" if language == 'hi' else "Telugu" if language == 'te' else "English",
            "classification": classification,
            "confidence": f"{confidence:.0%}",
            "sentiment": sentiment_label,
            "polarity": polarity,
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.processed_hashes.add(feedback_hash)
        return result, None
        
    except Exception as e:
        return None, f"Error analyzing feedback: {str(e)}"
