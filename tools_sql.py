import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_bot_stats_by_region(region_name):
    """
    Connects to the SQL database and calculates the percentage of bot traffic 
    for a specific region. This is the 'Watchdog' tool.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    
    # SQL query to calculate bot percentage
    # We add '::numeric' to the division result so ROUND can process it
    # UPDATE THIS QUERY
    query = """
    SELECT 
        COUNT(*) AS total_clicks,
        SUM(CASE WHEN is_bot = true THEN 1 ELSE 0 END) AS bot_clicks,
        ROUND(((SUM(CASE WHEN is_bot = true THEN 1 ELSE 0 END)::float / COUNT(*)) * 100)::numeric, 2) AS bot_percentage
    FROM click_logs
    WHERE user_region ILIKE %s 
    AND timestamp > NOW() - INTERVAL '5 minutes'; -- This makes it truly real-time
    """
    
    cursor.execute(query, (f"%{region_name}%",))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result and result[0] > 0:
        return {
            "region": region_name,
            "total_clicks": result[0],
            "bot_count": result[1],
            "bot_rate": f"{result[2]}%"
        }
    return f"No data found for region: {region_name}"

def get_raw_bot_rate(region_name):
    """Returns just the float value of the bot rate for UI components."""
    stats = get_bot_stats_by_region(region_name)
    if isinstance(stats, dict):
        return float(stats['bot_rate'].replace('%', ''))
    return 0.0

# Quick Test
if __name__ == "__main__":
    print(get_bot_stats_by_region("Mumbai"))