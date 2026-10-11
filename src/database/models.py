import json
import os
import hashlib
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from src.database.db import Base, SessionLocal

def hash_password(password: str) -> str:
    # PBKDF2 HMAC SHA-256 for secure, dependency-free cryptographic hashing
    salt = "sp_crisil_2026_salt"
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False, default="portfolio_manager") # 'portfolio_manager' or 'chief_risk_officer'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RiskSignal(Base):
    __tablename__ = "risk_signals"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(String(50), unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    source = Column(String(50), nullable=False) # 'financial_news', 'stocktwits', 'replay'
    headline = Column(Text, nullable=False)
    tickers = Column(String(100), default="MACRO")
    sentiment_score = Column(Float, nullable=False)
    sentiment_label = Column(String(20), nullable=False)
    event_class = Column(String(50), nullable=False)
    impact_score = Column(Float, nullable=False)
    confidence = Column(Float, default=0.92)
    triggers_stress_test = Column(Boolean, default=False)

class RebalanceRecord(Base):
    __tablename__ = "rebalance_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    trigger_signal_id = Column(String(50), nullable=True)
    weights_json = Column(Text, nullable=False) # JSON dict of ticker -> weight
    turnover_pct = Column(Float, default=0.0)
    strategy_alpha_bps = Column(Float, default=0.0)
    notes = Column(String(255), nullable=True)

class StressTestRun(Base):
    __tablename__ = "stress_test_runs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    event_id = Column(String(50), nullable=False)
    scenario_title = Column(String(150), nullable=False)
    event_class = Column(String(50), nullable=False)
    impact_score = Column(Float, nullable=False)
    yield_shock_bps = Column(Float, nullable=False)
    spread_shock_bps = Column(Float, nullable=False)
    pd_multiplier = Column(Float, nullable=False)
    pre_valuation_usd = Column(Float, nullable=False)
    post_valuation_usd = Column(Float, nullable=False)
    total_loss_usd = Column(Float, nullable=False)
    loss_pct = Column(Float, nullable=False)
    loans_loss_usd = Column(Float, nullable=False)
    bonds_loss_usd = Column(Float, nullable=False)
    derivatives_loss_usd = Column(Float, nullable=False)

def seed_default_data():
    db = SessionLocal()
    try:
        # 1. Seed demo accounts if not exist
        if not db.query(User).filter_by(username="admin").first():
            admin_user = User(
                username="admin",
                hashed_password=hash_password("admin123"),
                role="chief_risk_officer"
            )
            db.add(admin_user)

        if not db.query(User).filter_by(username="analyst").first():
            analyst_user = User(
                username="analyst",
                hashed_password=hash_password("analyst123"),
                role="portfolio_manager"
            )
            db.add(analyst_user)

        # 2. Seed initial baseline rebalance record
        if not db.query(RebalanceRecord).first():
            initial_constituents = [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
                "JPM", "BAC", "GS", "JNJ", "PFE",
                "WMT", "PG", "XOM", "CVX", "CAT"
            ]
            equal_weight = round(1.0 / len(initial_constituents), 4)
            weights = {t: equal_weight for t in initial_constituents}
            rec = RebalanceRecord(
                trigger_signal_id="INIT-BASELINE",
                weights_json=json.dumps(weights),
                turnover_pct=0.0,
                strategy_alpha_bps=0.0,
                notes="Initial Equal-Weight Baseline Allocation"
            )
            db.add(rec)

        db.commit()
    finally:
        db.close()
