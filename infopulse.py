import requests
from bs4 import BeautifulSoup
import csv
import re  # Import regular expressions module for the pattern check

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
        # Use regular expression to check if link ends with a number
        if re.search(r'\d+$', link):
            article_page = requests.get(link)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')
            title = article_soup.find('h1').text.strip() if article_soup.find('h1') else 'N/A'
            category_element = article_soup.find('span', {'class': 'sclt-storySectionLink'})
            category = category_element.text.strip() if category_element else 'N/A'
            summary_element = article_soup.find('div', {'class': 'detailSummary'})
            summary = summary_element.text.strip() if summary_element else 'N/A'

            # Find the image within the specified structure
            image_element = article_soup.find('figure', {'class': 'imageMedia leadmedia-story full'})
            image_placeholder = image_element.find('div', {'class': 'placeholder'}) if image_element else None
            image = image_placeholder.find('img') if image_placeholder else None
            image_link = image['src'] if image and image.has_attr('src') else 'N/A'

            if not (category == 'News' and image_link == 'N/A'):
                news.append((title, category, summary, image_link, link))

# Assuming you want to write these to a CSV file
csv_file_path = 'cbc_news_items.csv'  # Specify your desired file path

# Open the file with 'w' mode to write the data
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Category', 'Summary', 'Image Link', 'Article Link'])
    writer.writerows(news)

print(f"Saved news items to '{csv_file_path}'")
