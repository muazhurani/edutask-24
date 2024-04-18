import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock

@pytest.fixture
def dao_mock():
    dao = MagicMock()
    yield dao

@pytest.fixture
def controller(dao_mock):
    controller = UserController(dao_mock)
    yield controller
@pytest.mark.unit
class TestUserController:
    def test_single_user_valid_email(self, dao_mock, controller):
        dao_mock.find.return_value = [{'email': 'test@example.com', 'name': 'Test User'}]
        expected_user = {'email': 'test@example.com', 'name': 'Test User'}
        result = controller.get_user_by_email('test@example.com')
        dao_mock.find.assert_called_once_with({'email': 'test@example.com'})
        assert result == expected_user

    def test_invalid_email(self, dao_mock, controller):
        invalid_email = 'invalid_email'
        with pytest.raises(ValueError):
            controller.get_user_by_email(invalid_email)
        dao_mock.find.assert_not_called()

    def test_no_user_found(self, dao_mock, controller):
        dao_mock.find.return_value = []
        result = controller.get_user_by_email('nonexistent@example.com')
        dao_mock.find.assert_called_once_with({'email': 'nonexistent@example.com'})
        assert result is None

    def test_multiple_users_found(self, dao_mock, controller):
        dao_mock.find.return_value = [{'email': 'test@example.com', 'name': 'Test User 1'}, {'email': 'test@example.com', 'name': 'Test User 2'}]
        with pytest.raises(Exception):
            controller.get_user_by_email('test@example.com')
        dao_mock.find.assert_called_once_with({'email': 'test@example.com'})