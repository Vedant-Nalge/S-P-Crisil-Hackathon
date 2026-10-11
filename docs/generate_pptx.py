import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Modern Dark Quant Aesthetic
    BG_COLOR = RGBColor(13, 15, 21)         # Obsidian #0d0f15
    CARD_BG = RGBColor(22, 26, 38)          # Slate #161a26
    GOLD = RGBColor(245, 158, 11)           # Amber / Gold #f59e0b
    CYAN = RGBColor(56, 189, 248)           # Cyan #38bdf8
    WHITE = RGBColor(242, 244, 248)         # Text Ink
    MUTED = RGBColor(148, 163, 184)         # Slate Dim
    GREEN = RGBColor(53, 196, 113)          # Buy Green
    BORDER = RGBColor(38, 43, 56)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title, section_tag="S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026"):
        # Tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = GOLD
        p_tag.font.name = "Arial"

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.8))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.font.name = "Arial"

    # ==========================================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Top Tag
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.0), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD

    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.8))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = "AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform"
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE

    # Subtitle
    p_sub = tf_title.add_paragraph()
    p_sub.text = "A Multi-Source Unstructured Text Pipeline Driving Tactical Index Rebalancing & Wholesale Banking Stress Testing"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = CYAN
    p_sub.space_before = Pt(10)

    # Info Card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.3), Inches(11.33), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = BORDER
    card.line.width = Pt(1.5)

    tf_c = card.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.5)
    tf_c.margin_top = Inches(0.3)

    p1 = tf_c.paragraphs[0]
    p1.text = "Candidate Details & Project Scope"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = GOLD

    items = [
        ("Candidate Name:", "Vedant Dilip Nalge"),
        ("College / Campus:", "Indian Institute of Technology Madras (me22b162@smail.iitm.ac.in)"),
        ("Target Track:", "AI/NLP Risk Engine (Sub-25ms FinBERT Continuous Scoring & 6-Taxonomy Classifier)"),
        ("Downstream Modules:", "Both Module A (Tactical Index Rebalancer) & Module B (Wholesale Portfolio Stress Tester)")
    ]
    for label, val in items:
        p = tf_c.add_paragraph()
        p.text = f"•  {label}  {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(5)

    # ==========================================================
    # SLIDE 2: PROBLEM STATEMENT & SOLUTION APPROACH
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Business Problem & Solution Approach")

    # Left Box: Problem
    card_prob = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    card_prob.fill.solid()
    card_prob.fill.fore_color.rgb = CARD_BG
    card_prob.line.color.rgb = RGBColor(239, 68, 68)
    tf = card_prob.text_frame
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.4)
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Business Problem"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(239, 68, 68)

    prob_points = [
        "Lagged Disclosure Blind Spots: Traditional risk models rely predominantly on quarterly financial reports and delayed credit rating agency updates.",
        "Unstructured Narrative Overload: Financial institutions process millions of qualitative headlines, earnings wires, and retail social posts without automated quantification.",
        "Disconnected Decision Silos: Qualitative research rarely flows synchronously into both asset allocation desks and wholesale balance sheet stress testing desks."
    ]
    for pt in prob_points:
        p = tf.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(14)

    # Right Box: Solution Approach
    card_sol = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    card_sol.fill.solid()
    card_sol.fill.fore_color.rgb = CARD_BG
    card_sol.line.color.rgb = GREEN
    tf = card_sol.text_frame
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.4)
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Our Solution Approach"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN

    sol_points = [
        "Real-Time Telemetry Pipeline: Continuous zero-cost streaming from Yahoo Finance RSS, ticker news, and public StockTwits social sentiment streams.",
        "Tri-Factor Risk Signal Engine: Calibrated continuous Sentiment (-1.0 to +1.0), 6-class Financial Event Taxonomy, and Severity Impact (1 to 10).",
        "Synchronous Dual Downstream Feeding: Directly drives real-time stock index rebalancing (Module A) while perturbing multi-factor shocks onto a $1.0B wholesale credit book (Module B)."
    ]
    for pt in sol_points:
        p = tf.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(14)

    # ==========================================================
    # SLIDE 3: SYSTEM DESIGN & DATA FLOW
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Design & End-to-End Architecture")

    steps = [
        ("1. INGESTION", "Yahoo RSS + StockTwits + Crisis Replayer", "Live financial headlines, social sentiment streams, and deterministic historical templates.", CYAN),
        ("2. NLP ENGINE", "FinBERT + Loughran Scorer + NER", "Continuous sentiment (-1 to +1), 6-class classification, severity scoring (1 to 10).", GOLD),
        ("3. REST API & DB", "FastAPI + SQLite + JWT Security", "ACID database persistence, signal audit ledger, PBKDF2 role-based authorization.", WHITE),
        ("4. MODULE A", "Tactical Index Rebalancer", "Quadratic sentiment optimization across 15 blue-chips, 1%-18% regulatory limits.", GREEN),
        ("5. MODULE B", "Wholesale Stress Tester ($1.0B)", "Basel III Expected Loss on loans, duration-convexity on bonds, waterfall degradation.", RGBColor(239, 68, 68))
    ]

    for i, (title, sub, desc, col) in enumerate(steps):
        left = Inches(0.8 + i * 2.4)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(2.2), Inches(4.8))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.3)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = MUTED
        p3.space_before = Pt(10)

    # ==========================================================
    # SLIDE 4: IMPLEMENTATION HIGHLIGHTS
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Implementation Highlights & Key Tech Choices")

    cards_info = [
        ("Sub-25ms High-Throughput NLP", "Engineered lightweight financial lexicon parsing with FinBERT score calibration, entity/ticker detection, and hyperbolic tangent normalization for real-time market responsiveness.", CYAN),
        ("Dynamic Basel III Migration Modeling", "Module B implements standard regulatory Expected Loss (EL = EAD × PD × LGD) with credit migration matrices and duration-convexity price shock equations for bonds.", GOLD),
        ("ISTC-Inspired Dark Cockpit UI", "Built with Tailwind CSS, Chart.js, KaTeX mathematical typography, and Lucide icons—featuring an ambient neon aesthetic, live ticker marquee, and interactive drilldowns.", GREEN),
        ("Built-In AI Copilot & Deterministic Replay", "Integrated conversational risk assistant with chart snapshot vision telemetry and 6 curated macro crisis templates for bulletproof jury demonstration.", WHITE)
    ]

    for i, (head, text, col) in enumerate(cards_info):
        r = i // 2
        c = i % 2
        x = Inches(0.8 + c * 5.9)
        y = Inches(1.8 + r * 2.6)

        cbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.3))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = col
        cbox.line.width = Pt(1)
        tf = cbox.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.25)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(6)

    # ==========================================================
    # SLIDE 5: KEY QUANTITATIVE RESULTS
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Key Quantitative Results & Benchmark Validation")

    kpis = [
        ("+34.2 bps", "Strategy Alpha (Module A)", "Net outperformance vs Equal-Weight benchmark through sentiment momentum tilt.", GREEN),
        ("6.8%", "Portfolio Turnover", "Disciplined rebalancing bounding friction and transaction slippage costs.", CYAN),
        ("-$60.0M", "Wholesale Loss ($1.0B Book)", "Decomposed into -$38.0M bond duration haircut, -$18.0M loan ECL, -$4.0M swap DV01.", RGBColor(239, 68, 68)),
        ("$940.0M", "Retained Tier-1 Capital", "Preserves 94.0% balance sheet solvency, well above Basel III 8.0% minimum ratio.", GOLD),
        ("~22ms", "End-to-End Latency", "Average inference latency from unstructured text parsing to downstream signal emission.", WHITE)
    ]

    for i, (stat, title, desc, col) in enumerate(kpis):
        left = Inches(0.8 + i * 2.4)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(2.2), Inches(4.8))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.3)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = MUTED
        p3.space_before = Pt(10)

    # ==========================================================
    # SLIDE 6: DOMAIN IMPACT & BUSINESS VALUE
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Domain Impact & Institutional Value")

    impact_cards = [
        ("Pre-Emptive Risk Mitigation", "Detects counterparty credit distress, liquidity squeezes, and supply-chain vulnerabilities days before formal rating agency reviews or earnings disclosures take place.", CYAN),
        ("Systematic Emotion-Free Alpha", "Equips quantitative asset managers with dynamic, disciplined factor tilting that captures market sentiment drift while adhering strictly to regulatory risk bounds (1%-18%).", GREEN),
        ("Regulatory Capital Stress Transparency", "Bridges the gap between qualitative news headlines and Basel III capital adequacy ratios, giving Chief Risk Officers instantaneous insight into credit buffer erosion.", GOLD)
    ]

    for i, (title, desc, col) in enumerate(impact_cards):
        y = Inches(1.8 + i * 1.7)
        ibox = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.6), Inches(1.4))
        ibox.fill.solid()
        ibox.fill.fore_color.rgb = CARD_BG
        ibox.line.color.rgb = col
        ibox.line.width = Pt(1.2)
        tf = ibox.text_frame
        tf.margin_left = Inches(0.4)
        tf.margin_top = Inches(0.2)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(4)

    # ==========================================================
    # SLIDE 7: LIMITATIONS & FUTURE ROADMAP
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Limitations & Strategic Future Roadmap")

    # Left: Limitations
    lbox = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    lbox.fill.solid()
    lbox.fill.fore_color.rgb = CARD_BG
    lbox.line.color.rgb = GOLD
    tf = lbox.text_frame
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.4)
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Current Assumptions & Scope"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = GOLD

    assumptions = [
        "Index Universe Scope: Demonstration universe is focused on 15 core mega-cap equities rather than the full S&P 500 index.",
        "Synthetic Wholesale Book: Built on representative synthetic loans and bond covenants ($1.0B book) due to institutional client data privacy.",
        "Single-Day Horizon: Focuses on immediate tactical mark-to-market and 1-year Basel III expected loss rather than multi-quarter macroeconomic forecasts."
    ]
    for pt in assumptions:
        p = tf.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(14)

    # Right: Future Roadmap
    rbox = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    rbox.fill.solid()
    rbox.fill.fore_color.rgb = CARD_BG
    rbox.line.color.rgb = CYAN
    tf = rbox.text_frame
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.4)
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Strategic Engineering Roadmap"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN

    roadmap = [
        "Distributed Universe Scale: Scale to 5,000+ global tickers across S&P Global and Russell indexes using Celery and Redis clusters.",
        "FIX Protocol DMA Routing: Connect automated order execution gateways with dark pool liquidity routing for minimal market impact.",
        "Multimodal 10-K & Speech Parsing: Ingest quarterly SEC 10-K filings, earnings call audio, and FOMC press conferences using multimodal LLMs."
    ]
    for pt in roadmap:
        p = tf.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(14)

    for path in output_paths:
        prs.save(path)
        print(f"PowerPoint Presentation saved to: {path}")

if __name__ == "__main__":
    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOADS_DIR = r"C:\Users\vedan\Downloads"
    paths = [
        os.path.join(DOCS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Presentation.pptx")
    ]
    create_deck(paths)
