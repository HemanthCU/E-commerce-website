from email.policy import default
import pymongo

client = pymongo.MongoClient("mongodb://34.90.45.172:27017,35.204.166.243:27017,34.90.178.17:27017")
db = client["productDB"]
print(db)