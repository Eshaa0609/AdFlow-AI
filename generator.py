import csv
import random
from datetime import datetime, timedelta
from scraper import get_real_brands

def generate_ad_data(num_rows=10000):
    # Step 1: Get the real brands from your scraper!
    brand_list = get_real_brands()
    
    devices = ["Mobile-Android", "Mobile-iOS", "Desktop-Windows", "Desktop-MacOS"]
    regions = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata"]
    
    filename = "ad_clicks_dataset.csv"
    
    print(f"Generating {num_rows} logs for brands: {brand_list[:5]}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header matching our PostgreSQL table
        writer.writerow(["ad_id", "campaign_name", "source_url", "user_region", "device_type", "click_duration_ms", "is_bot"])
        
        for i in range(num_rows):
            brand = random.choice(brand_list)
            ad_id = f"AD-{random.randint(1000, 9999)}"
            # Simulating a URL based on the brand
            url = f"https://www.{brand.lower().replace(' ', '')}.com/ads/promo"
            
            writer.writerow([
                ad_id,
                f"{brand} Summer Sale 2026", # Campaign Name
                url,
                random.choice(regions),
                random.choice(devices),
                random.randint(100, 5000), # Duration in ms
                random.choice([True, False, False, False, False]) # 20% chance it's a bot
            ])
            
    print(f"Done! Created {filename} with {num_rows} rows.")

if __name__ == "__main__":
    generate_ad_data()