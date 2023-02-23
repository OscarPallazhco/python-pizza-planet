import pytest
from app.controllers import BeverageController


def test_create(app, beverage: dict):
    created_beverage, error = BeverageController.create(beverage)
    pytest.assume(error is None)
    for param, value in beverage.items():
        pytest.assume(param in created_beverage)
        pytest.assume(value == created_beverage[param])
        pytest.assume(created_beverage['_id'])


def test_create__should_return_message_when_required_info_is_missing(app, beverage):
    del beverage["price"]
    created_beverage, error = BeverageController.create(beverage)
    pytest.assume(created_beverage is None)
    pytest.assume(error == 'Invalid beverage payload')


def test_create__returns_error_message_when_have_an_error(app, beverage, mocker, manager_error):
    mocker.patch('app.repositories.managers.BeverageManager.create', side_effect = manager_error)
    created_beverage, error = BeverageController.create(beverage)
    pytest.assume(created_beverage == None)
    pytest.assume(error == 'Manager error')


def test_update(app, beverage: dict):
    created_beverage, _ = BeverageController.create(beverage)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }
    updated_beverage, error = BeverageController.update({
        '_id': created_beverage['_id'],
        **updated_fields
    })
    pytest.assume(error is None)
    beverage_from_database, error = BeverageController.get_by_id(created_beverage['_id'])
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_beverage[param] == value)
        pytest.assume(beverage_from_database[param] == value)


def test_update__returns_error_message_when_have_an_error(app, beverage, mocker, manager_error):
    created_beverage, _ = BeverageController.create(beverage)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }
    mocker.patch('app.repositories.managers.BeverageManager.update', side_effect = manager_error)
    updated_beverage, error = BeverageController.update({
        '_id': created_beverage['_id'],
        **updated_fields
    })
    pytest.assume(updated_beverage == None)
    pytest.assume(error == 'Manager error')


def test_get_by_id(app, beverage: dict):
    created_beverage, _ = BeverageController.create(beverage)
    beverage_from_db, error = BeverageController.get_by_id(created_beverage['_id'])
    pytest.assume(error is None)
    for param, value in created_beverage.items():
        pytest.assume(beverage_from_db[param] == value)


def test_get_by_id__returns_empty_object_when_id_no_exists(app, beverage: dict):
    created_beverage, _ = BeverageController.create(beverage)
    beverage_from_db, error = BeverageController.get_by_id(created_beverage['_id'] + 10)
    pytest.assume(error == None)
    pytest.assume(beverage_from_db == {})


def test_get_by_id__returns_error_message_when_have_an_error(app, mocker, manager_error):
    mocker.patch('app.repositories.managers.BeverageManager.get_by_id', side_effect = manager_error)
    beverage_from_db, error = BeverageController.get_by_id(1)
    pytest.assume(beverage_from_db == None)
    pytest.assume(error == 'Manager error')


def test_get_all(app, beverages: list):
    created_beverages = []
    for beverage in beverages:
        created_beverage, _ = BeverageController.create(beverage)
        created_beverages.append(created_beverage)

    beverages_from_db, error = BeverageController.get_all()
    searchable_beverages = {db_beverage['_id']: db_beverage for db_beverage in beverages_from_db}
    pytest.assume(error is None)
    for created_beverage in created_beverages:
        current_id = created_beverage['_id']
        assert current_id in searchable_beverages
        for param, value in created_beverage.items():
            pytest.assume(searchable_beverages[current_id][param] == value)
