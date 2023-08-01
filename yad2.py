import requests
import sqlite3
from bs4 import BeautifulSoup

def create_database():
    # Connect to the database (create it if it doesn't exist)
    conn = sqlite3.connect("house_database.db")
    cursor = conn.cursor()

    # Create a table to store the house data
    cursor.execute('''CREATE TABLE IF NOT EXISTS houses
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT,
                       price TEXT,
                       address TEXT,
                       num_beds TEXT,
                       num_baths TEXT,
                       sqft TEXT)''')

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

def scrape_house_data():
    url = "https://www.zillow.com/homes/for_sale/"

    # Send an HTTP GET request to the website
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract house data from the website's HTML content
        house_data = []
        houses = soup.find_all("li", class_="list-card")
        for house in houses:
            title = house.find("div", class_="list-card-title").text
            price = house.find("div", class_="list-card-price").text
            address = house.find("address", class_="list-card-addr").text
            num_beds = house.find("ul", class_="list-card-details").find_all("li")[0].text
            num_baths = house.find("ul", class_="list-card-details").find_all("li")[1].text
            sqft = house.find("ul", class_="list-card-details").find_all("li")[2].text

            # Store the data in a list of tuples
            house_data.append((title, price, address, num_beds, num_baths, sqft))

        # Connect to the database
        conn = sqlite3.connect("house_database.db")
        cursor = conn.cursor()

        # Insert the house data into the database
        cursor.executemany("INSERT INTO houses (title, price, address, num_beds, num_baths, sqft) VALUES (?, ?, ?, ?, ?, ?)", house_data)

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        print("House data successfully stored in the database.")
    else:
        print("Failed to fetch the website.")

def show_houses_from_database():
    # Connect to the database
    conn = sqlite3.connect("house_database.db")
    cursor = conn.cursor()

    # Fetch house data from the database
    cursor.execute("SELECT * FROM houses")
    houses = cursor.fetchall()

    # Print the house data
    for house in houses:
        print(f"Title: {house[1]}")
        print(f"Price: {house[2]}")
        print(f"Address: {house[3]}")
        print(f"Number of Beds: {house[4]}")
        print(f"Number of Baths: {house[5]}")
        print(f"Square Footage: {house[6]}")
        print("-" * 30)

    # Close the database connection
    conn.close()

# Create the database (if it doesn't exist) and fetch house data
create_database()
scrape_house_data()

# Show the houses in the database
show_houses_from_database()
