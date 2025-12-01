# KODE PRE-PROCESSING & ANALYSIS DATA (di-import ke stroe_data.py)
from datetime import date, datetime
import pandas as pd

# 1. Load CSV
waqi = pd.read_csv("data/aqi/waqi_output.csv")
weather = pd.read_csv("data/weather/weatherAPI_output.csv")
combine = pd.read_csv("data/processed_combined_data.csv")

# 2. Konversi ke numerik
num_cols_waqi = ['PM10', 'PM25', 'AQI', 'O3'] # atribut yang dipakai
num_cols_weather = ['Temperature', 'Humidity', 'Wind Speed', 'UV Index']
num_cols_combine = ['PM10', 'PM25', 'AQI', 'O3', 'Temperature', 'Humidity', 'Wind Speed', 'UV Index', 'risk_score']

waqi[num_cols_waqi] = waqi[num_cols_waqi].apply(pd.to_numeric, errors='coerce') # konversi ke numerik
weather[num_cols_weather] = weather[num_cols_weather].apply(pd.to_numeric, errors='coerce')
combine[num_cols_combine] = combine[num_cols_combine].apply(pd.to_numeric, errors='coerce')

waqi_means = waqi[num_cols_waqi].mean() # nilai rata-rata tiap kolom
weather_means = weather[num_cols_weather].mean()
combine_means = combine[num_cols_combine].mean()

# 3. Fungsi kategorisasi dan kalkulasi risiko
def categorize(x): # fungsi kategorisasi risiko
    if x < 50:
        return "Rendah"
    elif x < 100:
        return "Sedang"
    else:
        return "Tinggi"

def calculate_risk_score(df): # fungsi perhitungan risk score
    return (
        0.6 * df["PM25"] +
        0.3 * df["PM10"] +
        0.1 * df["Humidity"]
    )

# 4. FUNGSI FUNFSI PRE-PROCESSING & ANALYSIS (hasil disimpan ke file .csv)
def process_combine_data(): # fungsi gabung data WAQI & WeatherAPI
    combined_rows = []
    for i in range(len(waqi)):
        row = {**waqi.iloc[i].to_dict(), **weather.iloc[i].to_dict()}
        combined_rows.append(row)

    combined = pd.DataFrame(combined_rows)

    combined["risk_score"] = calculate_risk_score(combined)
    combined["risk_category"] = combined["risk_score"].apply(categorize)

    output_csv = "data/processed_combined_data.csv"
    combined.to_csv(output_csv, index=False)
    print("File kombinasi data disimpan di:", output_csv)
    print(combined.head())

    return combined

def process_risk_score(): # fungsi proses risk score dari data gabungan
    data = {
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "PM25": [float(combine_means["PM25"])],
        "PM10": [float(combine_means["PM10"])],
        "O3": [float(combine_means["O3"])],
        "AQI": [float(combine_means["AQI"])],
        "Temperature": [float(combine_means["Temperature"])],
        "Humidity": [float(combine_means["Humidity"])],
        "Wind Speed": [float(combine_means["Wind Speed"])],
        "UV Index": [float(combine_means["UV Index"])]
    }

    df = pd.DataFrame(data)
        
    df["risk_score"] = calculate_risk_score(df)
    df["risk_category"] = df["risk_score"].apply(categorize) 
    
    output_risk = "data/processed_data_risk-score.csv"
    df.to_csv(output_risk, index=False)
    print(f"\nFile risk score disimpan sebagai: {output_risk}")

def main():
    process_combine_data()
    process_risk_score()    

if __name__ == "__main__":
    main()