import pymongo
import pandas as pd

# --- KONEKSI MONGODB LOKAL ---
client = pymongo.MongoClient(
    "mongodb://iot_user:iot_password@localhost:27017/air_quality_db"
)

# Pilih database dan koleksi
db = client["air_quality_db"]
collection = db["data_risk_score"]

# --- AMBIL SEMUA DOKUMEN ---
data = list(collection.find())

if not data:
    print("Tidak ada data dalam koleksi.")
else:
    # Ubah menjadi DataFrame
    df = pd.DataFrame(data)

    # Hapus kolom _id jika ada
    # if "_id" in df.columns:
    #     df = df.drop(columns=["_id"])

    # --- SIMPAN KE CSV ---
    output_file = "data/export_mongoDB_risk_data.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"Data berhasil disimpan ke: {output_file}")

# Tutup koneksi
client.close()
