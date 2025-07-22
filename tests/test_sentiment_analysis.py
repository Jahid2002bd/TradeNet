from src.utils.sentiment_analysis import get_sentiment_score

def test_sentiment_score_range():
    score = get_sentiment_score("BTCUSDT")
    assert isinstance(score, float)
    assert -1.0 <= score <= 1.0
