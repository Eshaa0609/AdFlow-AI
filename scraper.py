import requests
from bs4 import BeautifulSoup
import time

def get_real_brands():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_India"
    
    try:
        print("Connecting to Wikipedia to fetch top Indian brands...")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'class': 'wikitable'})
        brands = []
        
        for row in table.find_all('tr')[1:21]:
            link = row.find('a')
            if link:
                brands.append(link.text.strip())
        
        # Adding your favorite Global brands + Indian household names
        must_have_brands = ["Walmart", "Amazon", "Zomato", "Jio", "Flipkart", "Tata Motors"]
        
        # Merge lists and remove duplicates
        final_brands = list(set(brands + must_have_brands))
        
        print(f"Success! Found {len(final_brands)} total brands.")
        return sorted(final_brands) # Alphabetical order looks cleaner

    except Exception as e:
        print(f"Scraping failed: {e}. Using combined fallback.")
        return ["Reliance Industries", "TCS", "Walmart", "Amazon", "Zomato", "HDFC Bank"]

if __name__ == "__main__":
    brands = get_real_brands()
    print("Preview of your data:", brands[:5])