import requests
import pandas as pd

# 1. URL API (token kamu dimasukkan ke URL)
KEY = "ba157ed0ab654607b79144746253011"
URL = "http://api.weatherapi.com/v1/forecast.json"

# 2. Data kecamatan yang mau diambil
kec = [
        "serpong", "cilegon", "bandung", "tunggulrejo", "manahan", "surabaya", "depok", 
        "serang", "purwakarta", "ngaliyan", "plumbungan", "kediri", "cisarua", "cilegon", 
        "pelabuhanratu", "candirejo", "mojopanggung", "leuwiliang", "indramayu", "sidakaya", 
        "kedopok", "bogor", "rembang", "mojokerto", "bekasi", "madiun", "gbk", "jombang", 
        "tangerang", "lamongan", "jakarta-timur", "tuban", "bojonegoro"]

# 3. Mengambil data dari API untuk setiap kecamatan (main loop)
results = []  # list untuk menampung hasil

for kc in kec:
    params = {"key": KEY, "q": f"{kc}", "aqi": "no"} # parameter request 
    resp = requests.get(URL, params=params, timeout=10)
    data = resp.json().get("current", None)

    # kalau data berhasil ditemukan
    if data:
        results.append({
            "Lokasi": kc,
            "Kecamatan": resp.json().get("location", {}).get("name", "null"),
            "Last Update": data.get("last_updated", "null"),
            "Temperature": data.get("temp_c", "null"),
            "Humidity": data.get("humidity", "null"),
            "Condition": data.get("condition", {}).get("text", "null"),
            "Wind Speed": data.get("wind_kph", "null"),
            "Wind Direction": data.get("wind_dir", "null"),
            "UV Index": data.get("uv", "null")
        })
    else: # kalau nggak, dikasih "null"
        print(f"Gagal mengambil data untuk kecamatan: {kc}")
        results.append({
            "Lokasi": kc,
            "Kecamatan": "null",
            "Last Update": "null",
            "Temperature": "null",
            "Humidity": "null",
            "Condition": "null",
            "Wind Speed": "null",
            "Wind Direction": "null",
            "UV Index": "null"
        })

# 4. Buat DataFrame
df = pd.DataFrame(results)

# 5. Simpan ke CSV
OUTPUT_CSV = "data/weather/weatherAPI_output.csv"
df.to_csv(OUTPUT_CSV, index=False)
print(f"CSV berhasil dibuat di: {OUTPUT_CSV}")