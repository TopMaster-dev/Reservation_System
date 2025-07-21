import threading
import time
import json
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

# Load URLs from settings.json
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

urls = settings["urls"]
stop_event = threading.Event()

def create_driver():
    # Configure Chrome options for headless operation
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Create and return a new Chrome driver instance
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

# Function to monitor each URL
def monitor_url(url):
    driver = create_driver()
    
    try:
        while not stop_event.is_set():
            try:
                # Load the page
                driver.get(url)
                
                # Get page title as verification that page loaded properly
                title = driver.title
                print(f"[{url}] Status: OK - Title: {title}")
                
            except WebDriverException as e:
                print(f"[{url}] Error: {str(e)}")
                print(f"❌ Error detected. Opening {url} in browser...")
                webbrowser.open(url)
            
            time.sleep(5)
    
    finally:
        # Clean up the driver
        try:
            driver.quit()
        except:
            pass

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