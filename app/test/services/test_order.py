import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_order_service(create_order):
    order = create_order.json

    pytest.assume(create_order.status.startswith('200'))
    pytest.assume(order['_id'])
    pytest.assume(order['client_name'])
    pytest.assume(order['client_dni'])
    pytest.assume(order['client_address'])
    pytest.assume(order['client_phone'])
    pytest.assume(order['size'])
    pytest.assume(order['total_price'])


def test_create_order_service__returns_400_when_have_an_error(client, order_uri, order, controller_error, mocker):
    mocker.patch('app.controllers.order.OrderController.create', return_value = controller_error)
    response = client.post(order_uri, json=order)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_update_order_service(client, create_order, order_uri):
    current_order = create_order.json
    update_data = {**current_order, 'name': get_random_string()}
    response = client.put(order_uri, json=update_data)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'].startswith('Method not suported'))


def test_get_order_by_id_service(client, create_order, order_uri):
    current_order = create_order.json
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)


def test_get_order_by_id_service__returns_404_when_id_no_exists(client, create_order, order_uri):
    current_order = create_order.json
    response = client.get(f'{order_uri}id/{current_order["_id"] + 1}')
    pytest.assume(response.status.startswith('404'))
    pytest.assume(response.json == {})


def test_get_order_by_id_service__returns_400_when_have_an_error(client, order_uri, controller_error, mocker):
    mocker.patch('app.controllers.order.OrderController.get_by_id', return_value = controller_error)
    response = client.get(f'{order_uri}id/1')
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')


def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_orders = {order['_id']: order for order in response.json}
    for order in create_orders:
        pytest.assume(order['_id'] in returned_orders)


def test_get_orders_service__return_404_when_not_have_orders(client, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('404'))
    pytest.assume(response.json == [])


def test_get_orders_service__return_400_when_have_an_error(client, order_uri, mocker, controller_error):
    mocker.patch('app.controllers.order.OrderController.get_all', return_value = controller_error)
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'] == 'Controller error')
