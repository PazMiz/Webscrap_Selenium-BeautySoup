
from selenium import webdriver 
from selenium.webdriver.common.by import By
import sqlite3

driver = webdriver.Chrome()
driver.get("http://books.toscrape.com/catalogue/page-8.html")

# Connect to SQLite database
conn = sqlite3.connect('books.db')
c = conn.cursor()

# Create table 
c.execute('''CREATE TABLE IF NOT EXISTS books 
             (id INTEGER PRIMARY KEY, title TEXT, price TEXT, availability TEXT)''')

books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

for book in books:
  title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
  price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
  availability = book.find_element(By.CSS_SELECTOR, "p.instock.availability").text

  # Insert book data into database
  c.execute("INSERT INTO books VALUES (NULL, ?, ?, ?)", (title, price, availability))

# Commit changes and close connection
conn.commit()
conn.close()

driver.quit()


