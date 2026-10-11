import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_zelenskyy_presentation(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Dark Obsidian Palette
    BG_COLOR = RGBColor(13, 15, 21)         # #0d0f15
    CARD_BG = RGBColor(22, 26, 38)          # #161a26
    CARD_BG_ALT = RGBColor(28, 33, 48)
    GOLD = RGBColor(245, 158, 11)           # #f59e0b
    CYAN = RGBColor(56, 189, 248)           # #38bdf8
    WHITE = RGBColor(242, 244, 248)         # #f2f4f8
    MUTED = RGBColor(148, 163, 184)         # #94a3b8
    GREEN = RGBColor(53, 196, 113)          # #35c471
    RED = RGBColor(239, 68, 68)             # #ef4444

    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title, section_tag="S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026"):
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(10); p_tag.font.bold = True; p_tag.font.color.rgb = GOLD; p_tag.font.name = "Arial"

        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22); p_title.font.bold = True; p_title.font.color.rgb = WHITE; p_title.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: TITLE & CANDIDATE METADATA (WITH HERO SCREENSHOT)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Header Tag & Title
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = "S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026 // CASE STUDY SUBMISSION"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = GOLD

    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(1.2))
    tf = tb_title.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform"
    p1.font.size = Pt(26); p1.font.bold = True; p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "A Multi-Source Unstructured Text Pipeline Driving Tactical Index Rebalancing & Wholesale Banking Stress Testing"
    p2.font.size = Pt(12.5); p2.font.color.rgb = CYAN; p2.space_before = Pt(4)

    # Candidate Info Table
    rows, cols = 4, 2
    table_shape = s1.shapes.add_table(rows, cols, Inches(0.8), Inches(2.2), Inches(11.7), Inches(1.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(8.9)

    meta = [
        ("Candidate Name", "Vedant Dilip Nalge"),
        ("College / Campus", "Indian Institute of Technology Madras (IIT Madras) • me22b162@smail.iitm.ac.in"),
        ("Target Track", "AI/NLP Financial Risk Engine (FinBERT Continuous Sentiment & 6-Taxonomy Classifier)"),
        ("Downstream Implementations", "Dual Delivery: Module A (Tactical Index Rebalancer) & Module B (Wholesale Portfolio Stress Tester)")
    ]
    for i, (k, v) in enumerate(meta):
        cell_k = table.cell(i, 0); cell_v = table.cell(i, 1)
        cell_k.fill.solid(); cell_k.fill.fore_color.rgb = CARD_BG
        cell_v.fill.solid(); cell_v.fill.fore_color.rgb = CARD_BG_ALT
        pk = cell_k.text_frame.paragraphs[0]; pk.text = k; pk.font.bold = True; pk.font.size = Pt(10); pk.font.color.rgb = GOLD
        pv = cell_v.text_frame.paragraphs[0]; pv.text = v; pv.font.size = Pt(10); pv.font.color.rgb = WHITE

    # Embed Actual Website Hero Cockpit Screenshot
    hero_img = os.path.join(DOCS_DIR, "user_shot_hero.png")
    if os.path.exists(hero_img):
        s1.shapes.add_picture(hero_img, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.9))

    # =========================================================================
    # SLIDE 2: BUSINESS PROBLEM & SOLUTION APPROACH
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Business Problem & Solution Approach")

    # Left: Problem
    cp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    cp.fill.solid(); cp.fill.fore_color.rgb = CARD_BG
    cp.line.color.rgb = RED; cp.line.width = Pt(1.5)
    tf = cp.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.35); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "The Financial Industry Problem"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = RED

    probs = [
        ("Lagged Quantitative Disclosures", "Traditional institutional risk engines rely on quarterly 10-K filings and delayed rating agency revisions, leaving portfolios vulnerable to fast-moving narrative shocks."),
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

    p = tf.paragraphs[0]; p.text = "Our AI/NLP Solution Approach"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = GREEN

    sols = [
        ("Continuous Multi-Source Ingestion", "Streams live financial news (Yahoo Finance RSS) and high-velocity retail sentiment (StockTwits API) with sub-25ms end-to-end processing."),
        ("Tri-Factor Risk Telemetry", "Converts unstructured text into 3 calibrated signals: continuous Sentiment (-1.0 to +1.0), 6-class Financial Taxonomy, and Impact Severity (1 to 10)."),
        ("Synchronous Dual Downstream Cascade", "Directly drives Module A (Tactical Index Rebalancer with 1%-18% bounds) and Module B (Wholesale Banking Stress Tester across $1.0B book) simultaneously.")
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
        pk = cell_k.text_frame.paragraphs[0]; pk.text = layer_name; pk.font.bold = True; pk.font.size = Pt(10.5); pk.font.color.rgb = GOLD
        pv = cell_v.text_frame.paragraphs[0]; pv.text = desc; pv.font.size = Pt(9.5); pv.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 4: LIVE SIMULATION INGESTION (THE ZELENSKYY SCENARIO)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Live Simulation Case Study: Ingesting Real-World Geopolitical News")

    # Embed Actual User Screenshot of Ingestion & News Wire with Zelenskyy headline
    zelenskyy_news_img = os.path.join(DOCS_DIR, "user_shot_news_zelenskyy.png")
    if os.path.exists(zelenskyy_news_img):
        s4.shapes.add_picture(zelenskyy_news_img, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Card: Zelenskyy Scenario Ingestion Telemetry
    rc = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = GOLD; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Live Ingestion Telemetry: Zelenskyy Headline"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = GOLD

    steps_text = [
        ("1. Ingested News Wire Headline", "Seeking Alpha (14m ago): 'Zelenskyy says Trump\'s Russia-Ukraine energy ceasefire deal was a surprise: Axios'\nParsed directly from multi-source institutional financial wire."),
        ("2. Automated Entity & Ticker Detection", "• Entity Identified: ExxonMobil (XOM), Energy Sector, Sovereign Macro\n• Ingestion-to-Inference Latency: ~22ms\n• Zero manual tag input required from user."),
        ("3. AI/NLP Inference Engine", "• Classification: Geopolitical / Energy Transition Event\n• Directional Sentiment: Evaluates ceasefire narrative impact on crude benchmarks & defensive energy stocks.\n• Severity Trigger: Cascades immediately into downstream rebalancing & wholesale capital stress.")
    ]
    for head, body in steps_text:
        p = tf.add_paragraph()
        p.text = head
        p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = CYAN; p.space_before = Pt(10)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5); p2.font.color.rgb = WHITE; p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: LIVE SIMULATION OUTPUT — MODULE A: TACTICAL REBALANCER
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Downstream Module A: Dynamic Tactical Index Rebalancing")

    # Embed Actual User Screenshot of Module A Rebalance Output
    mod_a_img = os.path.join(DOCS_DIR, "user_shot_module_a_zelenskyy.png")
    if os.path.exists(mod_a_img):
        s5.shapes.add_picture(mod_a_img, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Card: Module A Execution Metrics
    rc = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = GREEN; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Module A Live Simulation Results"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = GREEN

    mod_a_metrics = [
        ("Live Rebalance Confirmation", "Banner: 'Live Rebalance Applied: Constituent weights rebalanced after Zelenskyy says Trump\'s Russia-Ukraine energy cea...' (Normalized to 100%)."),
        ("Strategy Alpha & Turnover", "• Strategy Alpha: +5.0 bps generated.\n• Portfolio Turnover: 0.25% (disciplined institutional friction control)."),
        ("Tactical Weight Tilts (Core 15)", "• AAPL: 17.85% (upper regulatory bound)\n• JPM: 17.85% | MSFT: 16.48% | NVDA: 13.04%\n• XOM: 4.80% | TSLA: 1.60% | AMZN: 1.04%"),
        ("Regulatory Bounding Enforced", "All 15 constituent weights strictly clamped inside regulatory risk bounds [1.0%, 18.0%]."),
        ("Real-Time Visual Synchronization", "Sector Donut and Cumulative Alpha Line (+5.0 bps) instantly updated upon news ingestion.")
    ]
    for head, body in mod_a_metrics:
        p = tf.add_paragraph()
        p.text = f"•  {head}:"
        p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = GOLD; p.space_before = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9); p2.font.color.rgb = WHITE; p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: LIVE SIMULATION OUTPUT — MODULE B: WHOLESALE STRESS TESTER
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Downstream Module B: Wholesale Portfolio Stress Testing ($1.0B Book)")

    # Embed Actual User Screenshot of Module B Stress Output
    mod_b_img = os.path.join(DOCS_DIR, "user_shot_module_b_zelenskyy.png")
    if os.path.exists(mod_b_img):
        s6.shapes.add_picture(mod_b_img, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Card: Module B Stress Metrics
    rc = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = RED; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Module B Live Stress Results"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = RED

    mod_b_metrics = [
        ("Wholesale Credit Book Baseline", "Synthetic $1,000.0M ($1.0B) book across 15 wholesale facilities: $550M Commercial Loans, $450M Corporate Bonds, $250M Derivatives."),
        ("Multi-Factor Shocks Calibrated", "• Yield Shift (Δy): -4 bps\n• Credit Spread Widening (Δs): +10 bps\n• Basel PD Multiplier: 1.02x"),
        ("Valuation Shock & Degradation Waterfall", "• Pre-Stress Book Valuation: $1000.0M\n• Stressed Capital Loss: -$1.7M (-0.17% Drawdown)\n• Post-Stress Capital: $998.3M (99.83% Retained)"),
        ("Basel III Capital Adequacy Preserved", "Capital buffer remains safely above 8.0% Basel III floor. Retains $998.3M of regulatory Tier-1 capital."),
        ("CRO 'What-If' Sandbox Overrides", "Sliders dynamically synced to event parameters, allowing risk committees to run custom sensitivity checks.")
    ]
    for head, body in mod_b_metrics:
        p = tf.add_paragraph()
        p.text = f"•  {head}:"
        p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = GOLD; p.space_before = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9); p2.font.color.rgb = WHITE; p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 7: AI COPILOT, DOMAIN IMPACT & FUTURE ROADMAP
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "AI Copilot Intelligence, Domain Impact & Roadmap")

    # Embed Actual User Screenshot of AI Copilot Drawer
    copilot_img = os.path.join(DOCS_DIR, "user_shot_copilot.png")
    if os.path.exists(copilot_img):
        s7.shapes.add_picture(copilot_img, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))

    # Right Top Card: Domain Value & Institutional Impact
    rc_top = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.5), Inches(1.6), Inches(7.0), Inches(2.5))
    rc_top.fill.solid(); rc_top.fill.fore_color.rgb = CARD_BG
    rc_top.line.color.rgb = GOLD; rc_top.line.width = Pt(1.5)
    tf = rc_top.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.25); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "Institutional Value & Domain Impact"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GOLD
    p1 = tf.add_paragraph()
    p1.text = "• Early Contagion Warning: Detects credit distress 3 to 14 days before rating agency downgrades."
    p1.font.size = Pt(10); p1.font.color.rgb = WHITE; p1.space_before = Pt(6)
    p2 = tf.add_paragraph()
    p2.text = "• Cross-Asset Silo Breakdown: Provides a unified qualitative truth connecting equity PMs and credit CROs."
    p2.font.size = Pt(10); p2.font.color.rgb = WHITE; p2.space_before = Pt(4)
    p3 = tf.add_paragraph()
    p3.text = "• AI Copilot Vision: Features real-time chart snapshot reasoning and mathematical formula verification."
    p3.font.size = Pt(10); p3.font.color.rgb = WHITE; p3.space_before = Pt(4)

    # Right Bottom: 4-Phase Roadmap Timeline Table
    r, c = 2, 4
    t_shape = s7.shapes.add_table(r, c, Inches(5.5), Inches(4.3), Inches(7.0), Inches(2.5))
    t = t_shape.table
    for ci in range(4): t.columns[ci].width = Inches(1.75)

    timeline_data = [
        ("Phase 1: MVP (Done)", "Phase 2: Scale (Q2 2026)", "Phase 3: DMA (Q3 2026)", "Phase 4: Multimodal (Q4)"),
        ("Dual downstream + sub-25ms NLP + ISTC cockpit UI.", "Scale to 5,000+ global tickers with Celery / Redis.", "FIX protocol order routing to dark pools.", "SEC 10-K parser + FOMC speech transcription.")
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
        try:
            prs.save(path)
            print(f"Zelenskyy simulation presentation saved to: {path}")
        except Exception as e:
            print(f"Notice: Could not write to {path} (file is likely currently open in PowerPoint): {e}")

if __name__ == '__main__':
    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOADS_DIR = r"C:\Users\vedan\Downloads"
    paths = [
        os.path.join(DOCS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Zelenskyy_Simulation.pptx"),
        os.path.join(DOWNLOADS_DIR, "Vedant_Nalge_Final_Submission.pptx")
    ]
    build_zelenskyy_presentation(paths)
