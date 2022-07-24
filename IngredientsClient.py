import requests

BASE_URL = 'https://api.spoonacular.com/recipes/'
API_KEY = '#'


def findByIngredients(input_ingredients):
    ing = ' '.join([str(item) + "," for item in input_ingredients])
    payload = {'ingredients': ing, 'apiKey': API_KEY}
    response = requests.get('{}/findByIngredients'.format(BASE_URL), params=payload)
    return response.json()
