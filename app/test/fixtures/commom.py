import pytest

@pytest.fixture
def controller_error():
    return (None, 'Controller error')


@pytest.fixture
def manager_error():
    return RuntimeError('Manager error')