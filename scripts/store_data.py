import pymongo
import pandas as pd
import time
from datetime import datetime

# ==========================
# KONEKSI MongoDB
# ==========================
client = pymongo.MongoClient("mongodb://iot_user:iot_password@localhost:27017/iot_db")
db = client.iot_db
weather_collection = db.data_weatherAPI

CSV_FILE = "data/weather/DKIJakarta_weather_output.csv"

def insert_weather_data():
    """Baca CSV dan simpan satu per satu ke MongoDB"""
    try:
        df = pd.read_csv(CSV_FILE)

        for _, row in df.iterrows():
            weather_doc = {
                'kecamatan': row['Kecamatan'],
                'last_update': row['Last Update'],
                'temperature': row['Temperature'],
                'humidity': row['Humidity'],
                'condition': row['Condition'],
                'wind_speed': row['Wind Speed'],
                'wind_direction': row['Wind Direction'],
                'uv_index': row['UV Index'],
                'timestamp_saved': datetime.utcnow()
            }

            weather_collection.insert_one(weather_doc)
            print(f"✔ Inserted data for {row['Kecamatan']}")

    except Exception as e:
        print(f"ERROR reading CSV: {e}")

def main():
    print("STARTING CSV -> MongoDB weather stream...")
    try:
        while True:
            insert_weather_data()
            print(f"🔄 CSV data inserted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(30)  # 30 detik sekali
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        client.close()

if __name__ == "__main__":
    main()