from src.utils.db import mongo_db
from datetime import datetime

class ActivityLog:
    """Helper class to interact with MongoDB logs collection"""
    
    collection_name = "activity_logs"

    @classmethod
    def get_collection(cls):
        if mongo_db is not None:
             return mongo_db[cls.collection_name]
        return None

    @classmethod
    def log_activity(cls, user_id, action, details=None):
        collection = cls.get_collection()
        if collection is not None:
            log_entry = {
                "user_id": user_id,
                "action": action,
                "details": details or {},
                "timestamp": datetime.utcnow()
            }
            collection.insert_one(log_entry)
            return True
        return False

    @classmethod
    def get_logs(cls, user_id=None, limit=50):
        collection = cls.get_collection()
        if collection is not None:
            query = {}
            if user_id:
                query["user_id"] = user_id
            
            cursor = collection.find(query).sort("timestamp", -1).limit(limit)
            logs = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                logs.append(doc)
            return logs
        return []

class MongoUser:
    """Helper class to interact with MongoDB users if they choose MongoDB as their DB."""
    
    collection_name = "users"

    @classmethod
    def get_collection(cls):
        if mongo_db is not None:
             return mongo_db[cls.collection_name]
        return None

    @classmethod
    def create_user(cls, username, email, password_hash):
        collection = cls.get_collection()
        if collection is not None:
            # Check if user exists
            if collection.find_one({"$or": [{"username": username}, {"email": email}]}):
                return None
            
            user_doc = {
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "created_at": datetime.utcnow()
            }
            result = collection.insert_one(user_doc)
            user_doc['_id'] = str(result.inserted_id)
            return user_doc
        return None

    @classmethod
    def get_user_by_username(cls, username):
        collection = cls.get_collection()
        if collection is not None:
            user = collection.find_one({"username": username})
            if user:
                 user['_id'] = str(user['_id'])
            return user
        return None
