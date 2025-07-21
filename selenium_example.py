from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Setup Chrome WebDriver with automatic ChromeDriver installation
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Navigate to a website
        driver.get("https://www.google.com")
        
        # Find search box element
        search_box = driver.find_element(By.NAME, "q")
        
        # Type in search
        search_box.send_keys("Selenium with Python")
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results to load (up to 10 seconds)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        
        # Print the title of the page
        print(f"Page title: {driver.title}")
        
        # Example of finding multiple elements
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        print(f"Found {len(search_results)} search results")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Always close the browser
        driver.quit()

if __name__ == "__main__":
    main() 