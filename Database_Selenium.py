import os
import requests
from bs4 import BeautifulSoup
import sqlite3

def get_absolute_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def scrape_books_to_scrape():
    url = "http://books.toscrape.com/catalogue/page-3.html"

    # Send an HTTP GET request to the website
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract data from the website's HTML content
        books = soup.find_all("article", class_="product_pod")

        # Store the data in an SQLite database
        db_path = get_absolute_path("books_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create a table to store the data if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT,
                           price TEXT,
                           availability TEXT)''')

        # Clear the existing data from the table before reinserting (optional)
        cursor.execute("DELETE FROM books")

        for book in books:
            book_title = book.h3.a["title"]
            book_price = book.find("p", class_="price_color").text.strip()
            book_availability = book.find("p", class_="instock availability").text.strip()

            # Insert the data into the database
            cursor.execute("INSERT INTO books (title, price, availability) VALUES (?, ?, ?)",
                           (book_title, book_price, book_availability))
            conn.commit()

        # Close the database connection
        conn.close()

        print("Data successfully stored in the SQLite database.")
    else:
        print("Failed to fetch the website.")

def fetch_data_from_database():
    db_path = get_absolute_path("books_data.db")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a query to fetch data from the 'books' table
    cursor.execute("SELECT id, title, price, availability FROM books")

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    if not rows:
        print("No data found in the database.")
    else:
        # Process and use the fetched data
        for row in rows:
            book_id, book_title, book_price, book_availability = row
            print(f"Book ID: {book_id}")
            print(f"Title: {book_title}")
            print(f"Price: {book_price}")
            print(f"Availability: {book_availability}")
            print("-" * 30)

    # Close the database connection
    conn.close()

# First, scrape the website and store data in the database
scrape_books_to_scrape()

# Then, fetch and print the data from the database
fetch_data_from_database()

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


