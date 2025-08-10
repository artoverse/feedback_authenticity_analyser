import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

from core.styles import inject_custom_css
from core.models import load_models
from core.logic import analyze_feedback
from core.utils import (
    ensure_session_state,
)

# Inject CSS and init session state
inject_custom_css()
ensure_session_state()

# Load pre-trained models once
models = load_models()

# Header
st.markdown("""
<div class='header'>
    <h1 style='margin: 0;'>Feedback Authenticity Analyzer</h1>
    <p style='margin: 0.5rem 0 0; opacity: 0.9;'>Detect fake reviews with AI-powered analysis (Supports English, Hindi & Telugu)</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Analyze Feedback", "Review Dashboard", "Advanced Insights"])

with tab1:
    with st.expander("📁 Batch Upload (CSV/Excel)", expanded=False):
        uploaded_file = st.file_uploader(
            "Upload your feedback file",
            type=['csv', 'xlsx'],
            help="File should contain a 'feedback' or 'text' column",
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                if 'feedback' not in df.columns and 'text' not in df.columns:
                    st.error("Error: File must contain a 'feedback' or 'text' column")
                else:
                    feedback_col = 'feedback' if 'feedback' in df.columns else 'text'
                    with st.spinner(f"Analyzing {len(df)} feedback entries..."):
                        new_reviews = []
                        for feedback in df[feedback_col]:
                            if pd.notna(feedback) and isinstance(feedback, str):
                                result, error = analyze_feedback(str(feedback), models=models)
                                if result:
                                    new_reviews.append(result)
                                elif error:
                                    # Non-blocking: log or show first error
                                    pass
                        if new_reviews:
                            st.session_state.reviews.extend(new_reviews)
                            st.success(f"Successfully analyzed {len(new_reviews)} new feedback entries!")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

    st.markdown("### ✍️ Single Feedback Analysis")
    
    language_option = st.radio(
        "Select language (or Auto-detect)",
        options=['Auto-detect', 'English', 'Hindi', 'Telugu'],
        horizontal=True
    )
    selected_lang = 'auto' if language_option == 'Auto-detect' else \
                   'en' if language_option == 'English' else \
                   'hi' if language_option == 'Hindi' else 'te'
    
    feedback = st.text_area(
        "Enter feedback text:",
        placeholder="Paste customer feedback here...",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Feedback"):
            if feedback.strip():
                result, error = analyze_feedback(feedback, selected_lang, models)
                
                if error:
                    st.error(error)
                elif result:
                    st.session_state.reviews.append(result)
                    
                    with st.container():
                        st.markdown("### Analysis Results")
                        st.markdown(f"**Feedback:** {result['text']}")
                        
                        st.markdown(f"""
                        <div class="result-grid">
                            <div class="result-item">
                                <span class="result-label">Detected Language:</span>
                                <span class="language-value">{result['language']}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Classification:</span>
                                <span class="{'genuine' if result['classification'] == 'GENUINE' else 'fake'}">{result['classification']}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Confidence:</span>
                                <span class="confidence-value">{result['confidence']}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Sentiment:</span>
                                <span class="{'positive' if result['sentiment'] == 'POSITIVE' else 'negative' if result['sentiment'] == 'NEGATIVE' else 'neutral'}">{result['sentiment']}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Polarity:</span>
                                <span class="polarity-value">{result['polarity']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("🔍 Key Indicators", expanded=True):
                            if result['classification'] == 'FAKE':
                                st.markdown("- Unnatural language patterns")
                                st.markdown("- Overly generic or exaggerated statements")
                                st.markdown("- Mismatch between sentiment and content")
                            else:
                                st.markdown("- Natural language patterns")
                                st.markdown("- Specific details and examples")
                                st.markdown("- Consistent sentiment throughout")
                            
                            if result['sentiment'] == 'NEGATIVE':
                                st.markdown("- Criticism of specific aspects")
                                st.markdown("- Frustrated or disappointed tone")
                            elif result['sentiment'] == 'POSITIVE':
                                st.markdown("- Praise for specific aspects")
                                st.markdown("- Satisfied or enthusiastic tone")
                else:
                    st.warning("Please enter feedback to analyze")

    with col2:
        if st.button("Clear Input", type="secondary"):
            st.rerun()

with tab2:
    if st.session_state.reviews:
        st.markdown(f"### 📋 Review Dashboard ({len(st.session_state.reviews)} analyzed)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_class = st.selectbox("Filter by authenticity", ["All", "GENUINE", "FAKE"], index=0)
        with col2:
            filter_sent = st.selectbox("Filter by sentiment", ["All", "POSITIVE", "NEUTRAL", "NEGATIVE"], index=0)
        with col3:
            filter_lang = st.selectbox("Filter by language", ["All", "English", "Hindi", "Telugu"], index=0)
        
        filtered_reviews = [r for r in st.session_state.reviews 
                          if (filter_class == "All" or r['classification'] == filter_class) and
                          (filter_sent == "All" or r['sentiment'] == filter_sent) and
                          (filter_lang == "All" or r['language'] == filter_lang)]
        
        for review in filtered_reviews:
            st.markdown(f"""
            <div class='review-item'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <div>
                        <span class="{'genuine' if review['classification'] == 'GENUINE' else 'fake'}">
                            {review['classification']}
                        </span>
                        <span class="confidence-value"> ({review['confidence']})</span>
                        <span class="language-value" style='margin-left: 1rem;'>{review['language']}</span>
                    </div>
                    <small style='color: #6b7280;'>{review['timestamp']}</small>
                </div>
                <div style='margin-bottom: 0.5rem;'>{review['text']}</div>
                <div>
                    <span class="{'positive' if review['sentiment'] == 'POSITIVE' else 'negative' if review['sentiment'] == 'NEGATIVE' else 'neutral'}">
                        {review['sentiment']}
                    </span>
                    <span class="polarity-value"> (Polarity: {review['polarity']})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        csv = pd.DataFrame(filtered_reviews).to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Results",
            data=csv,
            file_name='feedback_analysis.csv',
            mime='text/csv'
        )
    else:
        st.info("No reviews analyzed yet. Submit feedback in the 'Analyze Feedback' tab.")

with tab3:
    if st.session_state.reviews:
        st.markdown("### 📊 Advanced Insights")
        
        df = pd.DataFrame(st.session_state.reviews)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Reviews", len(df))
        with col2:
            genuine_pct = len(df[df['classification'] == 'GENUINE']) / len(df)
            st.metric("Genuine Reviews", f"{genuine_pct:.0%}")
        with col3:
            fake_pct = len(df[df['classification'] == 'FAKE']) / len(df)
            st.metric("Fake Reviews", f"{fake_pct:.0%}")
        with col4:
            lang_counts = df['language'].value_counts(normalize=True)
            st.metric("Hindi Reviews", f"{lang_counts.get('Hindi', 0):.0%}")
        
        st.markdown("#### Distributions")
        fig_col1, fig_col2, fig_col3 = st.columns(3)
        
        with fig_col1:
            st.markdown("Authenticity")
            fig, ax = plt.subplots()
            sns.countplot(data=df, x='classification', palette=['#2a9d8f', '#e63946'])
            plt.xlabel("")
            plt.ylabel("Count")
            st.pyplot(fig)
        
        with fig_col2:
            st.markdown("Sentiment")
            fig, ax = plt.subplots()
            sns.countplot(data=df, x='sentiment', palette=['#2a9d8f', '#e63946', '#3a86ff'], order=['POSITIVE', 'NEGATIVE', 'NEUTRAL'])
            plt.xlabel("")
            plt.ylabel("Count")
            st.pyplot(fig)
        
        with fig_col3:
            st.markdown("Language")
            fig, ax = plt.subplots()
            sns.countplot(data=df, x='language', palette=['#4f46e5', '#e63946', '#2a9d8f'])
            plt.xlabel("")
            plt.ylabel("Count")
            st.pyplot(fig)
        
        st.markdown("#### Model Accuracy Analysis")
        accuracy_col1, accuracy_col2 = st.columns(2)
        
        with accuracy_col1:
            st.markdown("**Confidence Distribution**")
            fig, ax = plt.subplots()
            df['confidence_num'] = df['confidence'].str.rstrip('%').astype('float') / 100.0
            sns.histplot(data=df, x='confidence_num', bins=10, kde=True, color='#4f46e5')
            plt.xlabel("Confidence Level")
            plt.ylabel("Count")
            st.pyplot(fig)
            
        with accuracy_col2:
            st.markdown("**Accuracy Metrics**")
            avg_conf_genuine = df[df['classification'] == 'GENUINE']['confidence_num'].mean()
            avg_conf_fake = df[df['classification'] == 'FAKE']['confidence_num'].mean()
            
            def safe_ratio(a, b):
                return a/b if b else np.nan

            genuine_total = len(df[df['classification'] == 'GENUINE'])
            fake_total = len(df[df['classification'] == 'FAKE'])
            genuine_pos = safe_ratio(len(df[(df['classification'] == 'GENUINE') & (df['sentiment'] == 'POSITIVE')]), genuine_total)
            fake_neg = safe_ratio(len(df[(df['classification'] == 'FAKE') & (df['sentiment'] == 'NEGATIVE')]), fake_total)
            
            st.metric("Average Confidence (Genuine)", f"{avg_conf_genuine:.0%}" if not np.isnan(avg_conf_genuine) else "N/A")
            st.metric("Average Confidence (Fake)", f"{avg_conf_fake:.0%}" if not np.isnan(avg_conf_fake) else "N/A")
            st.metric("Positive Sentiment in Genuine", f"{genuine_pos:.0%}" if not np.isnan(genuine_pos) else "N/A")
            st.metric("Negative Sentiment in Fake", f"{fake_neg:.0%}" if not np.isnan(fake_neg) else "N/A")
        
        st.markdown("#### Keyword Analysis")
        tab_k1, tab_k2 = st.tabs(["Genuine Reviews", "Fake Reviews"])
        
        with tab_k1:
            genuine_text = " ".join(df[df['classification'] == 'GENUINE']['text'])
            if genuine_text:
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(genuine_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("No genuine reviews available")
        
        with tab_k2:
            fake_text = " ".join(df[df['classification'] == 'FAKE']['text'])
            if fake_text:
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(fake_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("No fake reviews available")
    else:
        st.info("No reviews analyzed yet. Submit feedback in the 'Analyze Feedback' tab.")

with st.sidebar:
    st.markdown("### System Controls")
    if st.button("🚨 Reset All Data"):
        st.session_state.reviews = []
        st.session_state.processed_hashes = set()
        st.success("All data has been reset!")
        st.rerun()
