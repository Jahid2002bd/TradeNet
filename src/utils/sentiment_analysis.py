# src/utils/sentiment_analysis.py

"""
sentiment_analysis.py

Fetches recent news articles for a given symbol and computes
an average sentiment polarity score using TextBlob.
Requires:
  - Environment variable NEWS_API_KEY set to a valid NewsAPI key.
  - textblob library installed.
"""

import os
import requests
from textblob import TextBlob

API_URL = "https://newsapi.org/v2/everything"
API_KEY = os.getenv("NEWS_API_KEY")


def get_sentiment_score(symbol: str, limit: int = 5) -> float:
    """
    Retrieve recent news for the symbol and calculate average polarity.

    Parameters:
        symbol (str): Market ticker or keyword to search.
        limit  (int): Max number of articles to fetch.

    Returns:
        float: Average sentiment polarity (-1.0 to +1.0).
               Returns 0.0 if no articles or API failure.
    """
    if not API_KEY:
        return 0.0

    params = {
        "q": symbol,
        "apiKey": API_KEY,
        "pageSize": limit,
        "language": "en",
        "sortBy": "publishedAt"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
    except requests.RequestException:
        # Network issue, timeout, invalid response, etc.
        return 0.0
    except ValueError:
        # JSON decoding failed
        return 0.0

    polarities = []
    for art in articles:
        content = art.get("description") or art.get("title") or ""
        if content:
            tb = TextBlob(content)
            polarities.append(tb.sentiment.polarity)

    if not polarities:
        return 0.0
    return sum(polarities) / len(polarities)


if __name__ == "__main__":
    # Demo: compute sentiment for BTCUSDT
    demo_symbol = "BTCUSDT"
    score = get_sentiment_score(demo_symbol, limit=3)
    print(f"Sentiment score for {demo_symbol}: {score:.3f}")
