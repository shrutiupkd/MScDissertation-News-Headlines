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
        for li in soup.find_all('li', class_='sc-knuQbY kMvGaA'):
            time_tag = li.find('p', class_='sc-dNsVcS fgLGED')
            headline_tag = li.find('a', class_='sc-ERObt kAsiND')
            if time_tag and headline_tag:
                time = time_tag.text.strip()
                headline = headline_tag.text.strip()
                headlines.append({"Time": time, "Headline": headline})
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
    base_url = 'https://www.standard.co.uk/archive/'   

    all_headlines = []

    dates = generate_dates(start_date, end_date)
    for date in dates:
        formatted_date = date.strftime('%Y-%m-%d')
        url = f"{base_url}{formatted_date}"
        print(f"Scraping {url}")
        headlines = scrape_headlines(url)
        for headline in headlines:
            headline['Date'] = formatted_date
        all_headlines.extend(headlines)

    df = pd.DataFrame(all_headlines)
    df.to_csv('evening_standard_headlines.csv', index=False)
    print(f"Headlines have been saved to evening_standard_headlines.csv")
