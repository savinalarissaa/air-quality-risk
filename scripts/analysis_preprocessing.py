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

combine = pd.read_csv("data/processed_combined_data.csv")
num_cols_combine = ['PM10', 'PM25', 'AQI', 'O3', 'Temperature', 'Humidity', 'Wind Speed', 'UV Index', 'risk_score']
combine[num_cols_combine] = combine[num_cols_combine].apply(pd.to_numeric, errors='coerce')
combine_means = combine[num_cols_combine].mean()

def categorize(x): # fungsi kategorisasi risiko
    if x < 50:
        return "Rendah"
    elif x < 100:
        return "Sedang"
    else:
        return "Tinggi"

def calculate_risk_score(df):
    return (
        0.6 * df["PM25"] +
        0.3 * df["PM10"] +
        0.1 * df["Humidity"]
    )

def process_combine_data():
    combined_rows = []
    for i in range(len(waqi)):
        row = {**waqi.iloc[i].to_dict(), **weather.iloc[i].to_dict()}
        combined_rows.append(row)

    #Station ID,Kecamatan,Last Update,AQI,Dominant Pollutant,PM10,PM25,CO,NO2,SO2,O3,Lokasi,Temperature,Humidity,Condition,Wind Speed,Wind Direction,UV Index,risk_score,risk_category

    combined = pd.DataFrame(combined_rows)

    combined["risk_score"] = calculate_risk_score(combined)
    combined["risk_category"] = combined["risk_score"].apply(categorize)

    output_csv = "data/processed_combined_data.csv"
    combined.to_csv(output_csv, index=False)

    print("DATA BERHASIL DIKOMBINASI! File disimpan di:", output_csv)
    print(combined.head())

    return combined

def process_risk_score():
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
    } # janlup ganti di store_data

    df = pd.DataFrame(data)
        
    df["risk_score"] = calculate_risk_score(df)
    df["risk_category"] = df["risk_score"].apply(categorize) 

    print("DATASET PREPOCESSING RISK SCORE SELESAI ✅")
    print(df)
    
    # 8. Simpan ke CSV
    output_risk = "data/processed_data_risk-score.csv"
    df.to_csv(output_risk, index=False)
    print(f"\nFile disimpan sebagai: {output_risk}")

def main():
    process_combine_data()
    process_risk_score()    

if __name__ == "__main__":
    main()