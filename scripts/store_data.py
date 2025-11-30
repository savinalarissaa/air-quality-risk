import pymongo
import pandas as pd
import time
from datetime import datetime

# KONEKSI MongoDB
client = pymongo.MongoClient("mongodb://iot_user:iot_password@localhost:27017/air_quality_db")
db = client.air_quality_db
weatherAPI_collection = db.data_weatherAPI
waqi_collection = db.data_waqi
risk_score_collection = db.data_risk_score


CSV_FILE_API = "data/weather/weatherAPI_output.csv"
CSV_FILE_WAQI = "data/aqi/waqi_output.csv"
CSV_FILE_RISK_SCORE = "data/processed_data_risk-score.csv"

# masukkin weatherAPI ke MongoDB
def insert_weatherAPI_data():
    try:
        df = pd.read_csv(CSV_FILE_API)

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

            weatherAPI_collection.insert_one(weather_doc)
            print(f"✔ Inserted weather data for {row['Kecamatan']}")

    except Exception as e:
        print(f"ERROR reading CSV: {e}")

# masukkin WAQI ke MongoDB
def insert_WAQI_data():
    try:
        df = pd.read_csv(CSV_FILE_WAQI)
        for _, row in df.iterrows():
            weather_doc = {
                'station_id': row['Station ID'],
                'kecamatan': row['Kecamatan'],
                'last_update': row['Last Update'],
                'AQI': row['AQI'],
                'Dominant_Pollutant': row['Dominant Pollutant'],
                'pm10': row['PM10'],
                'pm25': row['PM25'],
                'co': row['CO'],
                'no2': row['NO2'],
                'so2': row['SO2'],
                'o3': row['O3']
            }

            waqi_collection.insert_one(weather_doc)
            print(f"✔ Inserted AQI data for {row['Kecamatan']}")

    except Exception as e:
        print(f"ERROR reading CSV: {e}")

# masukkin risk score ke MongoDB
def insert_risk_score_data():
    try:
        df = pd.read_csv(CSV_FILE_RISK_SCORE)
        for _, row in df.iterrows():
            weather_doc = {
                'last_update': row['date'],
                'risk_score': row['risk_score'],
                'risk_category': row['risk_category'],
                'aqi': row['aqi_avg'],
                'pm10': row['pm10_avg'],
                'pm25': row['pm25_avg'],
                'o3': row['o3_avg'],
                'humidity_mean': row['humidity_mean'],
                'temperature_mean': row['temp_mean'],
                'wind_mean': row['wind_mean'],
                'uv_index': row['uv_index'],
                'timestamp_saved': datetime.utcnow()
            }

            risk_score_collection.insert_one(weather_doc)
            print(f"✔ Inserted Risk Score")

    except Exception as e:
        print(f"ERROR reading CSV: {e}")

def main():
    print("STARTING CSV -> MongoDB weather stream...")
    try:
        while True:
            insert_weatherAPI_data()
            insert_WAQI_data()
            insert_risk_score_data()
            print(f"🔄 CSV data inserted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(300)  # 5 menit sekali
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        client.close()

if __name__ == "__main__":
    main()