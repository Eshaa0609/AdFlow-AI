import psycopg2
import os
import random
import time
from datetime import datetime
from dotenv import load_dotenv

# Load credentials from your .env file
load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def setup_database():
    """Ensures the table exists before we start writing."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS click_logs (
            id SERIAL PRIMARY KEY,
            user_region VARCHAR(100),
            is_bot BOOLEAN,
            timestamp TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def simulate_traffic():
    print("🚀 Traffic Simulator Started. Writing to DB every 3 seconds...")
    setup_database()
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        while True:
            # Simulate real-world traffic patterns
            region = random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Pune'])
            is_bot = random.random() < 0.25  # 25% chance of being a bot
            
            cur.execute(
                "INSERT INTO click_logs (user_region, is_bot, timestamp) VALUES (%s, %s, %s)",
                (region, is_bot, datetime.now())
            )
            conn.commit()
            print(f"✅ Injected: {region} | Bot: {is_bot}")
            
            time.sleep(3) # Data flows every 3 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Simulator Stopped.")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    simulate_traffic()