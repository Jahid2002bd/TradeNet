# src/utils/auto_trade_guard.py

"""
auto_trade_guard.py

Allows only high-confidence signals to execute automatically.
"""

def is_auto_trade_allowed(
    confidence_score: float,
    min_confidence: float = 90.0
) -> bool:
    """
    Returns True if confidence_score meets or exceeds min_confidence.
    """
    return confidence_score >= min_confidence

def choose_trade_mode(
    confidence_score: float,
    min_confidence: float = 90.0
) -> str:
    """
    Returns 'auto' for auto-execute, 'manual' otherwise.
    """
    if confidence_score >= min_confidence:
        return "auto"
    return "manual"

if __name__ == "__main__":
    # Demo usage
    demo_confidence = 92.5
    demo_threshold = 90.0

    mode = choose_trade_mode(demo_confidence, demo_threshold)
    print(f"Trade mode for confidence {demo_confidence}%: {mode}")
