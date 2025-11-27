from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Kafka consumer
consumer = KafkaConsumer(
    'weather-data',
    bootstrap_servers='kafka:29092',
    group_id='weather-group',
    auto_offset_reset='earliest'
)

# MongoDB
client = MongoClient("mongodb://iot_user:iot_password@mongodb:27017/")
db = client["iot_db"]
collection = db["data_weatherAPI"]

print("Listening... and storing to MongoDB!")

for msg in consumer:
    try:
        data = json.loads(msg.value.decode('utf-8'))
        collection.insert_one(data)
        print("✔ Inserted to MongoDB")
    except:
        print("❌ Invalid JSON format")
