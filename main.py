from google_play_scraper import app
from google_play_scraper.exceptions import NotFoundError
import pandas as pd

def scrape_reviews(app_id, country):
    try:
        app_details = app(
            app_id,
            lang='en',
            country=country
        )
        print (f"Amount of reviews for {app_id} in {country.upper()} store: {app_details['reviews']}")
        
    except NotFoundError:
        print(f"App with id {app_id} not found in the {country.upper()} store.")
        return pd.DataFrame()

apps_to_scrape = {
    'com.whatsapp': ['us', 'in', 'jp'],
    'com.facebook.katana': ['us', 'gb', 'au']
}

# Scraping reviews
for app_id, countries in apps_to_scrape.items():
    for country in countries:
        print(f"Scraping {app_id} from {country.upper()} store...")
        reviews_df = scrape_reviews(app_id, country)
        