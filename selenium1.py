from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://pazmiz.github.io/Html_Shir/index.html")

# Get all anchor elements
anchors = driver.find_elements(By.TAG_NAME, "a")

# Get all div elements
divs = driver.find_elements(By.TAG_NAME, "div")
print("Number of divs:", len(divs)) 

# Print href for each anchor
print(f"Found {len(anchors)} anchor tags:")
for anchor in anchors:
    href = anchor.get_attribute("href") 
    print(href)

driver.quit()

