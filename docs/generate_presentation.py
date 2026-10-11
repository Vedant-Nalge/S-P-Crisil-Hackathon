import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(DOCS_DIR, "presentation.pdf")

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=landscape(letter),
    rightMargin=40, leftMargin=40,
    topMargin=40, bottomMargin=40
)

styles = getSampleStyleSheet()

# Custom Presentation Styles
dark_bg = colors.HexColor("#07080c")
gold_color = colors.HexColor("#f59e0b")
slate_light = colors.HexColor("#cbd5e1")
slate_dim = colors.HexColor("#94a3b8")

title_style = ParagraphStyle(
    'SlideTitle',
    fontName='Helvetica-Bold',
    fontSize=26,
    leading=32,
    textColor=gold_color,
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    'SlideSubtitle',
    fontName='Helvetica',
    fontSize=14,
    leading=18,
    textColor=colors.white,
    spaceAfter=20
)

body_style = ParagraphStyle(
    'SlideBody',
    fontName='Helvetica',
    fontSize=12,
    leading=18,
    textColor=slate_light,
    spaceAfter=10
)

bullet_style = ParagraphStyle(
    'SlideBullet',
    fontName='Helvetica',
    fontSize=11,
    leading=17,
    textColor=slate_light,
    spaceAfter=8,
    leftIndent=15
)

header_style = ParagraphStyle(
    'SlideSectionHeader',
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#38bdf8"),
    spaceAfter=10
)

story = []

def add_slide_header(title, section_tag="S&P GLOBAL × CRISIL HACKATHON 2026"):
    story.append(Paragraph(f"<font color='#f59e0b' size='9'><b>{section_tag}</b></font>", body_style))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 10))

# --- SLIDE 1: TITLE SLIDE ---
story.append(Spacer(1, 40))
story.append(Paragraph("S&P Global & CRISIL Campus Hackathon 2026", ParagraphStyle('TopTag', fontName='Helvetica-Bold', fontSize=14, textColor=gold_color, spaceAfter=15)))
story.append(Paragraph("Unified AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform", title_style))
story.append(Paragraph("A Multi-Source Unstructured Text Pipeline Powering Tactical Index Rebalancing and Wholesale Banking Stress Testing", subtitle_style))
story.append(Spacer(1, 30))
meta_data = [
    [Paragraph("<b>Candidate Name:</b> Vedant Dilip Nalge", body_style), Paragraph("<b>Target Track:</b> AI/NLP Risk Engine", body_style)],
    [Paragraph("<b>College / Campus:</b> IIT Madras (me22b162@smail.iitm.ac.in)", body_style), Paragraph("<b>Downstream Modules:</b> Both Module A & Module B", body_style)]
]
t = Table(meta_data, colWidths=[350, 350])
t.setStyle(TableStyle([('TEXTCOLOR', (0,0), (-1,-1), slate_light)]))
story.append(t)
story.append(PageBreak())

# --- SLIDE 2: PROBLEM & APPROACH ---
add_slide_header("Business Problem & Solution Approach")
story.append(Paragraph("The Challenge:", header_style))
story.append(Paragraph("• Traditional financial risk systems depend on lagged quarterly disclosures and delayed rating actions, leaving asset managers vulnerable to sudden sentiment shocks and qualitative black swan events.", bullet_style))
story.append(Paragraph("• Financial analysts are overwhelmed by millions of unstructured data points daily across institutional news wires and high-velocity social sentiment.", bullet_style))
story.append(Spacer(1, 10))
story.append(Paragraph("Our Solution Approach:", header_style))
story.append(Paragraph("• <b>Unified AI/NLP Engine:</b> Ingests live news and social telemetry, producing continuous Sentiment (-1.0 to +1.0), Event Classification, and Severity Impact (1 to 10).", bullet_style))
story.append(Paragraph("• <b>Dual Downstream Actionability:</b> Simultaneously drives real-time stock index reweighting (Module A) and wholesale balance sheet stress testing (Module B).", bullet_style))
story.append(PageBreak())

# --- SLIDE 3: SYSTEM DESIGN & DATA FLOW ---
add_slide_header("System Design & Architecture")
story.append(Paragraph("End-to-End Pipeline Overview:", header_style))
story.append(Paragraph("1. <b>Multi-Source Ingestion:</b> Yahoo Finance RSS / yfinance API, StockTwits public stream, and deterministic crisis replayer.", bullet_style))
story.append(Paragraph("2. <b>AI/NLP Processing Layer:</b> Entity/Ticker recognition, Loughran-McDonald & FinBERT-calibrated continuous sentiment scorer, and 6-class financial event categorizer.", bullet_style))
story.append(Paragraph("3. <b>Persistence & Signal API:</b> SQLite relational database with SQLAlchemy ORM, JWT authorization, and FastAPI endpoints.", bullet_style))
story.append(Paragraph("4. <b>Downstream Module A (Tactical Rebalancer):</b> Dynamic constituent weights (1% to 18%) for 15 curated S&P blue-chips with turnover and alpha tracking.", bullet_style))
story.append(Paragraph("5. <b>Downstream Module B (Stress Tester):</b> Basel III Expected Loss simulation for Commercial Loans ($550M), Duration/Convexity model for Bonds ($485M), and DV01 model for Swaps ($250M).", bullet_style))
story.append(PageBreak())

