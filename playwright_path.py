import os
def get_playwright_browsers_path():
    # You can customize this path if needed
    return os.path.join(os.getcwd(), ".playwright-browsers")