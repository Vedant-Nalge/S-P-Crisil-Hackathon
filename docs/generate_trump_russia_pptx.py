import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_trump_russia_deck(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Dark Obsidian Quant Palette
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
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title, section_tag="S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026 // LIVE CASE STUDY"):
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = GOLD
        p_tag.font.name = "Arial"

        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: TITLE & CANDIDATE METADATA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026 // CASE STUDY SUBMISSION"
    p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = GOLD

    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.7), Inches(1.9))
    tf = tb_title.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform"
    p1.font.size = Pt(29); p1.font.bold = True; p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Live Simulation Case Study: Transmitting the 'Trump-Russia Diesel Deal' Geopolitical Shock onto Index Weights & Wholesale Capital"
    p2.font.size = Pt(13.5); p2.font.color.rgb = CYAN; p2.space_before = Pt(8)

    # Metadata Table
    rows, cols = 5, 2
    table_shape = s1.shapes.add_table(rows, cols, Inches(0.8), Inches(3.35), Inches(11.7), Inches(2.6))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(8.5)

    meta = [
        ("Candidate Name", "Vedant Dilip Nalge"),
        ("College / Campus", "Indian Institute of Technology Madras (me22b162@smail.iitm.ac.in)"),
        ("Target Track", "AI/NLP Financial Risk Engine (FinBERT Continuous Sentiment & 6-Class Taxonomy)"),
        ("Downstream Implementations", "Simultaneous Delivery: Module A (Tactical Rebalancer) & Module B (Wholesale Stress Tester)"),
        ("Live Simulation Scenario", "Trump-Russia Diesel Deal Geopolitical Event (Sentiment: -0.95 | Impact: 9.6/10 | Loss: -$206.4M)")
    ]
    for i, (k, v) in enumerate(meta):
        cell_k = table.cell(i, 0); cell_v = table.cell(i, 1)
        cell_k.fill.solid(); cell_k.fill.fore_color.rgb = CARD_BG
        cell_v.fill.solid(); cell_v.fill.fore_color.rgb = CARD_BG_ALT
        pk = cell_k.text_frame.paragraphs[0]; pk.text = k; pk.font.bold = True; pk.font.size = Pt(11); pk.font.color.rgb = GOLD
        pv = cell_v.text_frame.paragraphs[0]; pv.text = v; pv.font.size = Pt(11); pv.font.color.rgb = WHITE

    # Bottom Pill Badges
    pills = [
        ("Sub-25ms FinBERT NLP", CYAN),
        ("Sentiment: -0.95 Bearish", RED),
        ("Severity Impact: 9.6/10", GOLD),
        ("Wholesale Drawdown: -$206.4M", RED),
        ("Tier-1 Retained: $793.6M", GREEN)
    ]
    for idx, (label, col) in enumerate(pills):
        px = Inches(0.8 + idx * 2.38)
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, Inches(6.25), Inches(2.25), Inches(0.55))
        box.fill.solid(); box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col; box.line.width = Pt(1)
        p = box.text_frame.paragraphs[0]
        p.text = label; p.alignment = PP_ALIGN.CENTER; p.font.size = Pt(9); p.font.bold = True; p.font.color.rgb = col

    # =========================================================================
    # SLIDE 2: BUSINESS PROBLEM & SOLUTION APPROACH (WITH NEWS FEED SCREENSHOT)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Business Problem & Solution Approach // Multi-Source Ingestion")

    # Left Top: Problem Card
    cp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(5.7), Inches(2.7))
    cp.fill.solid(); cp.fill.fore_color.rgb = CARD_BG
    cp.line.color.rgb = RED; cp.line.width = Pt(1.5)
    tf = cp.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.25); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "The Financial Problem: Qualitative Blind Spots"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = RED
    p_sub = tf.add_paragraph()
    p_sub.text = "• Lagged Disclosures: Traditional models wait for quarterly reports or delayed rating agency revisions, failing to detect sudden geopolitical crises.\n• Narrative Deluge: Institutional news wires generate thousands of qualitative headlines daily without automated, machine-readable quantification.\n• Disconnected Desks: Equity portfolio managers and wholesale banking CROs lack a unified real-time risk signal."
    p_sub.font.size = Pt(9.5); p_sub.font.color.rgb = WHITE; p_sub.space_before = Pt(6)

    # Right Top: Solution Card
    cs = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.55), Inches(5.7), Inches(2.7))
    cs.fill.solid(); cs.fill.fore_color.rgb = CARD_BG
    cs.line.color.rgb = GREEN; cs.line.width = Pt(1.5)
    tf = cs.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.25); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "Our Solution: Continuous Ingestion & AI Risk Signal"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GREEN
    p_sub = tf.add_paragraph()
    p_sub.text = "• Zero-Cost Live Ingestion: Streams institutional news (Yahoo RSS, Bloomberg wires) and social feeds (StockTwits) with sub-25ms parsing latency.\n• Tri-Factor Telemetry: Extracts continuous Sentiment (-1.0 to +1.0), 6-class Taxonomy, and Severity Impact (1 to 10).\n• Synchronous Dual Propagation: Simultaneously tilts index constituents (Module A) and stresses a $1.0B wholesale credit book (Module B)."
    p_sub.font.size = Pt(9.5); p_sub.font.color.rgb = WHITE; p_sub.space_before = Pt(6)

    # Bottom: Live Financial Wire Ingestion Screenshot
    feed_img = os.path.join(DOCS_DIR, "trump_russia_news_feed.png")
    if os.path.exists(feed_img):
        s2.shapes.add_picture(feed_img, Inches(0.8), Inches(4.45), Inches(11.7), Inches(2.55))

    # =========================================================================
    # SLIDE 3: SYSTEM DESIGN & ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "System Design & End-to-End Architecture")

    arch_img_path = os.path.join(DOCS_DIR, "architecture.png")
    if os.path.exists(arch_img_path):
        s3.shapes.add_picture(arch_img_path, Inches(0.8), Inches(1.55), Inches(6.8), Inches(5.3))

    r, c = 5, 2
    t_shape = s3.shapes.add_table(r, c, Inches(7.8), Inches(1.55), Inches(4.7), Inches(5.3))
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
    # SLIDE 4: SIMULATION: AI/NLP TELEMETRY (TRUMP-RUSSIA INFERENCE)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Live Simulation: AI/NLP Inference on 'Trump-Russia Diesel Deal'")

    # Inset Real Screenshot of NLP Telemetry
    telem_img = os.path.join(DOCS_DIR, "trump_russia_telemetry.png")
    if os.path.exists(telem_img):
        s4.shapes.add_picture(telem_img, Inches(0.8), Inches(1.55), Inches(7.3), Inches(3.6))

    # Right Card: Detailed Telemetry Interpretation
    rc = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.55), Inches(4.2), Inches(5.35))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = GOLD; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.25); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "Inference & Propagation Metrics"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GOLD

    telemetry_details = [
        ("Incoming Event", "Headline: 'Trump's Russia Diesel Deal Deepens Ukraine Rift' (Bloomberg)"),
        ("Classification", "Geopolitical Risk (80% Confidence Score)"),
        ("Sentiment Speedometer", "-0.95 (Deep Bearish / Extreme Risk Off)"),
        ("Impact Severity Score", "9.6 / 10.0 (Severe Systemic Shock)"),
        ("Stress Gate Status", "TRIPPED: Severity >= 7.0 automatically cascades into Module B Wholesale Stress Test"),
        ("Identified Assets", "4 Primary Tickers detected: AAPL, NVDA, PLTR, TSLA"),
        ("Inference Speed", "Processed in ~22ms end-to-end")
    ]
    for k, v in telemetry_details:
        p = tf.add_paragraph()
        p.text = f"•  {k}:"
        p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = CYAN; p.space_before = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.size = Pt(9); p2.font.color.rgb = WHITE; p2.space_before = Pt(1)

    # Bottom Table under Screenshot: Scenario Signal Summary
    r, c = 2, 4
    t_shape = s4.shapes.add_table(r, c, Inches(0.8), Inches(5.3), Inches(7.3), Inches(1.6))
    t = t_shape.table
    for ci in range(4): t.columns[ci].width = Inches(1.825)

    telem_table = [
        ("Event Taxonomy", "Sentiment Score", "Impact Severity", "Affected Tickers"),
        ("Geopolitical (80%)", "-0.95 (Bearish)", "9.6 / 10.0 (Critical)", "AAPL, NVDA, PLTR, TSLA")
    ]
    for row_idx, row_data in enumerate(telem_table):
        for col_idx, text_val in enumerate(row_data):
            cell = t.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx == 0 else CARD_BG_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = text_val
            p.font.size = Pt(8.5 if row_idx > 0 else 9.5)
            p.font.bold = (row_idx == 0)
            p.font.color.rgb = GOLD if row_idx == 0 else (RED if col_idx == 1 else WHITE)

    # =========================================================================
    # SLIDE 5: SIMULATION: DOWNSTREAM MODULE A (TACTICAL REBALANCING)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Live Simulation: Module A Tactical Index Rebalancer (Core 15)")

    # Inset Real Screenshot of Module A
    mod_a_img = os.path.join(DOCS_DIR, "trump_russia_module_a.png")
    if os.path.exists(mod_a_img):
        s5.shapes.add_picture(mod_a_img, Inches(0.8), Inches(1.55), Inches(7.3), Inches(5.35))

    # Right Card: Portfolio Dynamics & Bounded Optimization
    rc = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.55), Inches(4.2), Inches(5.35))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = GREEN; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.25); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "Portfolio Rebalancing Highlights"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GREEN

    mod_a_text = [
        ("Trigger Event", "Rebalance applied automatically after 'Trump's Russia Diesel Deal' signal emission."),
        ("Flight-to-Safety Rotation", "Capital rotates out of high-beta tech into fortress balance sheets: MSFT (18.87%), GOOGL (18.87%), and JPM (18.87%) hit the regulatory ceiling."),
        ("Risk Trimming", "High-volatility assets trimmed: TSLA reduced to 1.14%, AMZN reduced to 1.19%, NVDA to 8.45%."),
        ("Regulatory Bounding", "Single-stock constraints enforced [1.0%, 18.87%], preventing unbounded sentiment concentration."),
        ("Performance Metrics", "• Strategy Alpha: +5 bps (+0.05% excess return)\n• Portfolio Turnover: 9.49% (controlled cost)\n• Weights Normalized: Exactly 100.0% sum"),
        ("Dynamic Telemetry", "Sector donut and cumulative alpha timeline update in real time.")
    ]
    for k, v in mod_a_text:
        p = tf.add_paragraph()
        p.text = f"•  {k}:"
        p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = GOLD; p.space_before = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.size = Pt(9); p2.font.color.rgb = WHITE; p2.space_before = Pt(1)

    # =========================================================================
    # SLIDE 6: SIMULATION: DOWNSTREAM MODULE B (WHOLESALE STRESS TEST ON $1.0B BOOK)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Live Simulation: Module B Wholesale Stress Testing ($1.0B Book)")

    # Inset Real Screenshot of Module B
    mod_b_img = os.path.join(DOCS_DIR, "trump_russia_module_b.png")
    if os.path.exists(mod_b_img):
        s6.shapes.add_picture(mod_b_img, Inches(0.8), Inches(1.55), Inches(7.3), Inches(5.35))

    # Right Card: Wholesale Capital Impact & Basel III Solvency
    rc = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.55), Inches(4.2), Inches(5.35))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = RED; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.25); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "Wholesale Capital Stress Breakdown"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = RED

    mod_b_text = [
        ("Macro Shocks Applied", "• Interest Rate Shift (Δy): +104 bps\n• Credit Spread Widening (Δs): +351 bps\n• Basel PD Multiplier: 2.52x (jump-to-default)"),
        ("Capital Loss Breakdown", "• Pre-Stress Book: $1,000.0M ($1.0B)\n• Total Capital Drawdown: -$206.4M (-20.64%)\n• Decomposed across Loans (EL) and Bond mark-to-market duration-convexity"),
        ("Post-Stress Valuation", "Retained Tier-1 Capital: $793.6M (79.36% preservation)"),
        ("Basel III Solvency Floor", "Comfortably survives the 8.0% regulatory minimum capital threshold without breaching bank capital adequacy"),
        ("Credit Migration Heatmap", "• AAA: 0.10% -> 0.25%\n• A: 0.80% -> 2.00%\n• BBB: 1.80% -> 4.50%\n• B: 9.50% -> 23.75% default rate"),
        ("CRO 'What-If' Overrides", "Sliders dynamically synced to the event shock")
    ]
    for k, v in mod_b_text:
        p = tf.add_paragraph()
        p.text = f"•  {k}:"
        p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = GOLD; p.space_before = Pt(5)
        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.size = Pt(8.8); p2.font.color.rgb = WHITE; p2.space_before = Pt(1)

    # =========================================================================
    # SLIDE 7: DOMAIN IMPACT, AI COPILOT & ENGINEERING ROADMAP
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Institutional Domain Impact, AI Copilot & Strategic Roadmap")

    # Left: AI Copilot Screenshot
    copilot_img = os.path.join(DOCS_DIR, "shot_copilot.png")
    if os.path.exists(copilot_img):
        s7.shapes.add_picture(copilot_img, Inches(0.8), Inches(1.55), Inches(4.3), Inches(5.35))

    # Right Top: Institutional Impact Pillars
    rc_top = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.55), Inches(7.2), Inches(2.7))
    rc_top.fill.solid(); rc_top.fill.fore_color.rgb = CARD_BG
    rc_top.line.color.rgb = GOLD; rc_top.line.width = Pt(1.5)
    tf = rc_top.text_frame; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.2); tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "Institutional Business Value & Domain Impact"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GOLD
    p1 = tf.add_paragraph()
    p1.text = "• Pre-Emptive Counterparty Protection: Detects acute geopolitical and credit contagion 3 to 14 days before credit rating agency actions."
    p1.font.size = Pt(9.5); p1.font.color.rgb = WHITE; p1.space_before = Pt(5)
    p2 = tf.add_paragraph()
    p2.text = "• Unifying Risk & Alpha: Bridges quantitative equity managers (tactical rebalancing) and wholesale credit officers (Basel III stress testing) onto a single source of qualitative truth."
    p2.font.size = Pt(9.5); p2.font.color.rgb = WHITE; p2.space_before = Pt(4)
    p3 = tf.add_paragraph()
    p3.text = "• AI Copilot Vision & Mathematical Proof: Risk committees can verify dashboard figures with chart snapshot analysis and Merton Expected Loss formulations."
    p3.font.size = Pt(9.5); p3.font.color.rgb = WHITE; p3.space_before = Pt(4)

    # Right Bottom: 4-Phase Roadmap Timeline Table
    r, c = 2, 4
    t_shape = s7.shapes.add_table(r, c, Inches(5.3), Inches(4.45), Inches(7.2), Inches(2.45))
    t = t_shape.table
    for ci in range(4): t.columns[ci].width = Inches(1.8)

    timeline_data = [
        ("Phase 1: MVP (Done)", "Phase 2: Scale (Q2 2026)", "Phase 3: DMA (Q3 2026)", "Phase 4: Multimodal (Q4)"),
        ("Dual downstream modules + sub-25ms NLP + live crisis simulation.", "Scale to 5,000+ global equities with distributed Celery & Redis.", "Direct Market Access (DMA) FIX protocol order routing into dark pools.", "SEC 10-K filing parser + central bank press conference audio transcription.")
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
            print(f"Trump-Russia Crisis Simulation deck saved to: {path}")
        except PermissionError:
            print(f"Notice: {path} is currently open in another application (e.g. PowerPoint).")
            alt_path = path.replace(".pptx", "_v2.pptx")
            try:
                prs.save(alt_path)
                print(f"Saved alternate copy to: {alt_path}")
            except Exception as e:
                print(f"Failed to save alternate {alt_path}: {e}")

if __name__ == '__main__':
    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOADS_DIR = r"C:\Users\vedan\Downloads"
    paths = [
        os.path.join(DOCS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Trump_Russia_Deck.pptx")
    ]
    build_trump_russia_deck(paths)
