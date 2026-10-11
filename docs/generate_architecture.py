import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCH_PATH = os.path.join(DOCS_DIR, "architecture.png")

fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#07080c')
ax.set_facecolor('#07080c')

ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Title
ax.text(8, 8.4, "S&P Global × CRISIL — Unified AI/NLP Financial Risk Architecture", 
        fontsize=18, fontweight='bold', color='#f59e0b', ha='center', fontfamily='sans-serif')
ax.text(8, 8.0, "Multi-Source Telemetry → Structured Signal Inference → Tactical Rebalancing & Wholesale Stress Testing", 
        fontsize=10, color='#94a3b8', ha='center', fontfamily='sans-serif')

def draw_box(x, y, w, h, title, subtitle, border_color, fill_color='#0e111a'):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.2",
                                  linewidth=1.5, edgecolor=border_color, facecolor=fill_color)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.35, title, fontsize=10, fontweight='bold', color='#ffffff', ha='center')
    ax.text(x + w/2, y + 0.35, subtitle, fontsize=8, color='#94a3b8', ha='center')

def draw_arrow(x1, y1, x2, y2, color='#f59e0b'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5, mutation_scale=15))

# 1. Ingestion Layer
draw_box(0.8, 5.2, 3.2, 1.8, "1. Ingestion Feeds", "Yahoo Finance RSS\nStockTwits REST API\nCrisis Replay Engine", "#38bdf8")

# 2. Preprocessing & Extraction
draw_box(4.6, 5.2, 3.0, 1.8, "2. Preprocessing", "Ticker Extraction\nText Normalization\nToken Cleansing", "#818cf8")

# 3. Core AI/NLP Risk Engine
draw_box(8.2, 4.8, 3.4, 2.4, "3. Core NLP Engine", "FinBERT Sentiment (-1 to +1)\n6-Class Event Categorizer\nImpact Severity (1 to 10)", "#f59e0b", fill_color='#141824')

# 4. Signal Store & API
draw_box(12.2, 5.2, 3.0, 1.8, "4. Signal Ledger & API", "SQLite + SQLAlchemy\nFastAPI REST Service\nJWT & RBAC Security", "#10b981")

# 5. Module A: Tactical Rebalancer
draw_box(2.2, 1.4, 4.8, 2.2, "Module A: Tactical Rebalancer", "S&P 15 Blue-Chip Index\nDynamic Sentiment Weights (1%-18%)\nTurnover & Alpha Tracking", "#10b981", fill_color='#0e151d')

# 6. Module B: Wholesale Stress Tester
draw_box(9.0, 1.4, 4.8, 2.2, "Module B: Wholesale Stress Tester", "Synthetic $1.04B Portfolio\nLoans (Basel EL), Bonds (Dur/Cvx), Swaps\nMulti-Factor Shock Transmission", "#ef4444", fill_color='#181116')

# Connecting Arrows
draw_arrow(4.0, 6.1, 4.6, 6.1, '#38bdf8')
draw_arrow(7.6, 6.1, 8.2, 6.1, '#818cf8')
draw_arrow(11.6, 6.1, 12.2, 6.1, '#f59e0b')

# Arrows to downstream modules
draw_arrow(9.2, 4.8, 5.0, 3.6, '#10b981')
draw_arrow(10.6, 4.8, 11.0, 3.6, '#ef4444')

# Presentation / UI Banner
ax.text(8, 0.4, "Interactive ISTC-Style Quantitative Web Cockpit (Tailwind + Chart.js + Live Ticker)",
        fontsize=9, color='#64748b', ha='center', fontfamily='monospace')

plt.tight_layout()
plt.savefig(ARCH_PATH, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print(f"Architecture diagram saved to {ARCH_PATH}")
