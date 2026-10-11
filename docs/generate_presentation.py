import os
import shutil
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = r"C:\Users\vedan\Downloads"
PDF_PATH = os.path.join(DOCS_DIR, "presentation.pdf")

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=landscape(letter),
    rightMargin=30, leftMargin=30,
    topMargin=25, bottomMargin=25
)

styles = getSampleStyleSheet()

# Color Palette
gold_color = colors.HexColor("#f59e0b")
slate_light = colors.HexColor("#e2e8f0")
slate_dim = colors.HexColor("#94a3b8")
blue_accent = colors.HexColor("#38bdf8")
red_accent = colors.HexColor("#ef4444")
green_accent = colors.HexColor("#10b981")

title_style = ParagraphStyle(
    'SlideTitle',
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=gold_color,
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'SlideSubtitle',
    fontName='Helvetica',
    fontSize=11,
    leading=15,
    textColor=colors.white,
    spaceAfter=10
)

body_style = ParagraphStyle(
    'SlideBody',
    fontName='Helvetica',
    fontSize=9.5,
    leading=14,
    textColor=slate_light,
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'SlideBullet',
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=slate_light,
    spaceAfter=5,
    leftIndent=10
)

header_style = ParagraphStyle(
    'SlideSectionHeader',
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=blue_accent,
    spaceAfter=6
)

def add_slide_header(title, section_tag="FINANCIAL RISK ENGINE - TRUMP-RUSSIA CRISIS SIMULATION"):
    story.append(Paragraph(f"<font color='#f59e0b' size='8'><b>{section_tag}</b></font>", body_style))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 6))

story = []

# --- SLIDE 1: TITLE SLIDE ---
story.append(Spacer(1, 15))
story.append(Paragraph("FINANCIAL RISK ENGINE & QUANTITATIVE INTELLIGENCE PLATFORM", ParagraphStyle('TopTag', fontName='Helvetica-Bold', fontSize=12, textColor=gold_color, spaceAfter=10)))
story.append(Paragraph("Unified AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform", title_style))
story.append(Paragraph("Live Crisis Simulation: Trump-Russia Diesel Deal Deepens Ukraine Rift (Severity 9.6/10)", subtitle_style))
story.append(Spacer(1, 15))

meta_data = [
    [Paragraph("<b>Candidate Name:</b> Vedant Dilip Nalge", body_style), Paragraph("<b>Target Track:</b> AI/NLP Risk Engine", body_style)],
    [Paragraph("<b>Institution / Campus:</b> Indian Institute of Technology Madras", body_style), Paragraph("<b>Email:</b> me22b162@smail.iitm.ac.in", body_style)],
    [Paragraph("<b>Architecture:</b> FastAPI + Loughran-McDonald/FinBERT + SciPy", body_style), Paragraph("<b>Downstream Modules:</b> Both Module A & Module B", body_style)]
]
t = Table(meta_data, colWidths=[370, 370])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(Spacer(1, 15))

hero_img = os.path.join(DOCS_DIR, "trump_russia_hero.png")
if os.path.exists(hero_img):
    story.append(Image(hero_img, width=680, height=220))

story.append(PageBreak())

# --- SLIDE 2: PROBLEM & APPROACH ---
add_slide_header("Executive Summary & Core Challenge: Geopolitical Disruption")
col1 = [
    Paragraph("The Market Friction & Problem:", header_style),
    Paragraph("• <b>Latency Vulnerability:</b> Traditional credit risk and rating revisions take weeks to register qualitative geopolitical rifts.", bullet_style),
    Paragraph("• <b>Black Swan Shock:</b> The simulated Bloomberg wire: <i>'Trump\\'s Russia Diesel Deal Deepens Ukraine Rift'</i> causes immediate risk-off across tech/defense.", bullet_style),
    Paragraph("• <b>Dual Downstream Need:</b> Institutional desks need simultaneous equity rebalancing and wholesale banking capital preservation.", bullet_style),
    Spacer(1, 8),
    Paragraph("Our Algorithmic Architecture:", header_style),
    Paragraph("• <b>Domain NLP Pipeline:</b> Sub-25ms FinBERT/Loughran-McDonald hybrid scorer generates sentiment (-0.95) and severity (9.6/10).", bullet_style),
    Paragraph("• <b>Module A Index Tactical:</b> Bounded convex rebalance protects capital with 18% position caps.", bullet_style),
    Paragraph("• <b>Module B Wholesale Stress:</b> Basel III Expected Loss, duration convexity, and DV01 quantify balance sheet drawdowns.", bullet_style)
]

