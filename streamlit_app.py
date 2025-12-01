# streamlit_app.py : FILE IMPLEMENTASI STREAMLIT DASHBOARD 
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

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        FILENAME_combined = Path(__file__).parent / 'data/processed_combined_data.csv'
        FILENAME_risk = Path(__file__).parent / 'data/export_mongoDB_risk_data.csv'
        df_combined = pd.read_csv(FILENAME_combined)
        df_risk = pd.read_csv(FILENAME_risk)
        df_combined['Last Update'] = pd.to_datetime(df_combined['Last Update'], errors='coerce')
        df_risk['last_update'] = pd.to_datetime(df_risk['last_update'], errors='coerce')
        return df_combined, df_risk
    except Exception as e:
        st.error(f"Gagal membaca CSV: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_combined, df_risk = load_data()

if df_combined.empty:
    st.stop()  # Hentikan app jika data kosong

# --- KONVERSI DATETIME ---
if "Last Update" in df_combined.columns:
    df_combined["Last Update"] = pd.to_datetime(df_combined["Last Update"])
if "last_update" in df_risk.columns:
    df_risk["last_update"] = pd.to_datetime(df_risk["last_update"])

# st.subheader("testing") # untuk testing
# st.write(df_risk['last_update'].head(20))

# --- FILTER BERDASAR TANGGAL (untuk risk score) ---
st.subheader("🔍 Filter Data Risk Score Berdasarkan Tanggal")

if "last_update" in df_risk.columns:
    min_date = df_risk["last_update"].min().date()
    max_date = df_risk["last_update"].max().date()

    start_date, end_date = st.date_input(
        "Pilih rentang waktu:",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    df_risk_filtered = df_risk[
        (df_risk["last_update"].dt.date >= start_date) &
        (df_risk["last_update"].dt.date <= end_date)
    ]
else:
    df_risk_filtered = df_risk

# --- TAMPILKAN GRAFIK ---
st.subheader("📉 Grafik Risk Score Per Jam")
if "risk_score" in df_risk.columns:
    st.line_chart(df_risk_filtered.set_index("last_update")["risk_score"])
else:
    st.warning("Kolom `risk_score` tidak ditemukan.")

# --- FILTER BERDASAR TANGGAL (untuk data per kecamatan) ---
st.subheader("📉 Grafik Risk Score Per Kecamatan")
if "Last Update" in df_combined.columns:
    min_combined = df_combined["Last Update"].min().date()
    max_combined = df_combined["Last Update"].max().date()

    start_combined, end_combined = st.date_input(
        "Pilih rentang tanggal untuk data kecamatan:",
        (min_combined, max_combined),
        min_value=min_combined,
        max_value=max_combined,
        key="combined_filter"
    )

    df_combined_filtered = df_combined[
        (df_combined["Last Update"].dt.date >= start_combined) &
        (df_combined["Last Update"].dt.date <= end_combined)
    ]
else:
    df_combined_filtered = df_combined

# --- TAMPILKAN GRAFIK RISK SCORE PER KECAMATAN ---
st.write(
    f"Kecamatan risiko tertinggi: {df_combined_filtered.loc[df_combined_filtered['risk_score'].idxmax()]['Kecamatan']}"
)
st.bar_chart(df_combined_filtered.set_index("Kecamatan")["risk_score"])

# --- TAMPILAN SEMUA DATA TERBARU ---
st.subheader("📄 Tampilan Semua Data Terbaru")
st.dataframe(df_combined)

# --- DOWNLOAD DATA ---
st.subheader("⬇️ Unduh Data")
csv = df_combined_filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV Filtered",
    data=csv,
    file_name="filtered_risk_score.csv",
    mime="text/csv",
)