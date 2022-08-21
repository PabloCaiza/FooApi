import requests

BASE_URL = 'https://api.spoonacular.com/recipes/'
API_KEY = 'e4bdc2f9f29a43398fc981acfe1db13d'


def findByIngredients(input_ingredients):
    ing = ' '.join([str(item) + "," for item in input_ingredients])
    payload = {'ingredients': ing, 'apiKey': API_KEY}

    response = requests.get('{}/findByIngredients'.format(BASE_URL), params=payload)
    return response.json()
