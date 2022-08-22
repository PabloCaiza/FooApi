import objectService
from flask import Flask, jsonify, request, Response, make_response, flash, redirect
import json
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)

app.config[
    "MONGO_URI"
] = "mongodb+srv://OtterFox:1XTQqHNw9X7XvkXs@cluster0.uwltrza.mongodb.net/mineria"


@app.route('/predictIngredients', methods=['POST'])
def predictIngredientes():
    uploaded_file = request.files['file']
    print(uploaded_file)
    ingredients = objectService.detectIngredients(uploaded_file)
    print(ingredients)
    recipes = mongo.db.recipes.find()
    response = json_util.dumps(recipes)
    recipes = json.loads(response)
    possibleRecipes = []
    for r in recipes:
        hasAnyIngredient = False
        count = 0
        for i in ingredients:
            if i in r["ingredients"]:
                hasAnyIngredient = True
                count = count + 1
        if hasAnyIngredient:
            r["countedElements"] = count
            possibleRecipes.append(r)

    response = sorted(possibleRecipes, key=lambda d: d['countedElements'], reverse=True)
    response = response[:10]
    diccionario = {
        "status": 200,
        "data": response
    }
    return jsonify(diccionario)


mongo = PyMongo(app)

if __name__ == '__main__':
    app.run(debug=True)
    print(__name__)
