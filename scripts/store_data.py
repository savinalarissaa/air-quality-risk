import pymongo
import pandas as pd
import time
from datetime import datetime
import analysis_preprocessing as prep

# KONEKSI MongoDB
client = pymongo.MongoClient("mongodb://iot_user:iot_password@localhost:27017/air_quality_db")
db = client.air_quality_db
weatherAPI_collection = db.data_weatherAPI
waqi_collection = db.data_waqi
risk_score_collection = db.data_risk_score
combined_collection = db.data_combined

CSV_FILE_API = "data/weather/weatherAPI_output.csv"
CSV_FILE_WAQI = "data/aqi/waqi_output.csv"
CSV_FILE_RISK_SCORE = "data/processed_data_risk-score.csv"
CSV_FILE_COMBINED = "data/processed_combined_data.csv"

# masukkin weatherAPI ke MongoDB
def insert_weatherAPI_data():
    try:
        df = pd.read_csv(CSV_FILE_API)

        for _, row in df.iterrows():
            doc = {
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

            weatherAPI_collection.insert_one(doc)
            print(f"✔ Inserted weather data for {row['Kecamatan']}")

    except Exception as e:
        print(f"ERROR reading CSV WeatherAPI: {e}")

# masukkin WAQI ke MongoDB
def insert_WAQI_data():
    try:
        df = pd.read_csv(CSV_FILE_WAQI)
        for _, row in df.iterrows():
            doc = {
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

            waqi_collection.insert_one(doc)
            print(f"✔ Inserted AQI data for {row['Kecamatan']}")

    except Exception as e:
        print(f"ERROR reading CSV WAQI: {e}")

# masukkin risk score ke MongoDB
def insert_risk_score_data():
    try:
        df = pd.read_csv(CSV_FILE_RISK_SCORE)
        for _, row in df.iterrows():
            doc = {
                'last_update': row['update_time'],
                'risk_score': row['risk_score'],
                'risk_category': row['risk_category'],
                'aqi': row['AQI'],
                'pm10': row['PM10'],
                'pm25': row['PM25'],
                'o3': row['O3'],
                'humidity_mean': row['Humidity'],
                'temperature_mean': row['Temperature'],
                'wind_mean': row['Wind Speed'],
                'uv_index': row['UV Index'],
                'timestamp_saved': datetime.utcnow()
            }

            risk_score_collection.insert_one(doc)
            print(f"✔ Inserted Risk Score")

    except Exception as e:
        print(f"ERROR reading CSV Risk Score: {e}")

def insert_combined_data():
    try:
        df = pd.read_csv(CSV_FILE_COMBINED)
        for _, row in df.iterrows():
            doc = {
                # Station ID,Kecamatan,Last Update,AQI,Dominant Pollutant,PM10,PM25,CO,NO2,SO2,O3,Lokasi,Temperature,Humidity,Condition,Wind Speed,Wind Direction,UV Index,risk_score,risk_category
                'kecamatan' : row['Kecamatan'],
                'last_update': row['Last Update'],
                'risk_score': row['risk_score'],
                'risk_category': row['risk_category'],
                'aqi': row['AQI'],
                'pm10': row['PM10'],
                'pm25': row['PM25'],
                'humidity_mean': row['Humidity']
            }

            combined_collection.insert_one(doc)
            print(f"✔ Inserted Combined data.")

    except Exception as e:
        print(f"ERROR reading CSV: {e}")

def main():
    print("STARTING CSV -> MongoDB weather stream...")
    try:
        while True:
            prep.main()
            insert_weatherAPI_data()
            insert_WAQI_data()
            insert_risk_score_data()
            insert_combined_data()
            print(f"🔄 CSV data inserted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(900)  # 15 menit sekali
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        client.close()

if __name__ == "__main__":
    main()