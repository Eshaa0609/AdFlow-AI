import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Connects to the database using the single DATABASE_URL connection string.
    This is the only way to connect to cloud databases like Neon.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set!")
    return psycopg2.connect(db_url)

def get_bot_stats_by_region(region_name):
    """
    Connects to the SQL database and calculates the percentage of bot traffic.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query to calculate bot percentage
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
        
        # Return structured data if results exist
        if result and result[0] is not None and result[0] > 0:
            return {
                "region": region_name,
                "total_clicks": result[0],
                "bot_count": result[1],
                "bot_rate": f"{result[2]}%"
            }
        return None # Return None if no data, which your UI handles
        
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_raw_bot_rate(region_name):
    """Returns just the float value of the bot rate for UI components."""
    stats = get_bot_stats_by_region(region_name)
    if isinstance(stats, dict):
        return float(stats['bot_rate'].replace('%', ''))
    return 0.0

# Quick Test
if __name__ == "__main__":
    print(get_bot_stats_by_region("Mumbai"))