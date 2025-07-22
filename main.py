import time
import json
import threading
import subprocess
import sys
from playwright.sync_api import sync_playwright, TimeoutError

def ensure_playwright_browsers():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Playwright Chromium installed")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install browsers:", e)
        sys.exit(1)

class URLMonitorThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.running = True

    def run(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                page = browser.new_page()
                while self.running:
                    try:
                        print(f"🌐 Loading: {self.url}")
                        page.goto(self.url, wait_until="networkidle", timeout=120000)
                        print(f"✅ Loaded: {self.url} | Title: {page.title()}")
                        try:
                            page.wait_for_selector('a[href="#tabCont1"]', timeout=10000)
                            page.click('a[href="#tabCont1"]')
                            print(f"👉 Clicked button on {self.url}")
                        except TimeoutError:
                            print(f"⚠️ Button not found on {self.url}")
                        while self.running:
                            time.sleep(5)
                    except TimeoutError:
                        print(f"⏳ Timeout: {self.url} - Reloading in 5 seconds...")
                        time.sleep(5)
                    except Exception as e:
                        print(f"❌ Error at {self.url}: {e} - Retrying in 5 seconds...")
                        time.sleep(5)
        except Exception as e:
            print(f"❌ Fatal thread error ({self.url}): {e}")
        finally:
            try:
                page.close()
                browser.close()
            except:
                pass

def load_settings():
    with open("settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    return settings["urls"]

def main():
    ensure_playwright_browsers()
    urls = load_settings()

    threads = []
    for url in urls:
        t = URLMonitorThread(url)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Stopping all monitors...")
        for t in threads:
            t.running = False
        for t in threads:
            t.join()
        print("✅ All threads stopped.")

if __name__ == "__main__":
    main()