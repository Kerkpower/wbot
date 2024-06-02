import random

import pymongo
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
mongo_user = env_vars.get("MONG_USER")
mongo_pass = env_vars.get("MONG_PASSWORD")

client = pymongo.MongoClient(
    f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.naffa8p.mongodb.net/"
)
db = client["db"]
col = db["users"]
global_var = db["global"]


class MongoDB:
    @staticmethod
    def get_user(uid: int):
        """get a user from the database"""
        var = col.find_one({"_id": uid})
        if var:
            return var
        else:
            col.insert_one({
                "_id": uid, "cash": 0, "bank": 0, "bank_max": 10_000,
                "prof_coin": 0, "prof_slots": 0, "prof_roul": 0,
                "prof_stock": 0, "stocks": 0,
                "inv": {
                }
            })
            return col.find_one({"_id": uid})

    @staticmethod
    def update_user(uid: int, updated):
        """update user in database"""
        user = MongoDB.get_user(uid)
        col.update_one(user, {"$set": updated})

    @staticmethod
    def get_global():
        """get global variables from database"""
        var = global_var.find_one({"_id": 69420})
        if var:
            return var
        else:
            global_var.insert_one({
                "_id": 69420,
                "stock_price": 100,
                "stock_price_change": 5,
                "Stock_circulating": 0,
            })
            return global_var.find_one({"_id": 69420})

    @staticmethod
    def update_global(updated):
        """update global variables in database"""
        global_var.update_one(MongoDB.get_global(), {"$set": updated})


class Others:
    @staticmethod
    def random_hex():
        """random hex 0 - FFFFFF"""
        return random.randint(0x0, 0xFFFFFF)
