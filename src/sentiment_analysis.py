import requests
import pandas as pd
from transformers import pipeline

# --- Huggingface Sentiment Analyzer ---
sentiment_model = pipeline("sentiment-analysis")

# --- NewsAPI (basic headline fetch) ---
def fetch_news_headlines(query='Tesla', api_key='YOUR_NEWSAPI_KEY'):
    url = f'https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    articles = response.json().get('articles', [])
    headlines = [a['title'] for a in articles[:5]]
    return headlines

# --- Sentiment scorer ---
def analyze_sentiment(headlines):
    scores = []
    for line in headlines:
        result = sentiment_model(line)[0]
        label = result['label']
        score = result['score']
        scores.append({'text': line, 'label': label, 'score': score})
    return pd.DataFrame(scores)

# --- Overall signal ---
def get_sentiment_score(query='Tesla', api_key='YOUR_NEWSAPI_KEY'):
    headlines = fetch_news_headlines(query=query, api_key=api_key)
    df = analyze_sentiment(headlines)
    bullish = df[df['label'] == 'POSITIVE']
    bearish = df[df['label'] == 'NEGATIVE']
    sentiment_strength = len(bullish) - len(bearish)
    decision = 'positive' if sentiment_strength > 0 else 'negative'
    return {
        'sentiment': decision,
        'details': df.to_dict(orient='records')
    }