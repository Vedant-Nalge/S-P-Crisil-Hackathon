from typing import Tuple, List

BASE_EVENT_WEIGHTS = {
    "Credit Event": 6.2,
    "Geopolitical": 5.8,
    "Cyber / Operational Risk": 5.5,
    "Macroeconomic": 5.0,
    "Merger/Acquisition": 3.8,
    "Product Launch / Innovation": 3.2
}

SYSTEMIC_TICKERS = {"JPM", "BAC", "GS", "MSFT", "AAPL", "MACRO"}

def calculate_impact_score(
    sentiment_score: float,
    event_class: str,
    tickers: List[str]
) -> Tuple[float, bool]:
    """
    Predicts severity impact score on a calibrated scale from 1.0 to 10.0.
    Returns (impact_score, triggers_stress_test: bool).
    """
    base_weight = BASE_EVENT_WEIGHTS.get(event_class, 4.0)
    
    # Sentiment extremity bonus (more extreme negative or positive moves severity higher)
    sentiment_magnitude = abs(sentiment_score) * 3.2
    
    # Systemic entity contagion bonus
    has_systemic_entity = any(t in SYSTEMIC_TICKERS for t in tickers)
    entity_bonus = 0.8 if has_systemic_entity else 0.0

    raw_impact = base_weight + sentiment_magnitude + entity_bonus
    
    # Calibrate and clamp between 1.0 and 10.0
    impact_score = round(max(1.0, min(10.0, raw_impact)), 1)
    
    # Module B trigger rule: Impact >= 7.0 for systemic event types
    triggers_stress = (
        impact_score >= 7.0 and 
        event_class in ["Geopolitical", "Macroeconomic", "Credit Event", "Cyber / Operational Risk"]
    )
    
    return impact_score, triggers_stress
