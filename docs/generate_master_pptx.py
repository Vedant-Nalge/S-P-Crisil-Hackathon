import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_master_presentation(output_paths):
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
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title, section_tag="S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026"):
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

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "S&P GLOBAL × CRISIL CAMPUS HACKATHON 2026 // CASE STUDY SUBMISSION"
    p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = GOLD

    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.8))
    tf = tb_title.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "AI/NLP Financial Risk Engine & Dual Downstream Intelligence Platform"
    p1.font.size = Pt(30); p1.font.bold = True; p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "A Multi-Source Unstructured Text Pipeline Powering Tactical Index Rebalancing & Wholesale Banking Stress Testing"
    p2.font.size = Pt(14); p2.font.color.rgb = CYAN; p2.space_before = Pt(8)

    # Metadata Table
    rows, cols = 5, 2
    table_shape = s1.shapes.add_table(rows, cols, Inches(0.8), Inches(3.4), Inches(11.7), Inches(2.6))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(8.5)

    meta = [
        ("Candidate Name", "Vedant Dilip Nalge"),
        ("College / Campus", "Indian Institute of Technology Madras (me22b162@smail.iitm.ac.in)"),
        ("Target Track", "AI/NLP Financial Risk Engine (FinBERT Continuous Sentiment & 6-Class Taxonomy)"),
        ("Downstream Implementations", "Simultaneous Delivery: Module A (Tactical Rebalancer) & Module B (Wholesale Stress Tester)"),
        ("Core Architecture", "FastAPI (Async REST) + SQLite (ACID Persistence) + Tailwind/Chart.js + PyPPTX")
    ]
    for i, (k, v) in enumerate(meta):
        cell_k = table.cell(i, 0); cell_v = table.cell(i, 1)
        cell_k.fill.solid(); cell_k.fill.fore_color.rgb = CARD_BG
        cell_v.fill.solid(); cell_v.fill.fore_color.rgb = CARD_BG_ALT
        pk = cell_k.text_frame.paragraphs[0]; pk.text = k; pk.font.bold = True; pk.font.size = Pt(11); pk.font.color.rgb = GOLD
        pv = cell_v.text_frame.paragraphs[0]; pv.text = v; pv.font.size = Pt(11); pv.font.color.rgb = WHITE

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
        p.text = label; p.alignment = PP_ALIGN.CENTER; p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = col

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
        pk = cell_k.text_frame.paragraphs[0]; pk.text = layer_name; pk.font.bold = True; pk.font.size = Pt(10.5); pk.font.color.rgb = GOLD
        pv = cell_v.text_frame.paragraphs[0]; pv.text = desc; pv.font.size = Pt(9.5); pv.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 4: SAMPLE RUN FROM LIVE WEBSITE DASHBOARD (ACTUAL SCREENSHOT)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Sample Run: Live Dashboard NLP Telemetry & Inference")

    # Embed Live Dashboard Screenshot of Active Telemetry
    telemetry_img = os.path.join(DOCS_DIR, "shot_telemetry_active.png")
    if os.path.exists(telemetry_img):
        s4.shapes.add_picture(telemetry_img, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Card: Sample Run Narrative & Pipeline Metrics
    rc = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = GOLD; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Actual Live Telemetry Execution"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = GOLD

    steps_text = [
        ("1. Input Event Narrative", "Headline: 'Middle East Maritime Conflict: Escalation in Red Sea Threatens Global Energy Corridors'\nIngested in 18ms via Yahoo Finance RSS stream."),
        ("2. AI NLP Telemetry Output", "• Event Class: Geopolitical (96.0% Conf)\n• Sentiment Score: -0.75 (Bearish Defensives)\n• Severity Impact: 8.4 / 10.0 (Stress Trigger Gate Active)\n• Entities Detected: XOM, CVX, OIL, MACRO"),
        ("3. Dual Downstream Cascade", "• Module A: Tech trimmed (-3.2%); Energy tilted (+4.8%)\n• Module B: Shocked by Δy=+75bps, Δs=+150bps, PD=1.65x\n• Capital Loss: -$60.0M (-6.00%) | Retained: $940.0M")
    ]
    for head, body in steps_text:
        p = tf.add_paragraph()
        p.text = head
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = CYAN; p.space_before = Pt(10)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5); p2.font.color.rgb = WHITE; p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: DOWNSTREAM MODULE A: TACTICAL REBALANCER (ACTUAL SCREENSHOT)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Module A: Tactical Index Rebalancer (Live Dashboard View)")

    # Embed Live Dashboard Screenshot of Module A
    mod_a_img = os.path.join(DOCS_DIR, "shot_module_a.png")
    if os.path.exists(mod_a_img):
        s5.shapes.add_picture(mod_a_img, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Card: Module A Quantitative Validation
    rc = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = GREEN; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Module A Quantitative Highlights"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = GREEN

    mod_a_points = [
        ("Constituent Weights Bounding", "Enforces strict regulatory concentration limits: single-stock weights are bounded between 1.0% and 18.0%, preventing over-concentration in sentiment spikes."),
        ("+34.2 bps Strategy Alpha", "Generates +0.342% annualized excess return over equal-weight benchmark by tilting into momentum leaders."),
        ("Controlled Turnover (6.8%)", "Constrains portfolio turnover to 6.8%, minimizing transaction slippage and execution costs."),
        ("Dynamic Sector Donut & Alpha Line", "Live Chart.js widgets recalculate Tech (46%), Financials (18%), Healthcare (12%), Consumer (14%), and Energy (10%) on every sentiment shock.")
    ]
    for head, body in mod_a_points:
        p = tf.add_paragraph()
        p.text = f"•  {head}:"
        p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = GOLD; p.space_before = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5); p2.font.color.rgb = WHITE; p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: DOWNSTREAM MODULE B: WHOLESALE STRESS TESTER (ACTUAL SCREENSHOT)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Module B: Strategic Wholesale Banking Stress Tester (Live View)")

    # Embed Live Dashboard Screenshot of Module B
    mod_b_img = os.path.join(DOCS_DIR, "shot_module_b.png")
    if os.path.exists(mod_b_img):
        s6.shapes.add_picture(mod_b_img, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Card: Module B Stress Testing & Capital Adequacy
    rc = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2))
    rc.fill.solid(); rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = RED; rc.line.width = Pt(1.5)
    tf = rc.text_frame; tf.margin_left = Inches(0.35); tf.margin_top = Inches(0.3); tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Module B Stress Testing Breakdown"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = RED

    mod_b_points = [
        ("Synthetic $1.0B Credit Book", "Models 15 syndicated wholesale facilities: $550M Commercial Loans, $450M Corporate Bonds, and $250M Derivative Hedges across AAA to B ratings."),
        ("Multi-Factor Factor Transmission", "Perturbs Treasury Yield Shift (Δy = +75 bps), Credit Spread Widening (Δs = +150 bps), and Basel PD Default Multiplier (1.65x)."),
        ("Dual Valuation Loss Decomp", "• Bonds Mark-to-Market: -$38.0M (Duration-Convexity)\n• Loans Expected Loss (EL): -$18.0M (Merton Structural)\n• Swaps DV01 MTM: -$4.0M"),
        ("Basel III Solvency Preserved", "Total Loss: -$60.0M (-6.00% Drawdown). Preserves $940.0M (94.0%) Tier-1 capital, comfortably exceeding the 8.0% regulatory floor.")
    ]
    for head, body in mod_b_points:
        p = tf.add_paragraph()
        p.text = f"•  {head}:"
        p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = GOLD; p.space_before = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5); p2.font.color.rgb = WHITE; p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 7: AI COPILOT, DOMAIN IMPACT & FUTURE ROADMAP (ACTUAL SCREENSHOT)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "AI Copilot Intelligence, Domain Impact & Roadmap")

    # Embed Live Screenshot of AI Copilot Chatbot Drawer on Left
    copilot_img = os.path.join(DOCS_DIR, "shot_copilot.png")
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
    p2.text = "• Cross-Asset Silo Breakdown: Provides a unified qualitative truth feeding equity PMs and credit CROs."
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

    # Save Presentation
    for path in output_paths:
        prs.save(path)
        print(f"Master presentation with live dashboard screenshots saved to: {path}")

if __name__ == '__main__':
    DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOADS_DIR = r"C:\Users\vedan\Downloads"
    paths = [
        os.path.join(DOCS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "presentation.pptx"),
        os.path.join(DOWNLOADS_DIR, "IITM_Vedant_Nalge_Presentation.pptx")
    ]
    build_master_presentation(paths)
