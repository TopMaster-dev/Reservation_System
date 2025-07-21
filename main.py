import time
import json
import webbrowser
import subprocess
import sys
from playwright.sync_api import sync_playwright

def ensure_playwright_browsers():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Playwright browsers installed successfully")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install Playwright browsers:", e)
        sys.exit(1)

class URLMonitor:
    def __init__(self):
        # Load URLs from settings.json
        with open("settings.json", "r", encoding="utf-8") as f:
            self.settings = json.load(f)
        self.urls = self.settings["urls"]
        self.running = True
        self.pages = []

    def monitor_urls(self):
        """Monitor all URLs, one tab per URL, refreshing each tab."""
        ensure_playwright_browsers()
        with sync_playwright() as playwright:
            # Launch browser in visible mode
            browser = playwright.chromium.launch(headless=False)
            try:
                # Open one page per URL and keep it open
                self.pages = [browser.new_page() for _ in self.urls]
                for page, url in zip(self.pages, self.urls):
                    page.goto(url, wait_until="networkidle", timeout=60000)
                    print(f"✅ Opened {url}")
                print(f"✅ Monitoring {len(self.urls)} URLs. Press Ctrl+C to stop.")
                while self.running:
                    for page, url in zip(self.pages, self.urls):
                        try:
                            page.reload(wait_until="networkidle", timeout=60000)
                            title = page.title()
                            print(f"[{url}] Status: OK - Title: {title}")
                        except Exception as e:
                            print(f"[{url}] Error: {str(e)}")
                            print(f"❌ Error detected. Opening {url} in system browser...")
                            webbrowser.open(url)
                    time.sleep(5)
            finally:
                for page in self.pages:
                    try:
                        page.close()
                    except:
                        pass
                try:
                    browser.close()
                except:
                    pass
    def stop(self):
        print("\n⛔ Stopping monitoring...")
        self.running = False
        print("✅ Monitoring stopped.")

def main():
    monitor = URLMonitor()
    try:
        monitor.monitor_urls()
    except KeyboardInterrupt:
        monitor.stop()

if __name__ == "__main__":
    main()