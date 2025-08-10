# System Architecture

## Components

1. **User Interface**
   - Streamlit-based web interface
   - Three main tabs: Analysis, Dashboard, Insights

2. **Core Functionality**
   - Language detection (English/Hindi/Telugu)
   - Authenticity classification (Genuine/Fake)
   - Sentiment analysis (Positive/Negative/Neutral)

3. **Models**
   - DistilBERT-base-uncased (English)
   - BERT-base-multilingual (Hindi/Telugu)

4. **Data Processing**
   - Text preprocessing
   - Hash-based duplicate detection
   - Batch processing for CSV/Excel files

## Workflow

1. User inputs text or uploads file
2. System detects language
3. Appropriate model analyzes text
4. Results stored in session state
5. Visualizations generated from aggregated data