feed_img = os.path.join(DOCS_DIR, "trump_russia_news_feed.png")
col2 = []
if os.path.exists(feed_img):
    col2.append(Paragraph("<b>Live Multi-Source Ingestion Telemetry:</b>", header_style))
    col2.append(Image(feed_img, width=360, height=260))

summary_table = Table([[col1, col2]], colWidths=[370, 370])
summary_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(summary_table)
story.append(PageBreak())

# --- SLIDE 3: SYSTEM ARCHITECTURE ---
add_slide_header("System Design & Architecture: Multi-Source Real-Time Pipeline")
arch_data = [
    [Paragraph("<b>Component Layer</b>", header_style), Paragraph("<b>Implementation & Technologies</b>", header_style), Paragraph("<b>Trump-Russia Case Telemetry</b>", header_style)],
    [Paragraph("1. Data Ingestion", body_style), Paragraph("Yahoo Finance RSS, StockTwits streams, Bloomberg wire simulator", body_style), Paragraph("Extracted headline + ticker mentions AAPL, NVDA, PLTR, TSLA", body_style)],
    [Paragraph("2. AI/NLP Classifier", body_style), Paragraph("Dual-dictionary FinBERT & Loughran-McDonald keyword density", body_style), Paragraph("Geopolitical class (80% conf), -0.95 Sentiment (Deep Bearish)", body_style)],
    [Paragraph("3. Severity Gate", body_style), Paragraph("Rule-based impact weighting (Score >= 7.0 auto-trips Module B)", body_style), Paragraph("Impact Score: <b>9.6 / 10.0 (GATE TRIPPED)</b>", body_style)],
    [Paragraph("4. Module A Rebalance", body_style), Paragraph("Convex bounded optimizer with 18% upper cap & turnover penalty", body_style), Paragraph("Underweights TSLA (1.14%), AMZN (1.19%); +5 bps net alpha", body_style)],
    [Paragraph("5. Module B Stress Test", body_style), Paragraph("Basel III Expected Loss + Duration/Convexity + DV01 sensitivity", body_style), Paragraph("Yield shock +104 bps, Spread +351 bps, PD 2.52x, -$206.4M loss", body_style)],
    [Paragraph("6. Persistence & UI", body_style), Paragraph("FastAPI, SQLite WAL mode, Chart.js glassmorphic dashboard", body_style), Paragraph("Sub-25ms response time; zero external API dependencies", body_style)]
]
arch_table = Table(arch_data, colWidths=[150, 310, 280])
arch_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#020617")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(arch_table)
story.append(PageBreak())

# --- SLIDE 4: TELEMETRY & SEVERITY GATE ---
add_slide_header("AI/NLP Telemetry & Automated Severity Gate Execution")
telem_col1 = [
    Paragraph("Simulated Shock Details:", header_style),
    Paragraph("• <b>Headline:</b> <i>'Trump\\'s Russia Diesel Deal Deepens Ukraine Rift'</i>", body_style),
    Paragraph("• <b>Event Classification:</b> <b>Geopolitical</b> (80% confidence)", body_style),
    Paragraph("• <b>Sentiment Polarization:</b> <b>-0.95</b> (Extreme Risk-Off / Deep Bearish)", body_style),
    Paragraph("• <b>Severity Impact Score:</b> <font color='#ef4444'><b>9.6 / 10.0 (Systemic Crisis)</b></font>", body_style),
    Spacer(1, 6),
    Paragraph("Automated Pipeline Tripwire:", header_style),
    Paragraph("• The platform enforces an automatic threshold gate (Impact >= 7.0) for systemic classes (Geopolitical, Macro, Credit, Cyber).", bullet_style),
    Paragraph("• Real-time signal toast immediately dispatches shock parameters (Δy = +104 bps, Δs = +351 bps, PD = 2.52x) directly to downstream wholesale banking calculators.", bullet_style)
]

