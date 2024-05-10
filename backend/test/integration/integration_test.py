import pytest
from pymongo import MongoClient
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture(scope="function")
def test_dao():
    # Configuration for a test database
    client = MongoClient('mongodb://localhost:27017/')
    db = client["test_db"]
    collection = db["test_collection"]

    # Validator similar to the one used in production, adjust as needed
    mock_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['name', 'email'],
            'properties': {
                'name': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                }
            }
        }
    }

    # Set up the collection with the validator
    if "test_collection" not in db.list_collection_names():
        db.create_collection("test_collection", validator=mock_validator)

    # Initialize DAO with the test collection
    dao_instance = DAO('test_collection')
    yield dao_instance

    # Cleanup
    db.drop_collection("test_collection")
    client.close()


class TestDAOCreation:
    def test_create_valid_input(self, test_dao):
        result = test_dao.create({'name': 'Jane', 'email': 'jane.doe@example.com'})
        assert result is not None
        assert result['name'] == 'Jane'
        assert result['email'] == 'jane.doe@example.com'

    def test_create_fail_missing_name(self, test_dao):
        with pytest.raises(WriteError):
            test_dao.create({'email': 'jane.doe@example.com'})

    def test_create_fail_missing_email(self, test_dao):
        with pytest.raises(WriteError):
            test_dao.create({'name': 'Jane'})

    def test_create_no_input(self, test_dao):
        with pytest.raises(WriteError):
            test_dao.create({})

    def test_create_with_wrong_nametype(self, test_dao):
        with pytest.raises(WriteError):
            test_dao.create({'name': 1234, 'email': 'jane.doe@example.com'})

    def test_create_with_wrong_emailtype(self, test_dao):
        with pytest.raises(WriteError):
            test_dao.create({'name': 'Jane', 'email': 1234})

    def test_create_with_extra_fields(self, test_dao):
        # This should succeed if the extra field does not violate the schema
        result = test_dao.create({'name': 'Jane', 'email': 'jane.doe@example.com', 'age': 30})
        assert result is not None
        assert 'age' not in result

    def test_create_with_minimal_strings(self, test_dao):
        # This will depend on whether the validator allows empty strings
        with pytest.raises(WriteError):
            test_dao.create({'name': '', 'email': 'jane.doe@example.com'})
