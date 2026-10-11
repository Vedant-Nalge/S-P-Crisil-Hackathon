import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from src.nlp.sentiment import analyze_sentiment
from src.nlp.classifier import classify_event
from src.nlp.severity import calculate_impact_score
from src.ingestion.news_fetcher import _detect_tickers

def process_unstructured_text(
    headline: str,
    text: Optional[str] = None,
    source: str = "manual_input",
    forced_tickers: Optional[List[str]] = None
) -> Dict:
    """
    Unified AI/NLP Risk Engine pipeline:
    Parses unstructured text and outputs a structured financial risk signal.
    """
    content = f"{headline}. {text}" if text else headline
    
    # 1. Entity and Ticker Detection
    tickers = forced_tickers or _detect_tickers(content)
    
    # 2. Sentiment Scoring (-1.00 to +1.00)
    sentiment_score, sentiment_label = analyze_sentiment(content)
    
    # 3. Event Classification
    event_class, confidence = classify_event(content)
    
    # 4. Impact Severity Prediction (1.0 to 10.0)
    impact_score, triggers_stress_test = calculate_impact_score(
        sentiment_score=sentiment_score,
        event_class=event_class,
        tickers=tickers
    )
    
    signal = {
        "signal_id": f"SIG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4].upper()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "headline": headline,
        "raw_text": content,
        "tickers": tickers,
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment_label,
        "event_classification": event_class,
        "impact_score": impact_score,
        "confidence": confidence,
        "triggers_stress_test": triggers_stress_test,
        "rebalance_action_required": abs(sentiment_score) >= 0.20
    }
    
    return signal
