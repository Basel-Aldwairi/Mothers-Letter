import pymongo
import os
from dotenv import load_dotenv
import certifi

load_dotenv()


def clear_database():
    uri = os.getenv("ATLASDB_URI")
    client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
    db = client[os.getenv("MONGO_DB", "mothers_day_db")]
    collection = db[os.getenv("MONGO_COLLECTION", "poems")]

    # The empty filter {} tells MongoDB to match every single document
    result = collection.delete_one({'name':'Elvira'})

    print(f"Success! Deleted {result.deleted_count} poems from the database.")


if __name__ == "__main__":
    confirm = input("Are you SURE you want to delete all entries? (y/n): ")
    if confirm.lower() == 'y':
        clear_database()