telem_img = os.path.join(DOCS_DIR, "trump_russia_telemetry.png")
telem_col2 = []
if os.path.exists(telem_img):
    telem_col2.append(Image(telem_img, width=380, height=270))

telem_table = Table([[telem_col1, telem_col2]], colWidths=[350, 390])
telem_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(telem_table)
story.append(PageBreak())

# --- SLIDE 5: MODULE A RESULTS ---
add_slide_header("Downstream Module A: Real-Time Tactical Index Rebalancing")
mod_a_col1 = [
    Paragraph("Tactical Rebalance Allocation Results:", header_style),
    Paragraph("• <b>Defensive Caps (18.87% ceiling):</b> MSFT, GOOGL, JPM maxed at protective ceilings.", bullet_style),
    Paragraph("• <b>Vulnerable De-allocations:</b> TSLA slashed to <b>1.14%</b>, AMZN reduced to <b>1.19%</b>.", bullet_style),
    Paragraph("• <b>Strategy Alpha:</b> Achieved <b>+5.00 bps alpha</b> during extreme turbulence.", bullet_style),
    Paragraph("• <b>Controlled Turnover:</b> Kept turnover to <b>9.49%</b> to prevent transaction cost slippage.", bullet_style),
    Paragraph("• <b>Sector Distribution:</b> Technology 51.5%, Energy 11.8%, Financials 18.9%, Healthcare 17.8%.", bullet_style)
]

mod_a_img = os.path.join(DOCS_DIR, "trump_russia_module_a.png")
mod_a_col2 = []
if os.path.exists(mod_a_img):
    mod_a_col2.append(Image(mod_a_img, width=420, height=270))

mod_a_table = Table([[mod_a_col1, mod_a_col2]], colWidths=[310, 430])
mod_a_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(mod_a_table)
story.append(PageBreak())

# --- SLIDE 6: MODULE B RESULTS ---
add_slide_header("Downstream Module B: Wholesale Banking Stress Testing ($1.0B Book)")
mod_b_col1 = [
    Paragraph("Wholesale Portfolio Stress Simulation:", header_style),
    Paragraph("• <b>Baseline Valuation:</b> $1,000.0M ($1.0 Billion wholesale book).", bullet_style),
    Paragraph("• <b>Simulated Yield Shock:</b> Δy = <b>+104 bps</b> | Spread Shock: Δs = <b>+351 bps</b>.", bullet_style),
    Paragraph("• <b>Default Multiplier:</b> Corporate PD jumped <b>2.52x</b>.", bullet_style),
    Paragraph("• <b>Total Stressed Capital Loss:</b> <font color='#ef4444'><b>-$206.4M (-20.64%)</b></font>", bullet_style),
    Paragraph("• <b>Post-Stress Valuation:</b> <font color='#10b981'><b>$793.6M (79.36% Capital Preserved)</b></font>", bullet_style),
    Paragraph("• <b>Sub-Portfolio Impact Breakdown:</b> Commercial Loans -$95.2M (Basel III EL), Bond Portfolio -$78.4M (Duration/Convexity), IRS Swaps -$32.8M (DV01).", bullet_style)
]

mod_b_img = os.path.join(DOCS_DIR, "trump_russia_module_b.png")
mod_b_col2 = []
if os.path.exists(mod_b_img):
    mod_b_col2.append(Image(mod_b_img, width=420, height=270))

