import requests
import pandas as pd
import json

# 1. URL API (token kamu dimasukkan ke URL)
url = "https://api.waqi.info/feed/jakarta/?token=58ec7efe5d7fb9144a8d3f257e377b673140c695"

# 2. Request data dari API
response = requests.get(url)
data = response.json()

# 3. Cek status
if data.get("status") != "ok":
    print("Gagal mengambil data:", data)
    exit()

# 4. Ambil bagian 'data' dari JSON
data = data["data"]

# ============================
# 5. DATA TERBARU (satu baris)
# ============================
latest = {
    "city": data["city"]["name"],
    "aqi": data["aqi"],
    "dominant_pollutant": data["dominentpol"],
    "time": data["time"]["s"]
}
df_summary = pd.DataFrame([latest])
df_summary.to_csv("data/aqi/aqi_latest_data.csv", index=False)

# ===================================
# 6. DATA FORECAST (PM10 dan PM25)
# ===================================
forecast = data["forecast"]["daily"]

# PM10
df_pm10 = pd.DataFrame(forecast["pm10"])
df_pm10.to_csv("data/aqi/forecast_pm10.csv", index=False)

# PM25
df_pm25 = pd.DataFrame(forecast["pm25"])
df_pm25.to_csv("data/aqi/forecast_pm25.csv", index=False)

# # UVI (jika ingin digunakan)
df_uvi = pd.DataFrame(forecast.get("uvi", []))  # pakai get utk menghindari error
df_uvi.to_csv("data/aqi/forecast_uvi.csv", index=False)

print("Semua file CSV berhasil dibuat:")
print("- aqi_summary.csv")
print("- forecast_pm10.csv")
print("- forecast_pm25.csv")
print("- forecast_uvi.csv")