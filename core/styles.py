import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4f46e5;
            --danger: #e63946;
            --success: #2a9d8f;
            --info: #3a86ff;
            --dark: #1f2937;
            --warning: #f4a261;
            --neutral: #6c757d;
            --light-text: #f8f9fa;
            --light-bg: #f1f5f9;
            --light-label: #e2e8f0;
            --light-value: #f8fafc;
        }
        .main { background-color: var(--light-bg); }
        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: var(--light-text);
            padding: 2rem;
            border-radius: 0 0 12px 12px;
            margin-bottom: 2rem;
        }
        .accuracy-card {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white; padding: 1.5rem; border-radius: 12px;
            text-align: center; margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .accuracy-value { font-size: 3rem; font-weight: bold; margin: 0.5rem 0; }
        .analysis-container { background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
        .stTextArea textarea { min-height: 120px; border-radius: 8px; padding: 12px; border: 1px solid #e5e7eb; }
        .stButton button {
            background-color: var(--primary); color: var(--light-text); border-radius: 8px;
            padding: 10px 24px; font-weight: 500; border: none;
        }
        .stButton button:hover { background-color: #4338ca; color: var(--light-text); }
        .secondary-btn button { background-color: white !important; color: var(--primary) !important; border: 1px solid var(--primary) !important; }
        .file-uploader { border: 2px dashed #d1d5db; border-radius: 12px; padding: 2rem; text-align: center; margin-bottom: 1.5rem; }
        .review-item { padding: 1rem; border-bottom: 1px solid #e5e7eb; }
        .analysis-section { margin-bottom: 1.5rem; }
        .analysis-header { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--dark); }
        .indicator-item { margin-left: 1rem; margin-bottom: 0.3rem; }
        .result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .result-item { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #e5e7eb; }
        .result-label { font-weight: 600; color: var(--light-label); }
        .result-value { font-weight: 500; color: var(--light-value); }
        .positive { color: var(--success); font-weight: 600; background-color: rgba(42, 157, 143, 0.1); padding: 2px 8px; border-radius: 4px; }
        .negative { color: var(--danger); font-weight: 600; background-color: rgba(230, 57, 70, 0.1); padding: 2px 8px; border-radius: 4px; }
        .neutral { color: var(--neutral); font-weight: 600; background-color: rgba(108, 117, 125, 0.1); padding: 2px 8px; border-radius: 4px; }
        .genuine { color: var(--success); font-weight: 600; background-color: rgba(42, 157, 143, 0.1); padding: 2px 8px; border-radius: 4px; }
        .fake { color: var(--danger); font-weight: 600; background-color: rgba(230, 57, 70, 0.1); padding: 2px 8px; border-radius: 4px; }
        .language-value { color: var(--light-value); font-weight: 500; background-color: rgba(63, 114, 175, 0.1); padding: 2px 8px; border-radius: 4px; }
        .confidence-value { color: var(--light-value); font-weight: 500; background-color: rgba(147, 197, 253, 0.1); padding: 2px 8px; border-radius: 4px; }
        .polarity-value { color: var(--light-value); font-weight: 500; background-color: rgba(167, 139, 250, 0.1); padding: 2px 8px; border-radius: 4px; }
        * { cursor: default !important; }
        body { color: #4b5563; }
    </style>
    """, unsafe_allow_html=True)
