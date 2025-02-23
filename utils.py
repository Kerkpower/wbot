import random

from datetime import datetime

import pymongo

import os
from dotenv import load_dotenv

load_dotenv()

mongo_user = os.getenv("MONG_USER")
mongo_pass = os.getenv("MONG_PASSWORD")
mongo_cluster = os.getenv("MONG_HOSTNAME")

client = pymongo.MongoClient(
    f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_cluster}/?retryWrites=true&w=majority&appName=Cluster0"
)


db = client["db"]
col = db["users"]
global_var = db["global"]


class MongoDB:
    @staticmethod
    def get_user(uid: int):
        """Get a user from the database or create a new one if not found"""
        default_user = {
            "_id": uid,
            "cash": 10000,
            "bank": 0,
            "bank_max": 10_000,
            "prof_coin": 0,
            "prof_slots": 0,
            "prof_roul": 0,
            "prof_stock": 0,
            "prof_bj": 0,
            "stocks": 0,
            "daily_streak": 0,
            "daily_last": datetime.now(),
            "inv": {}
        }
        return col.find_one_and_update(
            {"_id": uid},
            {"$setOnInsert": default_user},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER
        )

    @staticmethod
    def update_user(uid: int, updated):
        """Update user in database"""
        col.update_one({"_id": uid}, {"$set": updated})

    @staticmethod
    def update_all(field, value):
        """Update a field for all users in the database"""
        col.update_many({}, {"$set": {field: value}})

    @staticmethod
    def get_global():
        """Get global variables from database or create if not found"""
        default_global = {
            "_id": 69420,
            "stock_price": 100,
            "stock_price_change": 5,
            "Stock_circulating": 0,
        }
        return global_var.find_one_and_update(
            {"_id": 69420},
            {"$setOnInsert": default_global},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER
        )

    @staticmethod
    def update_global(updated):
        """Update global variables in database"""
        global_var.update_one({"_id": 69420}, {"$set": updated})


class Others:
    @staticmethod
    def random_hex():
        """Generate a random hex 0 - FFFFFF"""
        return random.randint(0x0, 0xFFFFFF)
