import pymongo
import certifi

uri = "mongodb+srv://savinalarissa_db_user:pass123@pid.bngfn1a.mongodb.net/?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(uri, tls=True, tlsCAFile=certifi.where())  # SSL FIX
    db = client["air_quality_db"]
    print(db.list_collection_names())
    print("Connected! 🎉")
except Exception as e:
    print("❌ Failed:", e)
