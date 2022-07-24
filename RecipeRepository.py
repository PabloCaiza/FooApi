import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util

MONGO_DRIVER_CONNECTION = "mongodb+srv://admin:#@cluster0.khyn5lg.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(MONGO_DRIVER_CONNECTION)
db = cluster["foodapi"]
collection = db["recipes "]


def insertRecipe(recipe):
    collection.insert({"name": recipe['name']})


def getRecipes():
    return collection.find({})


def removeRecipe(id):
    collection.delete_one({"_id": ObjectId(id)})


def updateRecipe(id, recipe):
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": recipe['name']}})


def findRecipeById(id):
    return collection.find_one({"_id": ObjectId(id)})
