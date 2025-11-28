import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# -------------------------------
# LOAD DATA (CACHE)
# -------------------------------
@st.cache_data
def load_weather_data():
    DATA_FILENAME = Path(__file__).parent / 'data/weather/DKIJakarta_weather_output.csv'
    df = pd.read_csv(DATA_FILENAME)
    df['Last Update'] = pd.to_datetime(df['Last Update'], errors='coerce')

    return filtered_df

df = load_weather_data()

# -------------------------------
# HEADER
# -------------------------------
st.title("🌦️ Real-Time Weather Dashboard")
st.write("Data berasal dari API Cuaca (WeatherAPI / WAQI).")

st.write("Jumlah data:", len(df))

# -------------------------------
# FILTERS
# -------------------------------
# Sidebar Filter
st.sidebar.header("Filter Data")

kecamatan_list = sorted(df['Kecamatan'].unique())
selected_kecamatan = st.sidebar.multiselect(
    "Pilih Kecamatan:",
    kecamatan_list,
    kecamatan_list[:3]  # default 3 pertama
)

# Filter tanggal
min_date = df['Last Update'].min().date()
max_date = df['Last Update'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu:",
    [min_date, max_date]
)

# Cek dulu sebelum filter
if not selected_kecamatan:
    st.warning("⚠ Silakan pilih minimal 1 kecamatan di sidebar.")
    st.stop()

# Filter dataframe
filtered_df = df[
    (df['Kecamatan'].isin(selected_kecamatan)) &
    (df['Last Update'].dt.date >= start_date) &
    (df['Last Update'].dt.date <= end_date)
]


# -------------------------------
# APPLY FILTER
# -------------------------------
filtered_df = df[
    (df['Kecamatan'].isin(selected_kecamatan)) &
    (df['Last Update'].dt.date >= pd.to_datetime(start_date)) &
    (df['Last Update'].dt.date <= pd.to_datetime(end_date))
]

st.subheader("📌 Data yang Ditampilkan")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# CHARTS
# -------------------------------
st.subheader("🌡️ Suhu (Temperature) per Kecamatan")
st.line_chart(filtered_df, x='Last Update', y='Temperature', color='Kecamatan')

st.subheader("💧 Kelembaban (Humidity) per Kecamatan")
st.line_chart(filtered_df, x='Last Update', y='Humidity', color='Kecamatan')

st.subheader("🌬️ Kecepatan Angin (Wind Speed)")
st.line_chart(filtered_df, x='Last Update', y='Wind Speed', color='Kecamatan')

# -------------------------------
# STATISTIK
# -------------------------------
st.subheader("📊 Rata-rata & Maksimum")
col1, col2, col3 = st.columns(3)

col1.metric("Suhu Rata-rata", f"{filtered_df['Temperature'].mean():.2f} °C")
col2.metric("Kelembaban Rata-rata", f"{filtered_df['Humidity'].mean():.2f} %")
col3.metric("UV Index Maksimum", f"{filtered_df['UV Index'].max():.2f}")

# -------------------------------
# KONDISI TERAKHIR PER KECAMATAN
# -------------------------------
st.subheader("🔎 Kondisi Cuaca Terakhir per Kecamatan")

last_data = filtered_df.sort_values("Last Update").groupby("Kecamatan").tail(1)

for i, row in last_data.iterrows():
    st.write(f"### 📍 {row['Kecamatan']}")
    st.write(f"🕒 Update: {row['Last Update']}")
    st.write(f"🌡️ Temperature: **{row['Temperature']} °C**")
    st.write(f"💧 Humidity: **{row['Humidity']} %**")
    st.write(f"🌬️ Wind Speed: **{row['Wind Speed']} km/h**")
    st.write(f"🌞 UV Index: **{row['UV Index']}**")
    st.write(f"🌤️ Condition: **{row['Condition']}**")
    st.write("---")