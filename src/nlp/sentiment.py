import re
import math
from typing import Tuple

# Financial Sentiment Lexicon (Loughran-McDonald & Financial Domain calibrated)
FINANCIAL_POSITIVE = {
    "surge": 2.5, "surges": 2.5, "surging": 2.5, "soar": 2.8, "soars": 2.8, "soaring": 2.8,
    "rally": 2.4, "rallies": 2.4, "outperform": 2.2, "outperformed": 2.2, "beat": 2.0, "beats": 2.0,
    "profit": 1.8, "record": 2.0, "growth": 1.7, "bullish": 2.6, "expansion": 1.6, "dividend": 1.4,
    "breakthrough": 2.8, "upgraded": 2.3, "upgrade": 2.3, "gain": 1.5, "gains": 1.5, "rebound": 1.9,
    "tailwind": 1.8, "robust": 2.0, "strong": 1.5, "boom": 2.2, "highest": 1.6, "exceed": 2.1,
    "exceeded": 2.1, "positive": 1.8, "approval": 2.2, "approved": 2.2, "innovation": 1.8
}

FINANCIAL_NEGATIVE = {
    "plunge": -2.8, "plunges": -2.8, "plunging": -2.8, "crash": -3.2, "crashes": -3.2, "crashing": -3.2,
    "slump": -2.4, "slumps": -2.4, "default": -3.5, "defaults": -3.5, "defaulting": -3.5,
    "downgrade": -2.5, "downgraded": -2.5, "recession": -3.0, "loss": -1.8, "losses": -2.0,
    "collapse": -3.4, "collapsing": -3.4, "bankrupt": -3.8, "bankruptcy": -3.8, "inflation": -1.5,
    "hawkish": -1.8, "spike": -1.2, "spiking": -1.2, "miss": -1.8, "misses": -1.8, "bearish": -2.4,
    "investigation": -2.2, "fraud": -3.5, "lawsuit": -1.9, "fine": -1.6, "penalty": -1.8,
    "layoff": -1.9, "layoffs": -2.0, "deficit": -1.7, "headwind": -1.8, "debt": -1.2, "crisis": -3.2,
    "sanctions": -2.8, "embargo": -2.6, "war": -3.5, "conflict": -2.6, "risk": -1.2, "freeze": -2.2,
    "frozen": -2.2, "warning": -1.8, "warns": -1.8, "breach": -2.8, "hack": -2.7, "outage": -2.0
}

INTENSIFIERS = {"very": 1.4, "extremely": 1.8, "massive": 1.7, "severe": 1.9, "emergency": 1.8, "unprecedented": 2.0}
NEGATORS = {"not", "never", "no", "neither", "hardly", "barely", "unlikely"}

def analyze_sentiment(text: str) -> Tuple[float, str]:
    """
    Computes financial domain sentiment score S in range [-1.00, +1.00].
    Returns (score, label: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE').
    """
    if not text or not text.strip():
        return 0.0, "NEUTRAL"

    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    if not words:
        return 0.0, "NEUTRAL"

    raw_score = 0.0
    matched_count = 0
    negation_active = False
    intensity = 1.0

    for i, w in enumerate(words):
        if w in NEGATORS:
            negation_active = True
            continue
        if w in INTENSIFIERS:
            intensity = INTENSIFIERS[w]
            continue

        score = 0.0
        if w in FINANCIAL_POSITIVE:
            score = FINANCIAL_POSITIVE[w] * intensity
        elif w in FINANCIAL_NEGATIVE:
            score = FINANCIAL_NEGATIVE[w] * intensity

        if score != 0.0:
            if negation_active:
                score = -score * 0.7
                negation_active = False
            raw_score += score
            matched_count += 1
            intensity = 1.0 # reset

    if matched_count == 0:
        return 0.0, "NEUTRAL"

    # Normalize via hyperbolic tangent to bound between -1.0 and +1.0 smoothly
    normalized = math.tanh(raw_score / 3.5)
    normalized = round(max(-1.0, min(1.0, normalized)), 2)

    if normalized > 0.15:
        label = "POSITIVE"
    elif normalized < -0.15:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return normalized, label
