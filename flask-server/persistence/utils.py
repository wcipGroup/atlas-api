from persistence.mongoClient import Mongo

def saveRating(data):
    try:
        db = Mongo.get_db()
        return db["ratings"].insert_one(data).acknowledged
    except Exception as e:
        print("log e")
        return False