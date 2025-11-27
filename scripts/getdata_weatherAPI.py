import requests
import pandas as pd

KEY = "71197a83e2524eb5941144537251911"
URL = "http://api.weatherapi.com/v1/forecast.json"

kec = [
        "Cakung", "Cempaka Putih", "Cengkareng", "Cilandak", "Cilincing", "Cipayung", "Ciracas",
        "Duren Sawit",
        "Gambir", "Grogol Petamburan",
        "Jagakarsa", "Jatinegara", "Johar Baru",
        "Kalideres","Kebayoran Baru","Kebayoran Lama","Kebon Jeruk","Kelapa Gading","Kemayoran",
        "Kembangan","Kepulauan Seribu Selatan","Kepulauan Seribu Utara","Koja","Kramat Jati",
        "Makasar","Mampang Prapatan","Matraman","Menteng",
        "Pademangan","Palmerah","Pancoran","Pasar Minggu","Pasar Rebo","Penjaringan","Pesanggrahan","Pulo Gadung",
        "Sawah Besar","Senen","Setiabudi",
        "Taman Sari","Tambora","Tanah Abang","Tanjung Priok","Tebet"]

results = []  # list untuk menampung hasil

for kc in kec:
    params = {"key": KEY, "q": f"{kc}, Jakarta", "aqi": "no"}
    resp = requests.get(URL, params=params, timeout=10)
    data = resp.json().get("current", None)

    # kalau data berhasil ditemukan
    if data:
        results.append({
            "Kecamatan": kc,
            "Last Update": data.get("last_updated", "null"),
            "Temperature": data.get("temp_c", "null"),
            "Humidity": data.get("humidity", "null"),
            "Condition": data.get("condition", {}).get("text", "null"),
            "Wind Speed": data.get("wind_kph", "null"),
            "Wind Direction": data.get("wind_dir", "null"),
            "UV Index": data.get("uv", "null")
        })
    else: # kalau nggak dikasih "null"
        results.append({
            "Kecamatan": kc,
            "Last Update": "null",
            "Temperature": "null",
            "Humidity": "null",
            "Condition": "null",
            "Wind Speed": "null",
            "Wind Direction": "null",
            "UV Index": "null"
        })

# buat DataFrame
df = pd.DataFrame(results)

# simpan ke CSV
OUTPUT_CSV = "data/weather/DKIJakarta_weather_output.csv"
df.to_csv(OUTPUT_CSV, index=False)

print(f"CSV berhasil dibuat di: {OUTPUT_CSV}")
# print(df)