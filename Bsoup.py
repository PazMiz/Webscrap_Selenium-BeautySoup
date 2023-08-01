import requests
from bs4 import BeautifulSoup

url = 'https://pazmiz.github.io/Html_Shir/index.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Get all div elements
divs = soup.find_all('div')
print(f"Number of divs: {len(divs)}")

# Get all anchor elements
anchors = soup.find_all('a')

# Print href for each anchor
print(f"Found {len(anchors)} anchor tags:")
for anchor in anchors:
    href = anchor.get('href')
    print(href)
