import time
import json
from kafka import KafkaProducer
from getdata_weatherAPI import ambil_data_weather # ini dijadikan main bisa??
from getdata_waqi import ambil_data_waqi

# Kafka config
BOOTSTRAP_SERVERS = "kafka:29092"
TOPIC_WEATHER = "weather-data"
TOPIC_WAQI = "waqi-data"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    # --- GET DATA WEATHER API ---
    try:
        weather_data = ambil_data_weather()
        producer.send(TOPIC_WEATHER, weather_data)
        print("Weather API sent to Kafka:", weather_data)
    except Exception as e:
        print(f"Weather API error: {e}")

    # --- GET DATA WAQI API ---
    try:
        waqi_data = ambil_data_waqi()
        producer.send(TOPIC_WAQI, waqi_data)
        print("WAQI API sent to Kafka:", waqi_data)
    except Exception as e:
        print(f"WAQI API error: {e}")

    time.sleep(10)  # delay 10 detik
