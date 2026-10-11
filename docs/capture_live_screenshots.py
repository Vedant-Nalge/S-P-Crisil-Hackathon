import time
import os
from playwright.sync_api import sync_playwright

def capture_dashboard_screenshots():
    docs_dir = os.path.dirname(os.path.abspath(__file__))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 1600, 'height': 1050}, device_scale_factor=1.5)
        page = context.new_page()

        # Step 0: Capture Login Portal
        print("Navigating to http://127.0.0.1:8000/login ...")
        page.goto('http://127.0.0.1:8000/login')
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(docs_dir, "shot_login.png"))
        print("Captured Login Gateway!")

        # Step 1: Perform FastPass Login
        print("Logging in via FastPass as Chief Risk Officer (admin)...")
        page.evaluate("() => fastPassLogin('admin')")
        page.wait_for_timeout(3000)

        # Step 2: Main Telemetry & Ingestion Dashboard
        print("Capturing Main Dashboard Hero...")
        page.screenshot(path=os.path.join(docs_dir, "shot_telemetry_hero.png"))

        # Step 3: Trigger Scenario Replay to populate active gauges
        print("Triggering Crisis Scenario Replay (EVT-GEO-001)...")
        page.evaluate("() => triggerScenarioReplayWithId('EVT-GEO-001')")
        page.wait_for_timeout(2500)

        # Scroll to Telemetry Card with gauges and detect tickers
        page.evaluate("() => document.getElementById('customHeadline')?.scrollIntoView({behavior: 'instant', block: 'center'})")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(docs_dir, "shot_telemetry_active.png"))
        print("Captured Active NLP Telemetry & Gauges!")

        # Step 4: Module A - Tactical Index Rebalancer
        print("Capturing Module A Tactical Rebalancer...")
        page.evaluate("() => switchAppTab('module-a')")
        page.wait_for_timeout(2000)
        page.evaluate("() => document.getElementById('tabContent-module-a')?.scrollIntoView({behavior: 'instant', block: 'start'})")
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(docs_dir, "shot_module_a.png"))
        print("Captured Module A!")

        # Step 5: Module B - Wholesale Banking Stress Tester
        print("Capturing Module B Wholesale Banking Stress Tester...")
        page.evaluate("() => switchAppTab('module-b')")
        page.wait_for_timeout(2000)
        page.evaluate("() => document.getElementById('tabContent-module-b')?.scrollIntoView({behavior: 'instant', block: 'start'})")
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(docs_dir, "shot_module_b.png"))
        print("Captured Module B!")

        # Step 6: AI Copilot Chatbot Drawer
        print("Capturing AI Copilot Chatbot Drawer...")
        page.evaluate("() => toggleCopilotChat()")
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(docs_dir, "shot_copilot.png"))
        print("Captured AI Copilot!")

        browser.close()
        print("ALL LIVE DASHBOARD SCREENSHOTS CAPTURED SUCCESSFULLY!")

if __name__ == '__main__':
    capture_dashboard_screenshots()
