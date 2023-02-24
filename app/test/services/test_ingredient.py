import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_ingredient_service(create_ingredient):
    ingredient = create_ingredient.json
    pytest.assume(create_ingredient.status.startswith('200'))
    pytest.assume(ingredient['_id'])
    pytest.assume(ingredient['name'])
    pytest.assume(ingredient['price'])


def test_create_ingredient_service__returns_400_when_have_an_error(client, ingredient_uri, ingredient, controller_error, mocker):
    mocker.patch('app.controllers.ingredient.IngredientController.create', return_value = controller_error)
    response = client.post(ingredient_uri, json=ingredient)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_update_ingredient_service(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    update_data = {**current_ingredient, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(ingredient_uri, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_ingredient = response.json
    for param, value in update_data.items():
        pytest.assume(updated_ingredient[param] == value)


def test_update_ingredient_service__returns_400_when_have_an_error(client, create_ingredient, ingredient_uri, controller_error, mocker):
    current_ingredient = create_ingredient.json
    update_data = {**current_ingredient, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    mocker.patch('app.controllers.ingredient.IngredientController.update', return_value = controller_error)
    response = client.put(ingredient_uri, json=update_data)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_get_ingredient_by_id_service(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    response = client.get(f'{ingredient_uri}id/{current_ingredient["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_ingredient = response.json
    for param, value in current_ingredient.items():
        pytest.assume(returned_ingredient[param] == value)


def test_get_ingredient_by_id_service__returns_404_when_id_no_exists(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    response = client.get(f'{ingredient_uri}id/{current_ingredient["_id"] + 1}')
    pytest.assume(response.status.startswith('404'))
    pytest.assume(response.json == {})


def test_get_ingredient_by_id_service__returns_400_when_have_an_error(client, ingredient_uri, controller_error, mocker):
    mocker.patch('app.controllers.ingredient.IngredientController.get_by_id', return_value = controller_error)
    response = client.get(f'{ingredient_uri}id/1')
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_get_ingredients_service(client, create_ingredients, ingredient_uri):
    response = client.get(ingredient_uri)
    pytest.assume(response.status.startswith('200'))
    returned_ingredients = {ingredient['_id']: ingredient for ingredient in response.json}
    for ingredient in create_ingredients:
        pytest.assume(ingredient['_id'] in returned_ingredients)


def test_get_ingredients_service__return_404_when_not_have_ingredients(client, ingredient_uri):
    response = client.get(ingredient_uri)
    pytest.assume(response.status.startswith('404'))
    pytest.assume(response.json == [])


def test_get_ingredients_service__return_400_when_have_an_error(client, ingredient_uri, mocker, controller_error):
    mocker.patch('app.controllers.ingredient.IngredientController.get_all', return_value = controller_error)
    response = client.get(ingredient_uri)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')