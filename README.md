# WhatsApp Chat Analyzer

Demo - https://3eswiu3t5jdm9sdmjmzjnz.streamlit.app/

A Streamlit-based web app to analyze WhatsApp chat exports and generate useful insights like message trends, activity heatmaps, word cloud, emoji usage, and sentiment breakdown.

## Features

- Upload WhatsApp `.txt` chat export
- Analyze by `Overall` or by individual user
- Top stats:
  - Total messages
  - Total words
  - Media shared
  - Links shared
- Monthly and daily message timeline
- Most active days and months
- Weekly activity heatmap (day vs hour)
- Most active users (for overall analysis)
- Student activity ranking table
- Word cloud and most common words
- Emoji analysis with usage distribution
- Sentiment analysis (positive, neutral, negative)

## Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- WordCloud
- VADER Sentiment
- URLExtract
- Emoji

## Project Structure

```bash
whatsapp_chat_analysis/
├── whatsapp_chat_analysis_code/
│   ├── ui.py                # Enhanced Streamlit UI
│   ├── app.py               # Basic Streamlit UI
│   ├── preprocessor.py      # Chat parsing and data preprocessing
│   ├── helper.py            # Analytics and visualization helpers
│   ├── stop_hinglish.txt    # Stopwords for word analysis
│   └── requirements.txt
└── whatsapp_chat_analysis_env/  # Local virtual environment (optional, not needed on GitHub)


A Streamlit-based web app to analyze WhatsApp chat exports and generate useful insights like message trends, activity heatmaps, word cloud, emoji usage, and sentiment breakdown.

## Features

- Upload WhatsApp `.txt` chat export
- Analyze by `Overall` or by individual user
- Top stats:
  - Total messages
  - Total words
  - Media shared
  - Links shared
- Monthly and daily message timeline
- Most active days and months
- Weekly activity heatmap (day vs hour)
- Most active users (for overall analysis)
- Student activity ranking table
- Word cloud and most common words
- Emoji analysis with usage distribution
- Sentiment analysis (positive, neutral, negative)

## Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- WordCloud
- VADER Sentiment
- URLExtract
- Emoji

## Project Structure

```bash
whatsapp_chat_analysis/
├── whatsapp_chat_analysis_code/
│   ├── ui.py                # Enhanced Streamlit UI
│   ├── app.py               # Basic Streamlit UI
│   ├── preprocessor.py      # Chat parsing and data preprocessing
│   ├── helper.py            # Analytics and visualization helpers
│   ├── stop_hinglish.txt    # Stopwords for word analysis
│   └── requirements.txt
└── whatsapp_chat_analysis_env/  # Local virtual environment (optional, not needed on GitHub)