mod_b_table = Table([[mod_b_col1, mod_b_col2]], colWidths=[310, 430])
mod_b_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(mod_b_table)
story.append(PageBreak())

# --- SLIDE 7: BUSINESS IMPACT, AI COPILOT & ROADMAP ---
add_slide_header("Institutional Domain Impact, RiskPulse AI Copilot & Strategic Roadmap")

s7_col1 = []
copilot_pdf_img = os.path.join(DOCS_DIR, "trump_russia_copilot.png")
if os.path.exists(copilot_pdf_img):
    s7_col1.append(Paragraph("<b>RiskPulse AI Copilot (Live Advisory):</b>", header_style))
    s7_col1.append(Image(copilot_pdf_img, width=220, height=282))

s7_col2 = [
    Paragraph("Enterprise Value Proposition:", header_style),
]
impact_data = [
    [Paragraph("<b>Institutional Persona</b>", header_style), Paragraph("<b>Pre-Engine State</b>", header_style), Paragraph("<b>With Risk Engine Platform</b>", header_style)],
    [Paragraph("Chief Risk Officer (CRO)", body_style), Paragraph("Lagged quarterly reports, 2-3 wk turnaround on black swans", body_style), Paragraph("Instant sub-second Basel III balance sheet capital re-appraisal", body_style)],
    [Paragraph("Quant Portfolio Mgr", body_style), Paragraph("Emotional panic selling or delayed rebalancing on shock news", body_style), Paragraph("Algorithmic bounded convex reallocation generating +5 bps alpha", body_style)],
    [Paragraph("Treasury & Balance Desk", body_style), Paragraph("Opaque duration and credit spread mismatch under shocks", body_style), Paragraph("Real-time DV01 and spread sensitivity across multi-asset books", body_style)]
]
impact_table = Table(impact_data, colWidths=[130, 185, 195])
impact_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#020617")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
s7_col2.append(impact_table)
s7_col2.append(Spacer(1, 6))

s7_col2.append(Paragraph("Target Engineering Roadmap:", header_style))
roadmap_data = [
    [Paragraph("<b>Milestone</b>", header_style), Paragraph("<b>Objective</b>", header_style), Paragraph("<b>Horizon</b>", header_style)],
    [Paragraph("Phase 1 (Done)", body_style), Paragraph("Unified NLP pipeline, dual downstream Module A & B, AI copilot", body_style), Paragraph("Live MVP", body_style)],
    [Paragraph("Phase 2", body_style), Paragraph("Scale constituent universe from 15 S&P names to full S&P 500 & Russell 2000", body_style), Paragraph("Q2 2026", body_style)],
    [Paragraph("Phase 3", body_style), Paragraph("FIX Protocol integration for direct DMA broker execution and automated hedging", body_style), Paragraph("Q3 2026", body_style)],
    [Paragraph("Phase 4", body_style), Paragraph("Quarterly 10-K multimodal document ingestion and automated risk memos", body_style), Paragraph("Q4 2026", body_style)]
]
roadmap_table = Table(roadmap_data, colWidths=[105, 315, 90])
roadmap_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#020617")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
s7_col2.append(roadmap_table)

s7_layout = Table([[s7_col1, s7_col2]], colWidths=[230, 510])
s7_layout.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(s7_layout)

doc.build(story)
print(f"Presentation deck successfully created at {PDF_PATH}")

# Copy to downloads
for dest_name in ["presentation.pdf", "IITM_Vedant_Nalge_Presentation.pdf", "IITM_Vedant_Nalge_Trump_Russia_Deck.pdf"]:
    dest = os.path.join(DOWNLOADS_DIR, dest_name)
    try:
        shutil.copyfile(PDF_PATH, dest)
        print(f"Saved to {dest}")
    except PermissionError:
        alt_dest = dest.replace(".pdf", "_v2.pdf")
        shutil.copyfile(PDF_PATH, alt_dest)
        print(f"File locked, saved to {alt_dest}")
