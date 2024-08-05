import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock, patch

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
    def test_get_user_by_email_invalid_email(self, dao_mock, controller):
        invalid_email = "invalid.email"

        with pytest.raises(ValueError, match='Error: invalid email address'):
            controller.get_user_by_email(invalid_email)

        dao_mock.find.assert_not_called()

    def test_get_user_by_email_no_user_found(self, dao_mock, controller):
        email = "nonexistent@example.com"
        dao_mock.find.return_value = []

        result = controller.get_user_by_email(email)

        assert result is None

        dao_mock.find.assert_called_once_with({'email': email})

    def test_get_user_by_email_success(self, dao_mock, controller):
        email = "user@example.com"
        expected_user = {'email': email, 'name': 'John Doe'}
        dao_mock.find.return_value = [expected_user]

        result = controller.get_user_by_email(email)

        assert result == expected_user

        dao_mock.find.assert_called_once_with({'email': email})

    def test_get_user_by_email_multiple_users_found(self, dao_mock, controller):
        email = "duplicate@example.com"
        users = [
            {'email': email, 'name': 'User 1'},
            {'email': email, 'name': 'User 2'}
        ]
        dao_mock.find.return_value = users

        with patch('builtins.print') as mocked_print:
            result = controller.get_user_by_email(email)

        assert result == users[0]

        dao_mock.find.assert_called_once_with({'email': email})
        mocked_print.assert_called_once_with(f'Error: more than one user found with mail {email}')