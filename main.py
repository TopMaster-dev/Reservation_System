import threading
import time
import json
import webbrowser
import asyncio
import subprocess
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def ensure_playwright_browsers():
    try:
        # Try to install browsers if not already installed
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Playwright browsers installed successfully")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install Playwright browsers:", e)
        sys.exit(1)

# Load URLs from settings.json
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

urls = settings["urls"]
stop_event = threading.Event()

def create_browser():
    # Start Playwright and launch browser
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=True,  # Run in headless mode
    )
    return playwright, browser

# Function to monitor each URL
def monitor_url(url):
    playwright, browser = create_browser()
    
    try:
        context = browser.new_context()
        page = context.new_page()
        
        while not stop_event.is_set():
            try:
                # Navigate to the URL with a timeout of 30 seconds
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Get page title
                title = page.title()
                print(f"[{url}] Status: OK - Title: {title}")
                
            except Exception as e:
                print(f"[{url}] Error: {str(e)}")
                print(f"❌ Error detected. Opening {url} in browser...")
                webbrowser.open(url)
            
            time.sleep(5)
    
    finally:
        # Clean up resources
        try:
            context.close()
            browser.close()
            playwright.stop()
        except:
            pass

def main():
    # Ensure browsers are installed
    ensure_playwright_browsers()
    
    # Start threads
    threads = []
    for url in urls:
        t = threading.Thread(target=monitor_url, args=(url,))
        t.start()
        threads.append(t)

    print("✅ Monitoring started. Press Ctrl+C to stop.")

    # Monitor until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")
        stop_event.set()  # Signal threads to stop

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("✅ Monitoring stopped.")

if __name__ == "__main__":
    main()