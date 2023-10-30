import requests
from bs4 import BeautifulSoup
import os

dir = os.path.join(os.getcwd(), 'data')

# Create a directory to store the links
os.makedirs(dir, exist_ok=True)

# Get the HTML content of the page
base_url = 'https://plantvillage.psu.edu/plants'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the links under the div with col-md-3 col-sm-2 topics_item
links = soup.select('div.col-md-3.col-sm-2.topics_item a')

# Get the href attribute of each link
links = [f'https://plantvillage.psu.edu{link["href"]}' for link in links if link['href'].endswith('/infos')]

# Remove duplicate links
links = list(set(links))

# Save the links to a file
links_dir = os.path.join(dir, 'links.txt')
with open(links_dir, 'w') as f:
    f.write('\n'.join(links))