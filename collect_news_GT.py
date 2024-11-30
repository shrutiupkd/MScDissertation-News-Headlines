import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def scrape_guardian_for_one_day(date):
    # Format the date to match the URL structure, e.g., "2020/dec/01"
    formatted_date = date.strftime('%Y/%b/%d').lower()
    url = f"https://www.theguardian.com/uk-news/{formatted_date}/all"
    
    # Set up a user-agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Make the request to the page
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # Find all articles on the page
        for article in soup.find_all('a', class_='u-faux-block-link__overlay js-headline-text'):
            article_title = article.get_text(strip=True)
            article_link = article['href']
            articles.append({
                'date': date.strftime('%Y-%m-%d'), 
                'title': article_title, 
                'link': article_link
            })
        
        return articles
    else:
        print(f"Failed to retrieve data for {formatted_date}, Status code: {response.status_code}")
        return []

def scrape_guardian_for_one_month(year, month):
    # Determine the start and end dates for the month
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    all_articles = []

    # Iterate over each day in the month
    current_date = start_date
    while current_date <= end_date:
        print(f"Scraping data for {current_date.strftime('%Y-%m-%d')}")
        daily_articles = scrape_guardian_for_one_day(current_date)
        all_articles.extend(daily_articles)
        current_date += timedelta(days=1)

    # Convert to DataFrame
    df = pd.DataFrame(all_articles)

    # Save to CSV
    csv_filename = f'guardian_articles_{year}_{month:02}.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")

# Example usage
scrape_guardian_for_one_month(2021, 6)  # Scrapes articles for December 2020
