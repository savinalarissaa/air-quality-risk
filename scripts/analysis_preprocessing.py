from datetime import date, datetime
import pandas as pd

# 1. Load CSV
waqi = pd.read_csv("data/aqi/waqi_output.csv")
weather = pd.read_csv("data/weather/weatherAPI_output.csv")

# 2. Konversi ke numerik
num_cols_waqi = ['PM10', 'PM25', 'AQI', 'O3']
num_cols_weather = ['Temperature', 'Humidity', 'Wind Speed', 'UV Index']

waqi[num_cols_waqi] = waqi[num_cols_waqi].apply(pd.to_numeric, errors='coerce')
weather[num_cols_weather] = weather[num_cols_weather].apply(pd.to_numeric, errors='coerce')

waqi_means = waqi[num_cols_waqi].mean()
weather_means = weather[num_cols_weather].mean()

# 4. Gabungkan semua data dalam satu baris
data = {
    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "pm25_avg": [float(waqi_means["PM25"])],
    "pm10_avg": [float(waqi_means["PM10"])],
    "o3_avg": [float(waqi_means["O3"])],
    "aqi_avg": [float(waqi_means["AQI"])],
    "temp_mean": [float(weather_means["Temperature"])],
    "humidity_mean": [float(weather_means["Humidity"])],
    "wind_mean": [float(weather_means["Wind Speed"])],
    "uv_index": [float(weather_means["UV Index"])]
}

df = pd.DataFrame(data)
    
# 5. Hitung Risk Score
df["risk_score"] = (
    0.6 * df["pm25_avg"] +
    0.3 * df["pm10_avg"] +
    0.1 * df["humidity_mean"]
)

# 6. Kategorikan risiko
def categorize(x):
    if x < 50:
        return "Rendah"
    elif x < 100:
        return "Sedang"
    else:
        return "Tinggi"

df["risk_category"] = df["risk_score"].apply(categorize)

# 7. Print hasil
print("DATASET PREPOCESSING RISK SCORE SELESAI ✅")
print(df)
    
# 8. Simpan ke CSV
output_csv = "data/processed_data_risk-score.csv"
df.to_csv(output_csv, index=False)
print(f"\nFile disimpan sebagai: {output_csv}")