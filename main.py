import threading
import time
import requests
import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

urls = settings["urls"]

stop_event = threading.Event()

def monitor_url(url):
    while not stop_event.is_set():
        try:
            response = requests.get(url, timeout=5)
            print(f"[{url}] Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"[{url}] Error: {e}")
        time.sleep(5)
        
threads = []
for url in urls:
    t = threading.Thread(target=monitor_url, args=(url,))
    threads.append(t)
    t.start()

try:
    time.sleep(60)
except KeyboardInterrupt:
    print("Interrupted by user.")
    
stop_event.set()
for t in threads:
    t.join()
    
print("Monitoring stopped.")