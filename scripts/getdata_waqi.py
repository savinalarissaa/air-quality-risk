import requests
import pandas as pd
import json

# 1. URL API (token kamu dimasukkan ke URL)
key = "58ec7efe5d7fb9144a8d3f257e377b673140c695"
url = f"https://api.waqi.info/feed/"

station = [ "416785", "472489", "416860", "472675", "416908", "420154", "416857", "416821", "531553", 
           "506572", "519043", "519187", "544657", "472489", "519145", "472450", "519112", "472486", 
           "472492", "472585", "532009", "416833", "519124", "519280", "416815", "519016", "416842", 
           "516745", "472477", "519010", "531565", "519007", "519019"
        ]

results = []  # list untuk menampung hasil

# url = f"https://api.waqi.info/feed/jakarta/?token={key}"

# main loop untuk setiap stasiun
for kc in station:
    url = f"https://api.waqi.info/feed/A{kc}/?token={key}"
    
    # 2. Request data dari API
    response = requests.get(url)
    data = response.json()
    # results.append(data)

    # 3. Cek status
    if data.get("status") != "ok":
        print("Gagal mengambil data:", data)
        exit()
    
    if data:
        results.append({
            "Station ID": kc,
            "Kecamatan": data.get("data", {}).get("city", {}).get("name", "null"),
            "Last Update": data.get("data", {}).get("time", {}).get("s", "null"),
            "AQI": data.get("data", {}).get("aqi", "null"),
            "Dominant Pollutant": data.get("data", {}).get("dominentpol", "null"),
            "PM10": data.get("data", {}).get("iaqi", {}).get("pm10", {}).get("v", "null"),
            "PM25": data.get("data", {}).get("iaqi", {}).get("pm25", {}).get("v", "null"),
            "CO": data.get("data", {}).get("iaqi", {}).get("co", {}).get("v", "null"),
            "NO2": data.get("data", {}).get("iaqi", {}).get("no2", {}).get("v", "null"),
            "SO2": data.get("data", {}).get("iaqi", {}).get("so2", {}).get("v", "null"),
            "O3": data.get("data", {}).get("iaqi", {}).get("o3", {}).get("v", "null")
        })
    else: # kalau nggak, dikasih "null"
        print(f"Gagal mengambil data untuk kecamatan: {kc}")
        results.append({
            "Station ID": kc,
            "Kecamatan": "null",
            "Last Update": "null",
            "Dominant Pollutant": "null",
            "AQI": "null",
            "PM10": "null",
            "PM25": "null",
            "CO": "null",
            "NO2": "null",
            "SO2": "null",
            "O3": "null"
        })

# 4. simpan ke csv
df = pd.DataFrame(results)
output_csv = "data/aqi/waqi_output.csv"
df.to_csv(output_csv, index=False)
print(f"CSV berhasil dibuat di: {output_csv}")