import psycopg2
import csv
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def migrate_csv_to_db():
    # 1. Connection Details - Pulled safely from environment variables
    conn_params = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }

    conn = None # Initialize to avoid errors in 'finally' block

    try:
        # 2. Connect to the "Vault"
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # 3. Open the CSV file
        with open('ad_clicks_dataset.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            
            print("Uploading data to the 'click_logs' table...")
            for row in reader:
                cursor.execute(
                    "INSERT INTO click_logs (ad_id, campaign_name, source_url, user_region, device_type, click_duration_ms, is_bot) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    row
                )
        
        # 4. Save (Commit) the changes
        conn.commit()
        print("Success! Data has been moved to the vault securely.")

    except Exception as e:
        print(f"Error during ingestion: {e}")
    
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    migrate_csv_to_db()