import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import re

# Initialize the Google Sheets client
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("cbc_news_items").sheet1

# Function to check if an article already exists in the sheet
def article_exists(article_link, existing_links):
    return article_link in existing_links

# Scrape the website
url = 'https://www.cbc.ca/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links that might lead to news articles
articles = soup.find_all('a', href=True)

# List to store new articles
new_articles = []

# Retrieve all existing links to check for duplicates
existing_links = sheet.col_values(5)

for article in articles:
    if '/news/' in article['href']:
        link = 'https://www.cbc.ca' + article['href'] if not article['href'].startswith('http') else article['href']
        if re.search(r'\d+$', link) and not article_exists(link, existing_links):
            article_page = requests.get(link)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')
            title = article_soup.find('h1').text.strip() if article_soup.find('h1') else 'N/A'
            category_element = article_soup.find('span', {'class': 'sclt-storySectionLink'})
            category = category_element.text.strip() if category_element else 'N/A'
            summary_element = article_soup.find('div', {'class': 'detailSummary'})
            summary = summary_element.text.strip() if summary_element else 'N/A'

            image_element = article_soup.find('figure', {'class': 'imageMedia leadmedia-story full'})
            image_placeholder = image_element.find('div', {'class': 'placeholder'}) if image_element else None
            image = image_placeholder.find('img') if image_placeholder else None
            image_link = image['src'] if image and image.has_attr('src') else 'N/A'

            if not (category == 'News' and image_link == 'N/A'):
                new_articles.append([title, category, summary, image_link, link])

# Check if we have new articles to add
if new_articles:
    # Get the headers
    headers = sheet.row_values(1)

    # Get all existing data except the headers
    existing_data = sheet.get_all_values()[1:]

    # Prepend new articles to the existing data (excluding headers)
    combined_data = new_articles + existing_data

    # Clear the sheet and update with combined data, starting from the headers
    sheet.clear()
    sheet.update(range_name='A1', values=[headers] + combined_data)  # Use named arguments

    print("New articles have been prepended to the Google Sheet, headers are untouched.")
else:
    print("No new articles to add.")
