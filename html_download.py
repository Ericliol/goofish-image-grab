from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up options for headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

# Use webdriver-manager to install correct ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Load the target Goofish page
url = ## product URL
driver.get(url)

# Wait for JS to render
time.sleep(5)

# Save rendered HTML
with open("goofish_item_rendered.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("Rendered HTML saved.")

driver.quit()
