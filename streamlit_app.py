import streamlit as st
import pandas as pd
from pathlib import Path

# --- CONFIG APLIKASI ---
st.set_page_config(
    page_title="Risk Score Dashboard",
    page_icon="🌫️",
    layout="wide",
)

# --- HEADER APLIKASI ---
st.title("🌫️ Air Quality & Risk Score Dashboard")
# st.write("Data dibaca langsung dari GitHub (tanpa MongoDB).")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # uri = "mongodb+srv://savinalarissa_db_user:pass123@pid.bngfn1a.mongodb.net/?appName=PID"
        # client = pymongo.MongoClient(uri)
        # db = client["air_quality_db"]
        # collection = db["processed_risk_data"]
        # data = list(collection.find({}, {"_id": 0}))
        FILENAME_combined = Path(__file__).parent / 'data/processed_combined_data.csv'
        df_combined = pd.read_csv(FILENAME_combined)
        df_combined['Last Update'] = pd.to_datetime(df_combined['Last Update'], errors='coerce')
        return df_combined
    except Exception as e:
        st.error(f"Gagal membaca CSV: {e}")
        return pd.DataFrame()

df_combined = load_data()

if df_combined.empty:
    st.stop()  # Hentikan app jika data kosong

# --- KONVERSI DATETIME ---
if "Last Update" in df_combined.columns:
    df_combined["Last Update"] = pd.to_datetime(df_combined["Last Update"])

st.subheader("📄 Tampilan Data")
st.dataframe(df_combined)

# --- FILTER BERDASAR TANGGAL ---
st.subheader("🔍 Filter Data Berdasarkan Tanggal")

if "Last Update" in df_combined.columns:
    min_date = df_combined["Last Update"].min().date()
    max_date = df_combined["Last Update"].max().date()

    start_date, end_date = st.date_input(
        "Pilih rentang tanggal:",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    df_filtered = df_combined[
        (df_combined["Last Update"].dt.date >= start_date) &
        (df_combined["Last Update"].dt.date <= end_date)
    ]
else:
    df_filtered = df_combined

# --- TAMPILKAN GRAFIK ---
st.subheader("📉 Grafik Risk Score Per Jam")
if "risk_score" in df_combined.columns:
    st.line_chart(df_filtered.set_index("Last Update")["risk_score"])
else:
    st.warning("Kolom `risk_score` tidak ditemukan di CSV.")

st.subheader("📉 Grafik Risk Score Per Kecamatan")
st.write(f"Kecamatan dengan risiko tertinggi: {df_filtered.loc[df_filtered['risk_score'].idxmax()]['Kecamatan']} (Score: {df_filtered['risk_score'].max()})")
st.bar_chart(df_filtered.set_index("Kecamatan")["risk_score"])

# --- TAMPILKAN RINGKASAN ---
# st.subheader("📊 Statistik Singkat")
# st.write(df_filtered.describe())

# --- DOWNLOAD DATA ---
st.subheader("⬇️ Unduh Data")
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV Filtered",
    data=csv,
    file_name="filtered_risk_score.csv",
    mime="text/csv",
)