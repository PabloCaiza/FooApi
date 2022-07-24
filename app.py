from flask import Flask, jsonify, request
import products
import objectService
import IngredientsClient


app = Flask(__name__)


@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify(products)


@app.route('/products/<string:name>', methods=['GET'])
def getProductByName(name):
    products_found = [product for product in products if product['name'] == name]
    if len(products_found) > 0:
        return jsonify(products_found)
    return jsonify({"message": "Product not found"})


@app.route('/products', methods=['POST'])
def addProduct():
    products.append(request.json)
    return 'received'


@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    products_found = [product for product in products if product['name'] == product_name]
    if len(products_found) > 0:
        products.remove(products_found[0])
        return jsonify("deleted successfully")
    return jsonify({"message": "not founded"})


@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    product_found = [product for product in products if product['name'] == product_name]
    if len(product_found) > 0:
        product_found[0]['name'] = request.json['name']
        product_found[0]['price'] = request.json['price']
        product_found[0]['quantity'] = request.json['quantity']
        return jsonify({"message": "Updated Successfully"})

    return jsonify({"message": "not founded"})


@app.route('/lea')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/predictIngredients',methods=['POST'])
def predictIngredientes():
    uploaded_file =request.files['file']
    ingredients = objectService.detectIngredients(uploaded_file)
    print(list(ingredients.keys()))

    return jsonify(IngredientsClient.findByIngredients(['apple']))



if __name__ == '__main__':
    app.run(debug=True)
    print(__name__)
