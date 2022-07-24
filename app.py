from flask import Flask, jsonify, request, abort
import objectService
import IngredientsClient
import RecipeRepository

app = Flask(__name__)


@app.route('/recipes', methods=['GET'])
def getRecipes():
    recipes = RecipeRepository.getRecipes()
    new_recipes = []
    for recipe in recipes:
        recipe.update()
        recipe['_id'] = str(recipe['_id'])
        new_recipes.append(recipe)
    return jsonify(new_recipes)


@app.route('/recipes/<string:id>', methods=['GET'])
def getRecipeById(id):
    # products_found = [product for product in products if product['name'] == name]
    product_found = RecipeRepository.findRecipeById(id)
    if product_found:
        product_found['_id'] = str(product_found['_id'])
        return jsonify(product_found)
    abort(404)


@app.route('/recipes', methods=['POST'])
def addRecipe():
    RecipeRepository.insertRecipe(request.json)
    return 'received'


@app.route('/recipes/<string:id>', methods=['DELETE'])
def deleteRecipe(id):
    products_found = RecipeRepository.findRecipeById(id)
    if products_found:
        RecipeRepository.removeRecipe(id)
        return jsonify("deleted successfully")
    abort(404)


@app.route('/recipes/<string:id>', methods=['PUT'])
def editRecipe(id):
    product_found = RecipeRepository.findRecipeById(id)
    if product_found:
        RecipeRepository.updateRecipe(id, request.json)
        return jsonify({"message": "Updated Successfully"})

    abort(404)


@app.route('/predictIngredients', methods=['POST'])
def predictIngredientes():
    uploaded_file = request.files['file']
    ingredients = objectService.detectIngredients(uploaded_file)
    print(list(ingredients.keys()))

    return jsonify(IngredientsClient.findByIngredients(['apple']))


if __name__ == '__main__':
    app.run(debug=True)
    print(__name__)
