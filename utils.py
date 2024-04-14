import pymongo
import random

import logging

from dotenv import dotenv_values

env_vars = dotenv_values(".env")
mongo_user = env_vars.get("MONG_USER")
mongo_pass = env_vars.get("MONG_PASSWORD")

client = pymongo.MongoClient(
    f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.naffa8p.mongodb.net/"
)
db = client["db"]
col = db["users"]


class MongoDB:
    @staticmethod
    def get_user(uid):
        """get a user from the database"""
        if col.find_one({"_id": uid}):
            return col.find_one({"_id": uid})
        else:
            col.insert_one({
                "_id": uid, "cash": 0, "bank": 0, "bank_max": 10_000,
                "profit": {
                    "prof_coin": 0, "prof_slots": 0, "prof_roul": 0
                },
                "inv": {

                }
            })
            return col.find_one({"_id": uid})

    @staticmethod
    def update_user(uid, updated):
        """update user in database"""
        user = MongoDB.get_user(uid)
        col.update_one(user, {"$set": updated})


class Others:
    @staticmethod
    def random_hex():
        """random hex 0 - FFFFFF"""
        return random.randint(0x0, 0xFFFFFF)

