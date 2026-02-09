from pymongo import MongoClient

MONGO_URI = "mongodb+srv://fraudshield:shashi123@fraudshield01.ckxahmm.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["fraudshield_db"]

users = db["users"]
transactions = db["transactions"]
