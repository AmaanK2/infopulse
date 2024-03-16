import requests
from bs4 import BeautifulSoup
import csv

# URL of the site to scrape
url = 'https://www.cbc.ca/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links that might lead to news articles
articles = soup.find_all('a', href=True)

news = []
for article in articles:
    if '/news/' in article['href']:
        title = article.text.strip()
        link = article['href']
        # Filter out empty titles or duplicate links
        if title and link not in [n[1] for n in news]:
            news.append((title, link))

# Assuming you want to write these to a CSV file
csv_file_path = 'cbc_news_items.csv'  # Specify your desired file path

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Title', 'Link'])
    # Limiting to first 5 items to match the provided code snippet
    writer.writerows(news)

print(f"Saved the first 5 news items to '{csv_file_path}'")
