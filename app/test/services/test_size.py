import pytest
from app.test.utils.functions import get_random_string, get_random_price

def test_create_size_service(create_size):
    size = create_size.json
    pytest.assume(create_size.status.startswith('200'))
    pytest.assume(size['_id'])
    pytest.assume(size['name'])
    pytest.assume(size['price'])


def test_create_size_service__returns_400_when_have_an_error(client, size_uri, size, controller_error, mocker):
    mocker.patch('app.controllers.size.SizeController.create', return_value = controller_error)
    response = client.post(size_uri, json=size)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_update_size_service(client, create_size, size_uri):
    current_size = create_size.json
    update_data = {**current_size, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(size_uri, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)


def test_update_size_service__returns_400_when_have_an_error(client, create_size, size_uri, controller_error, mocker):
    current_size = create_size.json
    update_data = {**current_size, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    mocker.patch('app.controllers.size.SizeController.update', return_value = controller_error)
    response = client.put(size_uri, json=update_data)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_get_size_by_id_service(client, create_size, size_uri):
    current_size = create_size.json
    response = client.get(f'{size_uri}id/{current_size["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)


def test_get_size_by_id_service__returns_404_when_id_no_exists(client, create_size, size_uri):
    current_size = create_size.json
    response = client.get(f'{size_uri}id/{current_size["_id"] + 1}')
    pytest.assume(response.status.startswith('404'))
    pytest.assume(response.json == {})


def test_get_size_by_id_service__returns_400_when_have_an_error(client, size_uri, controller_error, mocker):
    mocker.patch('app.controllers.size.SizeController.get_by_id', return_value = controller_error)
    response = client.get(f'{size_uri}id/1')
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_get_sizes_service(client, create_sizes, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith('200'))
    returned_sizes = {size['_id']: size for size in response.json}
    for size in create_sizes:
        pytest.assume(size['_id'] in returned_sizes)


def test_get_sizes_service__return_404_when_not_have_sizes(client, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith('404'))
    pytest.assume(response.json == [])


def test_get_sizes_service__return_400_when_have_an_error(client, size_uri, mocker, controller_error):
    mocker.patch('app.controllers.size.SizeController.get_all', return_value = controller_error)
    response = client.get(size_uri)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')
