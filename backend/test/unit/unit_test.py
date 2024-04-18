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
    def test_valid_email_single_user(self, dao_mock, controller):
        dao_mock.find.return_value = [{'email': 'john@doe.com', 'name': 'John Doe'}]
        expected = {'email': 'john@doe.com', 'name': 'John Doe'}
        result = controller.get_user_by_email('john@doe.com')
        dao_mock.find.assert_called_once_with({'email': 'john@doe.com'})
        assert result == expected

    def test_nonexistent_email_raises_error(self, dao_mock, controller):
        invalid_email = 'invalid_email'
        with pytest.raises(ValueError):
            controller.get_user_by_email(invalid_email)
        dao_mock.find.assert_not_called()

    def test_email_not_found_returns_none(self, dao_mock, controller):
        dao_mock.find.return_value = []
        result = controller.get_user_by_email('nonexistent@example.com')
        dao_mock.find.assert_called_once_with({'email': 'nonexistent@example.com'})
        assert result is None

    def test_duplicate_emails_found_raises_exception(self, dao_mock, controller):
        dao_mock.find.return_value = [{'email': 'john@doe.com', 'name': 'John Doe 1'}, {'email': 'john@doe.com', 'name': 'John Doe 2'}]
        with pytest.raises(Exception):
            controller.get_user_by_email('john@doe.com')
        dao_mock.find.assert_called_once_with({'email': 'john@doe.com'})

    def test_empty_email_raises_value_error(self, dao_mock, controller):
        empty_email = ''
        with pytest.raises(ValueError):
            controller.get_user_by_email(empty_email)
        dao_mock.find.assert_not_called()

    def test_null_email_raises_type_error(self, dao_mock, controller):
        null_email = None
        with pytest.raises(TypeError):
            controller.get_user_by_email(null_email)
        dao_mock.find.assert_not_called()