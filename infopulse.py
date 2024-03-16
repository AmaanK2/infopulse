import requests
from bs4 import BeautifulSoup
import csv

# URL of the site to scrape
url = 'https://www.cbc.ca/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links that might lead to news articles
articles = soup.find_all('a', href=True)

# Filter the articles to get unique links that contain '/news/'
news_links = set()
for article in articles:
    href = article['href']
    if '/news/' in href and href not in news_links:
        news_links.add(href)

news_data = []
for link in news_links:
    article_url = link if link.startswith('http') else f'https://www.cbc.ca{link}'
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    title = article_soup.find('h1').text.strip() if article_soup.find('h1') else ''
    category = article_soup.find('a', {'class': 'category'}).text.strip() if article_soup.find('a', {'class': 'category'}) else ''
    summary = article_soup.find('p').text.strip() if article_soup.find('p') else ''
    image_link = article_soup.find('img')['src'] if article_soup.find('img') else ''

    news_data.append((title, category, summary, image_link, article_url))

# Specify your desired file path
csv_file_path = 'cbc_news_items.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Category', 'Summary', 'Image Link', 'Article Link'])
    writer.writerows(news_data)

print(f"Saved news items to '{csv_file_path}'")

