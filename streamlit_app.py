import streamlit as st
import pandas as pd
from pathlib import Path
import pymongo  # WAJIB

# --- CONFIG APLIKASI ---
st.set_page_config(
    page_title="Risk Score Dashboard",
    page_icon="🌫️",
    layout="wide",
)

# --- HEADER ---
st.title("🌫️ Air Quality & Risk Score Dashboard")
st.write("Data diambil dari MongoDB / CSV fallback.")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        uri = "mongodb+srv://savinalarissa_db_user:pass123@pid.bngfn1a.mongodb.net/?retryWrites=true&w=majority&appName=PID"
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)  # timeout cepat
        db = client["air_quality_db"]
        collection = db["processed_risk_data"]
        data = list(collection.find({}, {"_id": 0}))
        return pd.DataFrame(data)  # FIX
    except Exception as e:
        st.warning(f"MongoDB gagal: {e} — gunakan CSV lokal ⚠")
        try:
            df_csv = pd.read_csv("data/processed_data_risk-score.csv")
            df_csv["Last Update"] = pd.to_datetime(df_csv["Last Update"])
            return df_csv
        except:
            st.error("🚨 Gagal membaca MongoDB & CSV!")
            return pd.DataFrame()

df_combined = load_data()

if df_combined.empty:
    st.error("⚠ Tidak ada data ditemukan — hentikan aplikasi.")
    st.stop()

# --- KONVERSI DATETIME ---
if "Last Update" in df_combined.columns:
    df_combined["Last Update"] = pd.to_datetime(df_combined["Last Update"])

st.subheader("📄 Tampilan Data")
st.dataframe(df_combined)

# --- FILTER TANGGAL ---
st.subheader("🔍 Filter Berdasarkan Tanggal")

if "Last Update" in df_combined.columns:
    min_date = df_combined["Last Update"].min().date()
    max_date = df_combined["Last Update"].max().date()

    start_date, end_date = st.date_input(
        "Pilih tanggal:",
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

# --- GRAFIK PER TANGGAL ---
st.subheader("📈 Risk Score per Jam")
if "risk_score" in df_filtered.columns:
    st.line_chart(df_filtered.set_index("Last Update")["risk_score"])
else:
    st.warning("⚠ Kolom 'risk_score' tidak ditemukan!")

# --- GRAFIK PER KECAMATAN ---
st.subheader("📊 Risk Score per Kecamatan")
if "Kecamatan" in df_filtered.columns:
    st.bar_chart(df_filtered.set_index("Kecamatan")["risk_score"])

# --- DOWNLOAD DATA ---
st.subheader("⬇️ Download Data")
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_risk_score.csv", "text/csv")