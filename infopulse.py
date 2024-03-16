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
        link = 'https://www.cbc.ca' + article['href'] if not article['href'].startswith('http') else article['href']
        if link not in [n[4] for n in news]:
            article_page = requests.get(link)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')
            print(article_soup)
            title = article_soup.find('h1').text.strip() if article_soup.find('h1') else 'N/A'
            category_element = article_soup.find('span', {'class': 'sclt-storySectionLink'})
            category = category_element.text.strip() if category_element else 'N/A'
            summary_element = article_soup.find('div', {'class': 'detailSummary'})
            summary = summary_element.text.strip() if summary_element else 'N/A'
            image_element = article_soup.find('img')
            image_link = image_element['src'] if image_element and image_element.has_attr('src') else 'N/A'

            news.append((title, category, summary, image_link, link))

# Assuming you want to write these to a CSV file
csv_file_path = 'cbc_news_items.csv'  # Specify your desired file path

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Category', 'Summary', 'Image Link', 'Article Link'])
    writer.writerows(news)

print(f"Saved news items to '{csv_file_path}'")
