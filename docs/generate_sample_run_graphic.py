import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_sample_graphic(out_path):
    fig, ax = plt.subplots(figsize=(11.5, 5.0), facecolor='#0d0f15')
    ax.set_facecolor('#0d0f15')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Card 1: Input Telemetry
    card1 = patches.FancyBboxPatch((2, 8), 28, 84, boxstyle='round,pad=1.2', facecolor='#161a26', edgecolor='#38bdf8', linewidth=1.5)
    ax.add_patch(card1)
    ax.text(16, 84, 'STEP 1: INGESTION', color='#38bdf8', fontsize=11, fontweight='bold', ha='center')
    ax.text(16, 75, 'Incoming News Wire:', color='#94a3b8', fontsize=8.5, ha='center')
    ax.text(16, 62, 'Middle East Maritime\nConflict Escalates in\nRed Sea Corridor', color='#f8fafc', fontsize=9.5, fontweight='bold', ha='center', style='italic')
    ax.text(16, 44, 'Source: Yahoo RSS & Social\nLatency: ~18ms\nTickers: XOM, CVX, MACRO', color='#cbd5e1', fontsize=8.5, ha='center')
    ax.text(16, 20, 'STATUS: PARSED', color='#10b981', fontsize=8.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#064e3b', edgecolor='#10b981', linewidth=1))

    # Arrow 1 -> 2
    ax.annotate('', xy=(34, 50), xytext=(30.5, 50), arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=2.5))

    # Card 2: AI NLP Risk Engine
    card2 = patches.FancyBboxPatch((35, 8), 28, 84, boxstyle='round,pad=1.2', facecolor='#161a26', edgecolor='#f59e0b', linewidth=1.5)
    ax.add_patch(card2)
    ax.text(49, 84, 'STEP 2: AI/NLP ENGINE', color='#f59e0b', fontsize=11, fontweight='bold', ha='center')
    ax.text(49, 74, 'FinBERT + Lexicon Scorer', color='#94a3b8', fontsize=8.5, ha='center')
    ax.text(49, 62, 'Event: Geopolitical', color='#f8fafc', fontsize=10, fontweight='bold', ha='center')
    ax.text(49, 52, 'Sentiment: -0.75 (Bearish)', color='#ef4444', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(49, 42, 'Impact Score: 8.4 / 10.0', color='#f59e0b', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(49, 32, 'Confidence: 96.0%', color='#38bdf8', fontsize=8.5, ha='center')
    ax.text(49, 20, 'TRIGGER GATE: ACTIVE', color='#ef4444', fontsize=8, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#450a0a', edgecolor='#ef4444', linewidth=1))

    # Arrow 2 -> 3
    ax.annotate('', xy=(67, 50), xytext=(63.5, 50), arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2.5))

    # Card 3: Dual Downstream Cascade
    card3 = patches.FancyBboxPatch((68, 8), 30, 84, boxstyle='round,pad=1.2', facecolor='#161a26', edgecolor='#10b981', linewidth=1.5)
    ax.add_patch(card3)
    ax.text(83, 84, 'STEP 3: DUAL CASCADE', color='#10b981', fontsize=11, fontweight='bold', ha='center')

    # Module A
    ax.text(83, 73, 'MODULE A: TACTICAL REBALANCE', color='#38bdf8', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(83, 63, 'Tilt: XOM -> 14.0% | Tech Trimmed\nAlpha: +34.2 bps | Turnover: 6.8%', color='#f8fafc', fontsize=8, ha='center')

    # Divider line
    ax.plot([71, 95], [52, 52], color='#334155', lw=1)

    # Module B
    ax.text(83, 44, 'MODULE B: WHOLESALE STRESS ($1.0B)', color='#f59e0b', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(83, 33, 'Shocks: Dy=+75bps, Ds=+150bps, PD=1.65x\nTotal Loss: -$60.0M (-6.00%)\nRetained Capital: $940.0M (94.0%)', color='#f8fafc', fontsize=7.8, ha='center')
    ax.text(83, 16, 'BASEL III COMPLIANT (>8.0%)', color='#10b981', fontsize=8, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#064e3b', edgecolor='#10b981', linewidth=1))

    plt.tight_layout()
    plt.savefig(out_path, dpi=240, facecolor='#0d0f15')
    plt.close()
    print(f"Sample run graphic saved to: {out_path}")

if __name__ == '__main__':
    generate_sample_graphic('docs/slide_sample_run.png')
