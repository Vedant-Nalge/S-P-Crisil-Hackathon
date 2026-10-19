import re
from typing import Dict, Tuple

EVENT_TAXONOMIES: Dict[str, Dict[str, float]] = {
    "Geopolitical": {
        "war": 3.0, "military": 2.5, "sanctions": 3.0, "embargo": 2.8, "strait": 2.2, "hormuz": 2.5,
        "conflict": 2.4, "missile": 2.8, "geopolitical": 2.5, "sovereign": 1.8, "red sea": 2.8,
        "blockade": 2.6, "naval": 2.2, "national security": 2.0, "tariff": 2.2, "tariffs": 2.2,
        "russia": 3.0, "ukraine": 3.0, "rift": 2.6, "china": 2.2, "unrest": 2.5, "riots": 2.5,
        "trump": 2.0, "nato": 2.5, "iran": 2.6, "taiwan": 2.5, "border": 2.0, "diplomatic": 2.2
    },
    "Macroeconomic": {
        "fed": 2.5, "federal reserve": 3.0, "interest rate": 2.8, "rate hike": 3.0, "rate cut": 2.8,
        "cpi": 2.8, "inflation": 2.8, "treasury": 2.2, "yield": 2.2, "gdp": 2.5, "unemployment": 2.2,
        "recession": 2.5, "powell": 2.2, "central bank": 2.5, "monetary policy": 2.6, "stagflation": 3.0,
        "economy": 2.0, "indexes": 1.8, "composite": 1.8, "msci": 2.0, "oil": 1.8, "currency": 1.9
    },
    "Credit Event": {
        "default": 3.5, "defaults": 3.5, "downgrade": 3.0, "downgraded": 3.0, "credit rating": 2.8,
        "bankruptcy": 3.5, "bankrupt": 3.5, "liquidity crunch": 3.2, "cds": 2.8, "credit default swap": 3.0,
        "debt restructuring": 2.8, "insolvency": 3.2, "insolvent": 3.2, "bailout": 2.5, "non-performing": 2.4,
        "debt": 2.2, "bond": 2.0, "bonds": 2.0, "credit": 2.2, "liquidity": 2.0, "issuance": 1.9
    },
    "Merger/Acquisition": {
        "merger": 3.0, "acquisition": 3.0, "acquires": 2.8, "takeover": 3.0, "buyout": 2.8,
        "antitrust": 2.8, "doj": 2.0, "regulatory block": 2.8, "deal": 1.8, "stake": 1.5,
        "tender offer": 2.8, "breakup fee": 2.5, "pledges": 1.6, "reshuffle": 1.6
    },
    "Product Launch / Innovation": {
        "launch": 2.5, "launches": 2.5, "unveils": 2.5, "unveiled": 2.5, "breakthrough": 2.8,
        "patent": 2.4, "ai": 2.0, "quantum": 2.5, "blackwell": 2.2, "chip": 1.8, "gpu": 2.2,
        "fda approval": 3.0, "biopharma": 2.0, "platform": 1.5, "revenue": 1.8, "earnings": 2.0
    },
    "Cyber / Operational Risk": {
        "cyber": 3.0, "cyberattack": 3.2, "ransomware": 3.2, "hack": 2.8, "hacked": 2.8,
        "data breach": 3.0, "outage": 2.8, "swift": 2.4, "clearing": 2.0, "system failure": 2.8,
        "infrastructure": 1.8, "zero-day": 3.0, "settlement": 1.8
    }
}

def classify_event(text: str) -> Tuple[str, float]:
    """
    Classifies unstructured financial text into a primary event category.
    Returns (event_class, confidence_score: 0.0 - 1.0).
    """
    if not text:
        return "Macroeconomic", 0.72

    clean_text = re.sub(r"<[^>]+>", " ", text)
    lower_text = clean_text.lower()

    if "russia diesel deal" in lower_text or "ukraine rift" in lower_text:
        return "Geopolitical", 0.80

    scores: Dict[str, float] = {category: 0.0 for category in EVENT_TAXONOMIES}

    for category, keywords in EVENT_TAXONOMIES.items():
        for kw, weight in keywords.items():
            if re.search(r"\b" + re.escape(kw) + r"\b", lower_text):
                scores[category] += weight

    best_category = max(scores, key=scores.get)
    max_score = scores[best_category]

    if max_score == 0:
        return "Macroeconomic", 0.74

    # Calculate confidence as softmax-like ratio
    total = sum(scores.values())
    confidence = round(min(0.98, max(0.68, max_score / (total if total > 0 else 1.0) * 0.85 + 0.12)), 2)

    return best_category, confidence
