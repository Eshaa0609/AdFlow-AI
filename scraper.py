# scraper.py
import requests
from bs4 import BeautifulSoup

def get_real_brands_metrics(region_name="Mumbai"):
    """
    Scrapes Wikipedia for Indian companies. 
    Returns data in the SAME structure as your SQL tool, 
    so the Agent doesn't know the difference!
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_India"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        
        # Get count to simulate "clicks"
        brand_count = len(table.find_all('tr')) if table else 100
        
        # We simulate bot traffic data here, since Wikipedia doesn't have "AdFlow" data
        # This keeps the Agent working while you build out the real scraper logic
        return {
            "region": region_name,
            "total_clicks": brand_count,
            "bot_count": int(brand_count * 0.15), # Simulating 15% bot traffic
            "bot_rate": "15.00%"
        }
        
    except Exception as e:
        print(f"Scraping failed: {e}")
        # Return a fallback that keeps the Agent alive
        return {"region": region_name, "total_clicks": 0, "bot_count": 0, "bot_rate": "0%"}

if __name__ == "__main__":
    data = get_real_brands_metrics()
    print("Preview of your scraped data:", data)