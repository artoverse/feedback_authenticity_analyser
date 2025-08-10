# Feedback Authenticity Analyzer

An AI-powered application that detects fake reviews and analyzes sentiment in multiple languages (English, Hindi, Telugu).

## Features

- Fake review detection using DistilBERT models
- Multilingual support (English, Hindi, Telugu)
- Sentiment analysis (Positive/Negative/Neutral)
- Batch processing of CSV/Excel files
- Interactive dashboard with visualizations
- Word cloud generation for keyword analysis

## Installation

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Usage

1. Upload a CSV/Excel file with feedback or enter text manually
2. View analysis results in the dashboard
3. Explore advanced insights and visualizations

## Requirements

- Python 3.8+
- See requirements.txt for dependencies


Local Deployment:

- Create virtual environment: python -m venv venv
- Activate environment: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)
- Install dependencies: pip install -r requirements.txt
- Run application: streamlit run app.py