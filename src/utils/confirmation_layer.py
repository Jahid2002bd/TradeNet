"""
confirmation_layer.py

Confirms and formats trade signal messages by validating:
1. RSI level
2. MACD crossover
3. Volume spike
4. Sentiment score
5. AI confidence
6. Market open status

Returns formatted message if signal is fully approved.
"""

from datetime import datetime, timezone
from typing import Optional
from src.utils.sentiment_analysis import get_sentiment_score
from src.utils.timezone_filter import is_market_open


# ---------------- Indicator Validators ----------------

def validate_rsi(rsi: float, low: float = 30.0, high: float = 70.0) -> bool:
    return rsi <= low or rsi >= high

def validate_macd(macd_line: float, signal_line: float) -> bool:
    return macd_line > signal_line

def validate_volume_spike(current: float, average: float, spike_ratio: float = 1.5) -> bool:
    if average <= 0:
        return False
    return current >= average * spike_ratio

# ---------------- Sentiment & AI Validators ----------------

def validate_sentiment(sentiment: float, min_score: float = 0.3) -> bool:
    return abs(sentiment) >= min_score

def validate_confidence(confidence: float, threshold: float = 80.0) -> bool:
    return confidence >= threshold

# ---------------- Core Trade Confirmation ----------------

def confirm_trade_message(
    symbol: str,
    entry: float,
    stop_loss: float,
    take_profit: float,
    rsi: float,
    macd_line: float,
    signal_line: float,
    volume: float,
    avg_volume: float,
    ai_confidence: float
) -> Optional[str]:
    """
    Combines validation layers and returns full trade message if approved.

    Returns:
        str: Confirmation message if all filters pass
        None: If rejected
    """
    sentiment_score = get_sentiment_score(symbol)
    current_utc = datetime.now(timezone.utc)

    # ✅ Fix: call is_market_open with correct arguments
    market_ok = is_market_open(current_utc, symbol)

    checks = {
        "rsi": validate_rsi(rsi),
        "macd": validate_macd(macd_line, signal_line),
        "volume": validate_volume_spike(volume, avg_volume),
        "sentiment": validate_sentiment(sentiment_score),
        "confidence": validate_confidence(ai_confidence),
        "market": market_ok
    }

    if all(checks.values()):
        return (
            f"✅ Confirmed trade {symbol}:\n"
            f"→ Enter at {entry}\n"
            f"→ SL at {stop_loss}\n"
            f"→ TP at {take_profit}\n"
            f"(Sentiment: {round(sentiment_score, 2)} | Confidence: {ai_confidence}%)"
        )

    return None
