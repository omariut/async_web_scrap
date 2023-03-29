from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Launch Chrome with Selenium
driver = webdriver.Chrome()
driver.get("https://example.com")

# Wait for page to load
time.sleep(5)

# Scroll to bottom of page to load all content
elem = driver.find_element_by_tag_name("body")
while True:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    if driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
        break

# Capture page source after all content is loaded
html = driver.page_source

# Close Selenium driver
driver.quit()

# Parse HTML with bs4
soup = BeautifulSoup(html, "html.parser")

# Extract data from soup