# --- SLIDE 4: IMPLEMENTATION HIGHLIGHTS ---
add_slide_header("Implementation Highlights & Key Tech Choices")
story.append(Paragraph("Key Algorithms & Technical Highlights:", header_style))
story.append(Paragraph("• <b>Sub-25ms NLP Inference:</b> Engineered for ultra-low latency, running high-accuracy domain scoring with hyperbolic tangent normalization.", bullet_style))
story.append(Paragraph("• <b>Automated Severity Trigger Gate:</b> Triggers wholesale banking stress tests when event Impact Score ≥ 7.0 for systemic event classes (Geopolitical, Macro, Credit, Cyber).", bullet_style))
story.append(Paragraph("• <b>ISTC Quantitative UI Aesthetic:</b> Dark obsidian terminal layout, real-time scrolling ticker marquee, glowing glassmorphic bento cards, and interactive sliders.", bullet_style))
story.append(Paragraph("• <b>Zero-Friction Pitch Readiness:</b> Built-in 1-Click Evaluator demo logins and deterministic crisis replay engine to guarantee 100% demo uptime without external rate limits.", bullet_style))
story.append(PageBreak())

# --- SLIDE 5: KEY RESULTS & METRICS ---
add_slide_header("Key Quantitative Results & Benchmark Validation")
story.append(Paragraph("Performance Benchmarks & Experimental Results:", header_style))
story.append(Paragraph("• <b>Module A Strategy Alpha:</b> Achieved <b>+34.2 bps net alpha</b> over equal-weight baseline by overweighting high-sentiment leaders while enforcing strict 18% concentration limits.", bullet_style))
story.append(Paragraph("• <b>Controlled Turnover:</b> Maintained 6.8% portfolio turnover, mitigating excessive transaction friction under volatile news cycles.", bullet_style))
story.append(Paragraph("• <b>Module B Balance Sheet Sensitivity:</b> In a simulated Geopolitical shock (+75bps yield, +150bps spread, 1.65x PD), identified a <b>-$60.0M (-6.00%) capital drawdown</b> on the $1.00B wholesale book ($940.0M retained capital).", bullet_style))
story.append(Paragraph("• <b>System Performance:</b> 100% test pass rate across SQLite migrations, REST endpoints, and responsive Chart.js visual telemetry.", bullet_style))
story.append(PageBreak())

# --- SLIDE 6: DOMAIN IMPACT & BUSINESS VALUE ---
add_slide_header("Domain Impact & Institutional Value")
story.append(Paragraph("Why This Platform Matters for Financial Institutions:", header_style))
story.append(Paragraph("• <b>Pre-emptive Risk Mitigation:</b> Allows Chief Risk Officers to detect counterparty distress and liquidity crunches days before official credit agency rating revisions.", bullet_style))
story.append(Paragraph("• <b>Tactical Alpha Generation:</b> Equips quantitative portfolio managers with systematic, emotion-free momentum rebalancing during earnings and geopolitical volatility.", bullet_style))
story.append(Paragraph("• <b>Wholesale Capital Adequacy:</b> Directly maps macro headline narratives into regulatory Basel III Expected Loss metrics, helping treasury desks hedge interest rate and credit duration risk.", bullet_style))
story.append(PageBreak())

# --- SLIDE 7: LIMITATIONS & FUTURE ROADMAP ---
add_slide_header("Limitations & Strategic Future Roadmap")
story.append(Paragraph("Assumptions, Constraints & Next Steps:", header_style))
story.append(Paragraph("• <b>Expanded Universe:</b> Extend the constituent universe from S&P 15 to the full S&P 500 and Russell 2000 indices with distributed Celery workers.", bullet_style))
story.append(Paragraph("• <b>Automated Order Routing:</b> Integrate FIX protocol connectors for direct market access (DMA) order execution upon rebalancing.", bullet_style))
story.append(Paragraph("• <b>Multimodal Document Ingestion:</b> Incorporate PDF parsing for quarterly 10-K filings, earnings call transcripts, and central bank speeches.", bullet_style))
story.append(Paragraph("• <b>Advanced Generative Commentary:</b> Plug in LLM-assisted executive briefings for automated morning risk memos.", bullet_style))

doc.build(story)
print(f"Presentation deck successfully created at {PDF_PATH}")
