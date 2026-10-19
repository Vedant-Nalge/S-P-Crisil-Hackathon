import os
import json
from typing import Optional, List, Dict
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, RiskSignal, RebalanceRecord, StressTestRun, hash_password
from src.auth.security import create_access_token, get_current_user, require_cro_role
from src.ingestion.news_fetcher import fetch_live_financial_news
from src.ingestion.social_fetcher import fetch_live_social_stream
from src.ingestion.replay_engine import load_replay_scenarios, get_scenario_by_id
from src.nlp.engine import process_unstructured_text
from src.modules.module_a import rebalance_index, get_market_quotes, get_latest_weights
from src.modules.module_b import run_stress_test, load_portfolio_data

api_router = APIRouter(prefix="/api")

# --- AUTH SCHEMAS & ROUTES ---
class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "portfolio_manager"

@api_router.post("/auth/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    clean_username = req.username.strip().lower()
    if len(clean_username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(req.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")

    existing = db.query(User).filter_by(username=clean_username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists. Please choose another or log in.")

    valid_role = "chief_risk_officer" if req.role in ["chief_risk_officer", "cro", "admin"] else "portfolio_manager"
    
    new_user = User(
        username=clean_username,
        hashed_password=hash_password(req.password),
        role=valid_role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": new_user.username,
        "role": new_user.role,
        "message": "Account created successfully"
    }

@api_router.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    clean_username = req.username.strip().lower()
    user = db.query(User).filter_by(username=clean_username).first()
    if not user or user.hashed_password != hash_password(req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"sub": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }

@api_router.get("/auth/me")
def get_me(user: dict = Depends(get_current_user)):
    return user

# --- RISK ENGINE ROUTES ---
class TextAnalysisRequest(BaseModel):
    headline: str
    text: Optional[str] = None
    source: Optional[str] = "manual_analyst_entry"
    tickers: Optional[List[str]] = None

@api_router.post("/risk/analyze")
def analyze_text(req: TextAnalysisRequest, db: Session = Depends(get_db)):
    signal = process_unstructured_text(
        headline=req.headline,
        text=req.text,
        source=req.source,
        forced_tickers=req.tickers
    )
    
    # Store in database
    db_signal = RiskSignal(
        signal_id=signal["signal_id"],
        source=signal["source"],
        headline=signal["headline"],
        tickers=",".join(signal["tickers"]),
        sentiment_score=signal["sentiment_score"],
        sentiment_label=signal["sentiment_label"],
        event_class=signal["event_classification"],
        impact_score=signal["impact_score"],
        confidence=signal["confidence"],
        triggers_stress_test=signal["triggers_stress_test"]
    )
    db.add(db_signal)
    db.commit()

    return signal

@api_router.get("/risk/signals")
def get_signals(limit: int = 20, db: Session = Depends(get_db)):
    signals = db.query(RiskSignal).order_by(RiskSignal.id.desc()).limit(limit).all()
    return [
        {
            "signal_id": s.signal_id,
            "timestamp": s.timestamp.isoformat() if s.timestamp else "",
            "source": s.source,
            "headline": s.headline,
            "tickers": s.tickers.split(",") if s.tickers else ["MACRO"],
            "sentiment_score": s.sentiment_score,
            "sentiment_label": s.sentiment_label,
            "event_classification": s.event_class,
            "impact_score": s.impact_score,
            "confidence": s.confidence,
            "triggers_stress_test": s.triggers_stress_test
        }
        for s in signals
    ]

@api_router.get("/risk/live-news")
def get_live_news(limit: int = 15, source: str = "ALL"):
    return fetch_live_financial_news(limit=limit, source_filter=source)

@api_router.get("/risk/live-social")
def get_live_social(ticker: str = "ALL", limit: int = 16, platform: str = "ALL"):
    return fetch_live_social_stream(ticker=ticker, limit=limit, platform=platform)

@api_router.get("/risk/replay-scenarios")
def get_scenarios():
    return load_replay_scenarios()

class TriggerReplayRequest(BaseModel):
    event_id: str
    auto_trigger_downstream: bool = True

@api_router.post("/risk/trigger-replay")
def trigger_replay(req: TriggerReplayRequest, db: Session = Depends(get_db)):
    scenario = get_scenario_by_id(req.event_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Ingest news component
    signal = process_unstructured_text(
        headline=scenario["source_news"],
        source="replay_engine",
        forced_tickers=scenario["primary_tickers"]
    )
    # Ensure calibrated targets
    signal["event_classification"] = scenario["true_event_class"]
    signal["impact_score"] = scenario["target_impact"]
    signal["sentiment_score"] = scenario["target_sentiment"]
    signal["triggers_stress_test"] = scenario["target_impact"] >= 7.0

    db_signal = RiskSignal(
        signal_id=signal["signal_id"],
        source="replay_crisis_feed",
        headline=scenario["title"],
        tickers=",".join(scenario["primary_tickers"]),
        sentiment_score=signal["sentiment_score"],
        sentiment_label=signal["sentiment_label"],
        event_class=signal["event_classification"],
        impact_score=signal["impact_score"],
        confidence=0.96,
        triggers_stress_test=signal["triggers_stress_test"]
    )
    db.add(db_signal)
    db.commit()

    rebalance_result = None
    stress_result = None

    if req.auto_trigger_downstream:
        # Module A rebalance
        sentiment_map = {t: signal["sentiment_score"] for t in scenario["primary_tickers"]}
        rebalance_result = rebalance_index(sentiment_map, trigger_signal_id=signal["signal_id"])

        # Module B stress test for scenario
        shocks = scenario.get("shocks", {})
        stress_result = run_stress_test(
            event_id=scenario["event_id"],
            scenario_title=scenario["title"],
            event_class=scenario["true_event_class"],
            impact_score=scenario["target_impact"],
            custom_yield_bps=shocks.get("yield_shock_bps"),
            custom_spread_bps=shocks.get("spread_shock_bps"),
            custom_pd_mult=shocks.get("pd_multiplier")
        )

    return {
        "scenario": scenario,
        "signal": signal,
        "rebalance_result": rebalance_result,
        "stress_result": stress_result
    }

# --- MODULE A: TACTICAL REBALANCER ROUTES ---
@api_router.get("/rebalance/quotes")
def get_quotes():
    return get_market_quotes()

@api_router.get("/rebalance/weights")
def get_weights():
    return get_latest_weights()

class RebalanceExecuteRequest(BaseModel):
    sentiment_adjustments: Dict[str, float]
    sensitivity: Optional[float] = 0.05

@api_router.post("/rebalance/execute")
def execute_rebalance(req: RebalanceExecuteRequest):
    return rebalance_index(req.sentiment_adjustments, sensitivity_k=req.sensitivity)

@api_router.get("/rebalance/history")
def get_rebalance_history(limit: int = 10, db: Session = Depends(get_db)):
    records = db.query(RebalanceRecord).order_by(RebalanceRecord.id.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat() if r.timestamp else "",
            "trigger_signal_id": r.trigger_signal_id,
            "weights": json.loads(r.weights_json) if r.weights_json else {},
            "turnover_pct": r.turnover_pct,
            "strategy_alpha_bps": r.strategy_alpha_bps,
            "notes": r.notes
        }
        for r in records
    ]

# --- MODULE B: WHOLESALE STRESS TEST ROUTES ---
@api_router.get("/stress/portfolio")
def get_portfolio():
    return load_portfolio_data()

class StressSimulateRequest(BaseModel):
    event_id: Optional[str] = "MANUAL-STRESS"
    scenario_title: Optional[str] = "Manual Stress Simulation"
    event_class: str = "Geopolitical"
    impact_score: float = 7.5
    yield_shock_bps: Optional[float] = None
    spread_shock_bps: Optional[float] = None
    pd_multiplier: Optional[float] = None

@api_router.post("/stress/simulate")
def simulate_stress(req: StressSimulateRequest):
    return run_stress_test(
        event_id=req.event_id or "MANUAL-STRESS",
        scenario_title=req.scenario_title or "Custom Stress Test",
        event_class=req.event_class,
        impact_score=req.impact_score,
        custom_yield_bps=req.yield_shock_bps,
        custom_spread_bps=req.spread_shock_bps,
        custom_pd_mult=req.pd_multiplier
    )

@api_router.get("/stress/history")
def get_stress_history(limit: int = 10, db: Session = Depends(get_db)):
    runs = db.query(StressTestRun).order_by(StressTestRun.id.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat() if r.timestamp else "",
            "event_id": r.event_id,
            "scenario_title": r.scenario_title,
            "event_class": r.event_class,
            "impact_score": r.impact_score,
            "shocks": {
                "yield_bps": r.yield_shock_bps,
                "spread_bps": r.spread_shock_bps,
                "pd_multiplier": r.pd_multiplier
            },
            "pre_valuation": r.pre_valuation_usd,
            "post_valuation": r.post_valuation_usd,
            "total_loss": r.total_loss_usd,
            "loss_pct": r.loss_pct,
            "breakdown": {
                "loans_loss": r.loans_loss_usd,
                "bonds_loss": r.bonds_loss_usd,
                "derivatives_loss": r.derivatives_loss_usd
            }
        }
        for r in runs
    ]

# --- AI COPILOT CHATBOT & CONTAGION ROUTES ---
from src.nlp.copilot import chat_with_risk_copilot

class ChatbotRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []
    portfolio_context: Optional[Dict] = None
    api_key: Optional[str] = None
    image_data: Optional[str] = None
    image_mime: Optional[str] = "image/png"

@api_router.post("/copilot/chat")
def copilot_chat(req: ChatbotRequest):
    return chat_with_risk_copilot(
        message=req.message,
        conversation_history=req.history,
        portfolio_context=req.portfolio_context,
        api_key=req.api_key,
        image_data=req.image_data,
        image_mime=req.image_mime or "image/png"
    )

@api_router.get("/contagion/simulate")
def contagion_simulate(
    primary_sector: str = "Financials",
    initial_loss_m: float = 350.0,
    rounds: int = 3,
    damping_factor: float = 0.65
):
    """
    Dynamic Multi-Round Systemic Network Contagion Engine.
    Simulates iterative counterparty default cascades across bilateral credit exposures
    using an Eisenberg-Noe / Leontief inter-sectoral clearing network model with
    node-specific equity/capital buffer thresholds.
    """
    contagion_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "contagion.json")
    if not os.path.exists(contagion_path):
        return {"error": "Contagion data file not found"}
    with open(contagion_path, "r", encoding="utf-8") as f:
        cdata = json.load(f)

    raw_nodes = cdata.get("networkNodes", [])
    matrix = cdata.get("matrix", {})
    transmission_channels = cdata.get("transmissionChannels", {})

    node_dict = {}
    for n in raw_nodes:
        nid = n["id"]
        node_dict[nid] = {
            **n,
            "roundLosses": [0.0] * (rounds + 1),
            "totalLossM": 0.0,
            "remainingEquityM": float(n.get("equityBufferM", 300)),
            "capitalDepletedPct": 0.0,
            "isDefaulted": False,
            "status": "HEALTHY",
            "isTriggered": False
        }

    if primary_sector not in node_dict:
        primary_sector = "Financials"

    # Round 0: Direct External Shock at Epicenter
    node_dict[primary_sector]["roundLosses"][0] = initial_loss_m
    node_dict[primary_sector]["totalLossM"] = initial_loss_m
    node_dict[primary_sector]["isTriggered"] = True
    
    eq = node_dict[primary_sector]["equityBufferM"]
    node_dict[primary_sector]["remainingEquityM"] = max(0.0, round(eq - initial_loss_m, 1))
    depleted_pct = min(100.0, round((initial_loss_m / eq) * 100, 1))
    node_dict[primary_sector]["capitalDepletedPct"] = depleted_pct
    if initial_loss_m >= eq:
        node_dict[primary_sector]["isDefaulted"] = True
        node_dict[primary_sector]["status"] = "INSOLVENT / DEFAULTED"
    elif depleted_pct >= 60.0:
        node_dict[primary_sector]["status"] = "DISTRESSED"
    else:
        node_dict[primary_sector]["status"] = "STRESSED"

    propagation_logs = []
    active_transmissions = []
    round_totals = [initial_loss_m] + [0.0] * rounds

    # Iterative Cascade Simulation across rounds r = 1..rounds
    for r in range(1, rounds + 1):
        prev_round = r - 1
        current_round_loss_sum = 0.0

        for src_id, src_node in node_dict.items():
            prev_loss = src_node["roundLosses"][prev_round]
            if prev_loss <= 0.1:
                continue

            # Transmission multiplier: defaulted nodes dump higher distressed liquidity shocks
            distress_amplifier = 1.35 if src_node["isDefaulted"] else 1.0
            src_matrix = matrix.get(src_id, {})

            for tgt_id, exposure_weight in src_matrix.items():
                if tgt_id == src_id or exposure_weight <= 0.0:
                    continue

                # Mathematical transmission: Loss_trans = Loss_prev * exposure_weight * damping^r * amplifier
                effective_damping = (damping_factor ** r)
                transmitted = round(prev_loss * exposure_weight * effective_damping * distress_amplifier, 1)

                if transmitted >= 0.5:
                    node_dict[tgt_id]["roundLosses"][r] = round(node_dict[tgt_id]["roundLosses"][r] + transmitted, 1)
                    node_dict[tgt_id]["totalLossM"] = round(node_dict[tgt_id]["totalLossM"] + transmitted, 1)
                    node_dict[tgt_id]["isTriggered"] = True
                    current_round_loss_sum += transmitted

                    # Update capital buffer of target
                    tgt_eq = node_dict[tgt_id]["equityBufferM"]
                    tgt_tot_loss = node_dict[tgt_id]["totalLossM"]
                    node_dict[tgt_id]["remainingEquityM"] = max(0.0, round(tgt_eq - tgt_tot_loss, 1))
                    tgt_dep_pct = min(100.0, round((tgt_tot_loss / tgt_eq) * 100, 1))
                    node_dict[tgt_id]["capitalDepletedPct"] = tgt_dep_pct

                    if tgt_tot_loss >= tgt_eq:
                        node_dict[tgt_id]["isDefaulted"] = True
                        node_dict[tgt_id]["status"] = "INSOLVENT / DEFAULTED"
                    elif tgt_dep_pct >= 60.0:
                        node_dict[tgt_id]["status"] = "DISTRESSED"
                    elif tgt_dep_pct >= 25.0:
                        node_dict[tgt_id]["status"] = "STRESSED"

                    channel_desc = transmission_channels.get(f"{src_id}->{tgt_id}", f"Inter-sector wholesale credit and counterparty exposure from {src_id} to {tgt_id}")
                    active_transmissions.append({
                        "round": r,
                        "source": src_id,
                        "target": tgt_id,
                        "transmittedLossM": transmitted,
                        "exposureWeight": exposure_weight,
                        "channel": channel_desc
                    })

        round_totals[r] = round(current_round_loss_sum, 1)
        propagation_logs.append({
            "round": r,
            "roundLossM": round(current_round_loss_sum, 1),
            "description": f"Round {r} cascade generated ${round(current_round_loss_sum, 1)}M across counterparty balance sheets."
        })

    first_order_total = initial_loss_m
    second_order_total = round_totals[1] if rounds >= 1 else 0.0
    third_plus_order_total = round(sum(round_totals[2:]), 1) if rounds >= 2 else 0.0
    grand_total = round(sum(round_totals), 1)

    # Executive memo generation
    defaulted_nodes = [n["label"] for n in node_dict.values() if n["isDefaulted"]]
    distressed_nodes = [n["label"] for n in node_dict.values() if n["status"] == "DISTRESSED"]

    return {
        "primary_sector": primary_sector,
        "initial_loss_m": initial_loss_m,
        "first_order_total_m": first_order_total,
        "second_order_total_m": second_order_total,
        "third_plus_order_total_m": third_plus_order_total,
        "grand_total_m": grand_total,
        "rounds_executed": rounds,
        "round_totals": round_totals,
        "nodes": list(node_dict.values()),
        "active_transmissions": active_transmissions,
        "propagation_logs": propagation_logs,
        "defaulted_nodes": defaulted_nodes,
        "distressed_nodes": distressed_nodes,
        "risk_committee_memo": {
            "title": f"RISK COMMITTEE EXECUTIVE BRIEF // SECTOR EPICENTER: {primary_sector.upper()}",
            "situation": f"Direct initial liquidity shock of ${initial_loss_m}M in {primary_sector} propagated across {rounds} systemic clearing rounds.",
            "exposure_hit": f"Second-order spillover generated ${second_order_total}M; multi-hop cascade added ${third_plus_order_total}M in downstream losses.",
            "capital_impact": f"Total systemic capital at risk stands at ${grand_total}M. " + (f"Severe insolvencies triggered in: {', '.join(defaulted_nodes)}." if defaulted_nodes else "All sectors maintained minimum solvent equity buffers."),
            "recommended_actions": [
                "Activate Basel III emergency capital conservation buffers across affected subsidiaries.",
                "Execute bilateral counterparty novation and mandatory daily VM/IM cash variation margins.",
                f"Initiate priority ring-fencing on {' & '.join(distressed_nodes) if distressed_nodes else primary_sector} exposures to halt hop-3 contagion."
            ]
        }
    }
