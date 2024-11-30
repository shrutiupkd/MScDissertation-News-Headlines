import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def fetch_html(url):
    """Fetches HTML content from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching HTML: {e}")
        return None

def scrape_headlines(url):
    """Scrapes a website for news headlines."""
    html = fetch_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        headlines = []
        for li in soup.find_all('li'):
            link_tag = li.find('a')
            if link_tag:
                headline = link_tag.text.strip()
                if headline:
                    headlines.append({"Headline": headline})
        return headlines
    else:
        print("Failed to fetch HTML.")
        return []

def generate_dates(start_date, end_date):
    """Generates a list of dates between the start_date and end_date."""
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

if __name__ == "__main__":
    start_date = datetime(2020, 12, 1)
    end_date = datetime(2021, 6, 30)
    base_url = 'https://www.dailymail.co.uk/home/sitemaparchive/day_'

    all_headlines = []

    dates = generate_dates(start_date, end_date)
    for date in dates:
        formatted_date = date.strftime('%Y%m%d')
        url = f"{base_url}{formatted_date}.html"
        print(f"Scraping {url}")
        headlines = scrape_headlines(url)
        for headline in headlines:
            headline['Date'] = formatted_date
        all_headlines.extend(headlines)

    df = pd.DataFrame(all_headlines)
    df.to_csv('daily_mail_headlines.csv', index=False)
    print(f"Headlines have been saved to daily_mail_headlines.csv")
