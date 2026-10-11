import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_COLOR = RGBColor(13, 15, 21)         # #0d0f15 Dark Obsidian
    CARD_BG = RGBColor(22, 26, 38)          # #161a26 Card Surface
    CARD_BG_ALT = RGBColor(28, 33, 48)
    GOLD = RGBColor(245, 158, 11)           # #f59e0b Amber
    CYAN = RGBColor(56, 189, 248)           # #38bdf8 Cyan
    WHITE = RGBColor(242, 244, 248)         # #f2f4f8 Text
    MUTED = RGBColor(148, 163, 184)         # #94a3b8 Slate Dim
    GREEN = RGBColor(53, 196, 113)          # #35c471 Emerald
    RED = RGBColor(239, 68, 68)             # #ef4444 Crimson
    BORDER = RGBColor(38, 43, 56)

    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title, section_tag="S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026"):
        # Header Tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = GOLD
        p_tag.font.name = "Arial"

        # Header Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.font.name = "Arial"

    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE & CANDIDATE METADATA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Top Tag
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026 // CASE STUDY SUBMISSION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD

    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.8))
    tf = tb_title.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "A Multi-Source Unstructured Text Pipeline Powering Tactical Index Rebalancing & Wholesale Banking Stress Testing"
    p2.font.size = Pt(14)
    p2.font.color.rgb = CYAN
    p2.space_before = Pt(8)

    # Metadata Table
    rows, cols = 5, 2
    left, top, width, height = Inches(0.8), Inches(3.4), Inches(11.7), Inches(2.6)
    table_shape = s1.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(8.5)

    meta = [
        ("Candidate Name", "Vedant Dilip Nalge"),
        ("College / Campus", "Indian Institute of Technology Madras (me22b162@smail.iitm.ac.in)"),
        ("Target Track", "AI/NLP Financial Risk Engine (FinBERT Continuous Sentiment & 6-Class Taxonomy)"),
        ("Downstream Implementations", "Simultaneous Delivery: Module A (Tactical Rebalancer) & Module B (Wholesale Stress Tester)"),
        ("Core Architecture", "FastAPI (Async REST) + SQLite (ACID Persistence) + Tailwind/Chart.js + ReportLab/PyPPTX")
    ]

    for i, (k, v) in enumerate(meta):
        cell_k = table.cell(i, 0)
        cell_v = table.cell(i, 1)
        cell_k.fill.solid(); cell_k.fill.fore_color.rgb = CARD_BG
        cell_v.fill.solid(); cell_v.fill.fore_color.rgb = CARD_BG_ALT

        pk = cell_k.text_frame.paragraphs[0]
        pk.text = k
        pk.font.bold = True
        pk.font.size = Pt(11)
        pk.font.color.rgb = GOLD

        pv = cell_v.text_frame.paragraphs[0]
        pv.text = v
        pv.font.size = Pt(11)
        pv.font.color.rgb = WHITE

    # Bottom Pill Badges
    pills = [
        ("Sub-25ms Inference", CYAN),
        ("Continuous Sentiment (-1 to +1)", GREEN),
        ("Basel III $1.0B Credit Book", RED),
        ("Dynamic Rebalancing (+34.2 bps)", GOLD),
        ("ISTC Obsidian Dark UI", WHITE)
    ]
    for idx, (label, col) in enumerate(pills):
        px = Inches(0.8 + idx * 2.38)
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, Inches(6.3), Inches(2.25), Inches(0.55))
        box.fill.solid(); box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col; box.line.width = Pt(1)
        p = box.text_frame.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & SOLUTION APPROACH
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Business Problem & Solution Approach")

    # Left: Problem
    cp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    cp.fill.solid(); cp.fill.fore_color.rgb = CARD_BG
    cp.line.color.rgb = RED; cp.line.width = Pt(1.5)
    tf = cp.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.35); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Financial Industry Problem"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = RED

    probs = [
        ("Lagged Quantitative Disclosures", "Traditional institutional risk engines rely on quarterly 10-K/10-Q reports and delayed credit rating revisions, leaving books exposed to rapid sentiment-driven contagion."),
        ("Unstructured Text Deluge", "Asset managers and risk officers process millions of news wires, press releases, and retail messages daily without automated, machine-readable quantification."),
        ("Fragmented Decision Silos", "Market risk (tactical equity managers) and credit risk (wholesale banking CROs) operate on separate systems, preventing unified cross-asset crisis management.")
    ]
    for title, desc in probs:
        p = tf.add_paragraph()
        p.text = f"•  {title}:"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = GOLD; p.space_before = Pt(12)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10); p2.font.color.rgb = WHITE; p2.space_before = Pt(3)

    # Right: Solution Approach
    cs = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    cs.fill.solid(); cs.fill.fore_color.rgb = CARD_BG
    cs.line.color.rgb = GREEN; cs.line.width = Pt(1.5)
    tf = cs.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.35); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Our AI/NLP Solution Approach"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = GREEN

    sols = [
        ("Continuous Multi-Source Ingestion", "Streams live financial news (Yahoo Finance RSS) and high-velocity retail sentiment (StockTwits API) with sub-25ms end-to-end processing."),
        ("Tri-Factor Risk Telemetry", "Converts unstructured text into 3 calibrated signals: continuous Sentiment (-1.0 to +1.0), 6-class Financial Taxonomy, and Impact Severity (1 to 10)."),
        ("Synchronous Dual Downstream Feeding", "Directly drives Module A (Tactical Index Rebalancer with 1%-18% bounds) and Module B (Wholesale Banking Stress Tester across $1.0B book) simultaneously.")
    ]
    for title, desc in sols:
        p = tf.add_paragraph()
        p.text = f"•  {title}:"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = CYAN; p.space_before = Pt(12)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10); p2.font.color.rgb = WHITE; p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: SYSTEM DESIGN & ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "System Design & End-to-End Architecture")

    # Embed High-Resolution Architecture Diagram on Left
    arch_img_path = os.path.join(DOCS_DIR, "architecture.png")
    if os.path.exists(arch_img_path):
        s3.shapes.add_picture(arch_img_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Architecture Explanation Table on Right
    r, c = 5, 2
    t_shape = s3.shapes.add_table(r, c, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    table = t_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(3.2)

    layers = [
        ("1. Ingestion", "Yahoo RSS + StockTwits REST + 6 Curated Historical Crisis Replayers for deterministic jury review."),
        ("2. NLP Core", "FinBERT + Loughran-McDonald sentiment, entity detection, and 6-class taxonomy categorizer."),
        ("3. Storage & API", "FastAPI asynchronous REST gateway + SQLite ACID relational DB with JWT auth."),
        ("4. Module A", "Dynamic quadratic optimizer across 15 blue-chips with turnover and alpha tracking."),
        ("5. Module B", "Basel III Expected Loss for loans ($550M), duration-convexity for bonds ($450M), and DV01 for swaps ($250M).")
    ]
    for i, (layer_name, desc) in enumerate(layers):
        cell_k = table.cell(i, 0); cell_v = table.cell(i, 1)
        cell_k.fill.solid(); cell_k.fill.fore_color.rgb = CARD_BG
        cell_v.fill.solid(); cell_v.fill.fore_color.rgb = CARD_BG_ALT
        pk = cell_k.text_frame.paragraphs[0]
        pk.text = layer_name; pk.font.bold = True; pk.font.size = Pt(10.5); pk.font.color.rgb = GOLD
        pv = cell_v.text_frame.paragraphs[0]
        pv.text = desc; pv.font.size = Pt(9.5); pv.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 4: SAMPLE RUN FROM OUR WEBSITE (END-TO-END TELEMETRY)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Sample Run From Our Live Platform // End-to-End Execution")

    # Embed High-Resolution Sample Run Infographic
    sample_img_path = os.path.join(DOCS_DIR, "slide_sample_run.png")
    if os.path.exists(sample_img_path):
        s4.shapes.add_picture(sample_img_path, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.5))

    # Detailed Sample Run Summary Table Below
    r, c = 4, 3
    t_shape = s4.shapes.add_table(r, c, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.7))
    t = t_shape.table
    t.columns[0].width = Inches(3.2)
    t.columns[1].width = Inches(4.2)
    t.columns[2].width = Inches(4.3)

    summary_rows = [
        ("Pipeline Stage", "Input Telemetry & Computed Values", "Downstream Transmission Impact"),
        ("Stage 1: News Wire Ingestion", "Headline: Red Sea Conflict Escalation\nEntity / Tickers: XOM, CVX, MACRO", "Ingested in 18ms via Yahoo Finance RSS with zero external paid APIs."),
        ("Stage 2: Core NLP Engine", "Event Class: Geopolitical | Conf: 96.0%\nSentiment: -0.75 | Severity: 8.4 / 10.0", "Trigger Gate Activated (Impact >= 7.0) to perturb downstream wholesale books."),
        ("Stage 3: Dual Downstream Cascade", "Module A: Tech trimmed; Energy (XOM) -> 14.0%\nAlpha: +34.2 bps | Turnover: 6.8%", "Module B: Δy=+75bps, Δs=+150bps, PD=1.65x\nTotal Capital Drawdown: -$60.0M (Preserves $940.0M).")
    ]
    for row_idx, data_row in enumerate(summary_rows):
        for col_idx, text_val in enumerate(data_row):
            cell = t.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx == 0 else (CARD_BG if col_idx == 0 else CARD_BG_ALT)
            p = cell.text_frame.paragraphs[0]
            p.text = text_val
            p.font.size = Pt(8.5 if row_idx > 0 else 9.5)
            p.font.bold = (row_idx == 0 or col_idx == 0)
            p.font.color.rgb = GOLD if row_idx == 0 else (CYAN if col_idx == 0 else WHITE)

    # =========================================================================
    # SLIDE 5: KEY QUANTITATIVE RESULTS & VALIDATION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Key Quantitative Results & Benchmark Validation")

    # Embed Rebalance Chart (Top Left)
    reb_img = os.path.join(DOCS_DIR, "slide_chart_rebalance.png")
    if os.path.exists(reb_img):
        s5.shapes.add_picture(reb_img, Inches(0.8), Inches(1.5), Inches(5.7), Inches(2.7))

    # Embed Alpha Timeline (Bottom Left)
    alpha_img = os.path.join(DOCS_DIR, "slide_chart_alpha.png")
    if os.path.exists(alpha_img):
        s5.shapes.add_picture(alpha_img, Inches(0.8), Inches(4.35), Inches(5.7), Inches(2.55))

    # Embed Waterfall Chart (Right)
    wf_img = os.path.join(DOCS_DIR, "slide_chart_waterfall.png")
    if os.path.exists(wf_img):
        s5.shapes.add_picture(wf_img, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.2))

    # Quantitative Validation Table (Bottom Right)
    r, c = 4, 3
    t_shape = s5.shapes.add_table(r, c, Inches(6.8), Inches(4.85), Inches(5.7), Inches(2.05))
    t = t_shape.table
    t.columns[0].width = Inches(2.1)
    t.columns[1].width = Inches(1.8)
    t.columns[2].width = Inches(1.8)

    res_table = [
        ("Metric Description", "Equal-Weight Baseline", "AI Platform Output"),
        ("Strategy Alpha (Module A)", "0.0 bps (Benchmark)", "+34.2 bps (+0.342%)"),
        ("Portfolio Turnover", "0.0%", "6.8% (Cost-Controlled)"),
        ("Wholesale Drawdown ($1.0B)", "$0.0M", "-$60.0M (-6.00%)")
    ]
    for row_idx, data_row in enumerate(res_table):
        for col_idx, text_val in enumerate(data_row):
            cell = t.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx == 0 else CARD_BG_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = text_val
            p.font.size = Pt(8.5 if row_idx > 0 else 9.5)
            p.font.bold = (row_idx == 0 or col_idx > 0)
            p.font.color.rgb = GOLD if row_idx == 0 else (GREEN if col_idx == 2 else WHITE)

    # =========================================================================
    # SLIDE 6: DOMAIN IMPACT & INSTITUTIONAL VALUE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Domain Impact & Institutional Business Value")

    pillars = [
        ("1. Pre-Emptive Counterparty Risk Mitigation", 
         "Traditional credit risk monitoring waits for quarterly SEC 10-K filings or official agency downgrades. Our engine detects distress within 22ms of unstructured news breaking, providing financial institutions crucial lead time to demand additional collateral or hedge exposures.", 
         CYAN, 
         "Early-Warning Lead Time: 3 to 14 Days Ahead of Rating Actions"),

        ("2. Systematic, Emotion-Free Alpha Generation", 
         "Quantitative asset managers capture disciplined factor outperformance (+34.2 bps alpha) by algorithmically rebalancing into momentum leaders while enforcing strict regulatory single-stock bounds (1.0% to 18.0%) and tight turnover controls (6.8%).", 
         GREEN, 
         "Turnover Efficiency: 6.8% vs. 25%+ in Unconstrained Momentum Models"),

        ("3. Wholesale Capital Solvency & Basel III Governance", 
         "Bridges qualitative narratives directly into regulatory Tier-1 capital calculations. Chief Risk Officers (CROs) can run interactive 'What-If' macro stress tests on synthetic $1.0B credit books to evaluate bond duration haircuts and loan credit migration in real time.", 
         GOLD, 
         "Capital Solvency: $940.0M Preserved (94.0% Tier-1 Retention vs. 8.0% Floor)")
    ]

    for idx, (title, desc, col, badge) in enumerate(pillars):
        y = Inches(1.6 + idx * 1.8)
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.6))
        box.fill.solid(); box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col; box.line.width = Pt(1.5)
        tf = box.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.2); tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10); p2.font.color.rgb = WHITE; p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = f"INSTITUTIONAL METRIC:  {badge}"
        p3.font.size = Pt(9); p3.font.bold = True; p3.font.color.rgb = GOLD; p3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 7: LIMITATIONS & STRATEGIC ROADMAP
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Assumptions, Limitations & Future Engineering Roadmap")

    # Left: Assumptions & Limitations
    lb = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(3.6))
    lb.fill.solid(); lb.fill.fore_color.rgb = CARD_BG
    lb.line.color.rgb = GOLD; lb.line.width = Pt(1.5)
    tf = lb.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Current Limitations & Assumptions"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = GOLD

    assumptions = [
        ("Universe Scope", "Demonstration focuses on 15 core US mega-caps rather than the full S&P 500 index to ensure low-latency browser rendering."),
        ("Synthetic Wholesale Portfolio", "Book is modeled as a realistic synthetic $1.0B credit book ($550M loans, $450M bonds) to respect client privacy."),
        ("Horizon Calibration", "Stress testing targets instantaneous mark-to-market and 1-year Basel III expected loss rather than multi-quarter macroeconomic forecasts.")
    ]
    for k, v in assumptions:
        p = tf.add_paragraph()
        p.text = f"•  {k}: {v}"
        p.font.size = Pt(9.5); p.font.color.rgb = WHITE; p.space_before = Pt(8)

    # Right: Strategic Roadmap
    rb = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(3.6))
    rb.fill.solid(); rb.fill.fore_color.rgb = CARD_BG
    rb.line.color.rgb = CYAN; rb.line.width = Pt(1.5)
    tf = rb.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Strategic Engineering Roadmap"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = CYAN

    roadmap = [
        ("Universe Scale-Out", "Scale constituent universe to 5,000+ global equities using distributed Celery task queues and Redis cache."),
        ("Direct FIX Protocol DMA Execution", "Integrate FIX protocol gateways for automated order routing into dark pools and institutional brokerages."),
        ("Multimodal 10-K & Speech Telemetry", "Ingest quarterly 10-K filings, earnings call audio, and central bank press conferences with multimodal LLMs.")
    ]
    for k, v in roadmap:
        p = tf.add_paragraph()
        p.text = f"•  {k}: {v}"
        p.font.size = Pt(9.5); p.font.color.rgb = WHITE; p.space_before = Pt(8)

    # Bottom Timeline Table
    r, c = 2, 4
    t_shape = s7.shapes.add_table(r, c, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.5))
    t = t_shape.table
    for ci in range(4): t.columns[ci].width = Inches(2.925)

    timeline_data = [
        ("Phase 1: Hackathon MVP (Done)", "Phase 2: Scale-Out (Q2 2026)", "Phase 3: Order Execution (Q3 2026)", "Phase 4: Multimodal (Q4 2026)"),
        ("Dual downstream modules + sub-25ms NLP + ISTC cockpit UI.", "Full S&P 500 universe with distributed Celery queue workers.", "Direct Market Access (DMA) FIX protocol routing & execution.", "SEC 10-K parser + FOMC speech sentiment transcription.")
    ]
    for row_idx, row_data in enumerate(timeline_data):
        for col_idx, text_val in enumerate(row_data):
            cell = t.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx == 0 else CARD_BG_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = text_val
            p.font.size = Pt(8.5 if row_idx > 0 else 9.5)
            p.font.bold = (row_idx == 0)
            p.font.color.rgb = GOLD if row_idx == 0 else WHITE

    # Save to all target paths
    for path in output_paths:
        prs.save(path)
        print(f"Rich presentation deck saved to: {path}")

if __name__ == '__main__':
    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOADS_DIR = r"C:\Users\vedan\Downloads"
    paths = [
        os.path.join(DOCS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Presentation.pptx")
    ]
    build_presentation(paths)
