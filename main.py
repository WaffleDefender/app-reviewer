from google_play_scraper import app, reviews, Sort
from google_play_scraper.exceptions import NotFoundError
from pprint import pprint 
import pandas as pd

def scrape_reviews(app_id, country):
    try:
        app_details = app(
            app_id,
            lang='en',
            country=country
        )
        print (f"Amount of reviews for {app_id} in {country.upper()} store: {app_details['reviews']}")

        result, continuation_token  = reviews(
            app_id,
            lang='en',
            country=country,
            sort=Sort.NEWEST,
        )
        print(result)

        result, _ = reviews(
            app_id,
            continuation_token=continuation_token,
        )
        print(result)
        
        return result
    except NotFoundError:
        print(f"App with id {app_id} not found in the {country.upper()} store.")
        return pd.DataFrame()
    
def convert_to_df(reviews):
    pprint(reviews)
    reviews_df = pd.DataFrame(reviews)
    return reviews_df

apps_to_scrape = {
    'com.higherone.mobile.android': ['au'],
    # 'com.facebook.katana': ['us', 'gb', 'au']
}

# Scraping reviews
for app_id, countries in apps_to_scrape.items():
    for country in countries:
        print(f"Scraping {app_id} from {country.upper()} store...")
        reviews = scrape_reviews(app_id, country)
        reviews_df = convert_to_df(reviews)

        print(reviews_df)
        
        # Save the DataFrame as a CSV file
        if not reviews_df.empty:
            reviews_df.to_csv(f"{app_id}_{country}.csv", index=False)
            print(f"Saved {len(reviews_df)} reviews to {app_id}_{country}.csv")
        else:
            print(f"No reviews found for {app_id} in {country.upper()} store.")