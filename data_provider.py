# data_provider.py
import psycopg2
import os
from dotenv import load_dotenv
# We import your scraper function here
from scraper import get_real_brands_metrics 

load_dotenv()

# --- SQL Logic ---
def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set!")
    return psycopg2.connect(db_url)

def get_metrics_from_sql(region_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            COUNT(*) AS total_clicks,
            SUM(CASE WHEN is_bot = true THEN 1 ELSE 0 END) AS bot_clicks,
            ROUND(((SUM(CASE WHEN is_bot = true THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0)) * 100)::numeric, 2) AS bot_percentage
        FROM click_logs
        WHERE user_region ILIKE %s 
        AND timestamp > NOW() - INTERVAL '5 minutes';
        """
        cursor.execute(query, (f"%{region_name}%",))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result and result[0] is not None and result[0] > 0:
            return {
                "region": region_name, 
                "total_clicks": result[0], 
                "bot_count": result[1], 
                "bot_rate": f"{result[2]}%"
            }
        return None
    except Exception as e:
        print(f"SQL Error: {e}")
        return None

# --- Web Scraper Logic ---
def get_metrics_from_web(region_name):
    """Wraps your existing scraper logic into the Data Provider format"""
    # This calls the function in your scraper.py
    return get_real_brands_metrics(region_name)

# --- THE INTERFACE (The Strategy Pattern) ---
def get_campaign_metrics(region, source_type="sql"):
    """The central hub: Agent doesn't care where data comes from!"""
    if source_type == "sql":
        return get_metrics_from_sql(region)
    elif source_type == "web":
        return get_metrics_from_web(region)
    else:
        raise ValueError(f"Unknown source_type: {source_type}")

# --- HELPER FOR UI ---
def get_raw_bot_rate(region_name, source_type="sql"):
    stats = get_campaign_metrics(region_name, source_type)
    if isinstance(stats, dict):
        return float(stats['bot_rate'].replace('%', ''))
    return 0.0