import os
import json
from typing import Dict, Optional
from src.database.db import SessionLocal
from src.database.models import StressTestRun

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PORTFOLIO_FILE = os.path.join(BASE_DIR, "data", "wholesale_portfolio.json")

DEFAULT_SHOCKS = {
    "Geopolitical": {"yield_shock_bps": 75, "spread_shock_bps": 150, "pd_multiplier": 1.65},
    "Macroeconomic": {"yield_shock_bps": 150, "spread_shock_bps": 85, "pd_multiplier": 1.35},
    "Credit Event": {"yield_shock_bps": -40, "spread_shock_bps": 320, "pd_multiplier": 2.50},
    "Cyber / Operational Risk": {"yield_shock_bps": 15, "spread_shock_bps": 140, "pd_multiplier": 1.50},
    "Merger/Acquisition": {"yield_shock_bps": 0, "spread_shock_bps": 35, "pd_multiplier": 1.10},
    "Product Launch / Innovation": {"yield_shock_bps": 5, "spread_shock_bps": -20, "pd_multiplier": 0.95}
}

def load_portfolio_data() -> Dict:
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return {"loans": [], "bonds": [], "derivatives": [], "summary": {}}

def run_stress_test(
    event_id: str,
    scenario_title: str,
    event_class: str,
    impact_score: float,
    custom_yield_bps: Optional[float] = None,
    custom_spread_bps: Optional[float] = None,
    custom_pd_mult: Optional[float] = None
) -> Dict:
    """
    Module B: Strategic Wholesale Banking Portfolio Stress Testing
    Applies multi-factor macro/credit shocks across loans, bonds, and derivatives books.
    """
    portfolio = load_portfolio_data()
    loans = portfolio.get("loans", [])
    bonds = portfolio.get("bonds", [])
    derivatives = portfolio.get("derivatives", [])

    # Determine shocks
    shock_params = DEFAULT_SHOCKS.get(event_class, {"yield_shock_bps": 50, "spread_shock_bps": 100, "pd_multiplier": 1.25})
    
    if custom_yield_bps is not None and custom_spread_bps is not None:
        eff_yield_bps = float(custom_yield_bps)
        eff_spread_bps = float(custom_spread_bps)
        eff_pd_mult = float(custom_pd_mult if custom_pd_mult is not None else 1.25)
    else:
        severity_scaler = max(0.5, impact_score / 7.0)
        eff_yield_bps = shock_params["yield_shock_bps"] * severity_scaler
        eff_spread_bps = shock_params["spread_shock_bps"] * severity_scaler
        eff_pd_mult = 1.0 + (shock_params["pd_multiplier"] - 1.0) * severity_scaler

    # 1. Commercial Loans Stress Valuation (Basel Expected Loss Framework)
    pre_loans_el = 0.0
    post_loans_el = 0.0
    loans_total_principal = 0.0

    for ln in loans:
        p = ln["principal_usd"]
        loans_total_principal += p
        pd_base = ln["pd_baseline"]
        lgd = ln["lgd_baseline"]
        
        pre_loans_el += p * pd_base * lgd
        stressed_pd = min(0.99, pd_base * eff_pd_mult)
        stressed_lgd = min(0.95, lgd * (1.0 + 0.25 * max(0.0, eff_pd_mult - 1.0)))
        post_loans_el += p * stressed_pd * stressed_lgd

    migration_factor = max(1.0, eff_pd_mult ** 1.35) if eff_pd_mult >= 1.0 else 0.8
    loans_loss = max(0.0, (post_loans_el - pre_loans_el) * migration_factor)
    pre_loans_val = loans_total_principal
    post_loans_val = max(0.0, loans_total_principal - loans_loss)

    # 2. Corporate Fixed-Rate Bonds Stress Valuation (Duration-Convexity Model)
    total_effective_rate_shock = (eff_yield_bps + eff_spread_bps) / 10000.0 # to decimal
    bonds_total_par = 0.0
    bonds_loss = 0.0

    for bd in bonds:
        par = bd["par_value_usd"]
        bonds_total_par += par
        d_mod = bd["modified_duration"]
        cvx = bd["convexity"]
        
        # Bond price change: dP/P ~ -D * dy + 0.5 * C * dy^2
        pct_price_chg = -d_mod * total_effective_rate_shock + 0.5 * cvx * (total_effective_rate_shock ** 2)
        bond_loss_item = -pct_price_chg * par
        bonds_loss += bond_loss_item

    pre_bonds_val = bonds_total_par
    post_bonds_val = max(0.0, bonds_total_par - bonds_loss)

    # 3. Derivatives MTM Shock (DV01 Dollar Sensitivity)
    derivatives_loss = 0.0
    pre_deriv_mtm = 0.0
    for dr in derivatives:
        pre_deriv_mtm += dr["current_mtm_usd"]
        # DV01 is gain/loss per 1 bp change
        derivatives_loss += dr["dv01_usd"] * eff_yield_bps

    # 4. Total Wholesale Portfolio Aggregation
    pre_total_val = pre_loans_val + pre_bonds_val
    total_loss = loans_loss + bonds_loss + derivatives_loss
    post_total_val = max(0.0, pre_total_val - total_loss)
    loss_pct = round((total_loss / pre_total_val) * 100, 2) if pre_total_val > 0 else 0.0

    # Save run audit into database
    db = SessionLocal()
    try:
        run = StressTestRun(
            event_id=event_id,
            scenario_title=scenario_title,
            event_class=event_class,
            impact_score=round(impact_score, 1),
            yield_shock_bps=round(eff_yield_bps, 1),
            spread_shock_bps=round(eff_spread_bps, 1),
            pd_multiplier=round(eff_pd_mult, 2),
            pre_valuation_usd=round(pre_total_val, 2),
            post_valuation_usd=round(post_total_val, 2),
            total_loss_usd=round(total_loss, 2),
            loss_pct=loss_pct,
            loans_loss_usd=round(loans_loss, 2),
            bonds_loss_usd=round(bonds_loss, 2),
            derivatives_loss_usd=round(derivatives_loss, 2)
        )
        db.add(run)
        db.commit()
    finally:
        db.close()

    return {
        "event_id": event_id,
        "scenario_title": scenario_title,
        "event_class": event_class,
        "impact_score": impact_score,
        "shocks_applied": {
            "yield_shock_bps": round(eff_yield_bps, 1),
            "spread_shock_bps": round(eff_spread_bps, 1),
            "pd_multiplier": round(eff_pd_mult, 2)
        },
        "valuations": {
            "pre_total_valuation_usd": round(pre_total_val, 2),
            "post_total_valuation_usd": round(post_total_val, 2),
            "total_loss_usd": round(total_loss, 2),
            "loss_pct": loss_pct
        },
        "breakdown": {
            "loans": {
                "pre_val": round(pre_loans_val, 2),
                "loss": round(loans_loss, 2),
                "post_val": round(post_loans_val, 2)
            },
            "bonds": {
                "pre_val": round(pre_bonds_val, 2),
                "loss": round(bonds_loss, 2),
                "post_val": round(post_bonds_val, 2)
            },
            "derivatives": {
                "loss": round(derivatives_loss, 2)
            }
        }
    }
