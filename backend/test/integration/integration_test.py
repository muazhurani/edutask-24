import pytest
from pymongo import MongoClient
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture(scope="function")
def test_dao():
    client = MongoClient('mongodb://localhost:27017/')
    db = client["test_db"]
    collection = db["test_collection"]

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

    if "test_collection" not in db.list_collection_names():
        db.create_collection("test_collection", validator=mock_validator)

    dao_instance = DAO('test_collection')
    yield dao_instance

    db.drop_collection("test_collection")
    client.close()

class TestDAOCreation:
    def test_create_valid_input(self, test_dao):

        result = test_dao.create({'name': 'Jane Doe', 'email': 'jane.doe@example.com'})
        assert result is not None
        assert result['name'] == 'Jane Doe'
        assert result['email'] == 'jane.doe@example.com'

    def test_create_missing_field(self, test_dao):

        with pytest.raises(WriteError):
            test_dao.create({'name': 'Jane Doe'}) 
        
        with pytest.raises(WriteError):
            test_dao.create({'email': 'jane.doe@example.com'})  

    def test_create_invalid_type(self, test_dao):
        with pytest.raises(WriteError):
            test_dao.create({'name': 123, 'email': 'jane.doe@example.com'})  
        
        with pytest.raises(WriteError):
            test_dao.create({'name': 'Jane Doe', 'email': 456})  

    def test_create_multiple_objects(self, test_dao):
        objects = [
            {'name': 'Jane Doe', 'email': 'jane.doe@example.com'},
            {'name': 'John Smith', 'email': 'john.smith@example.com'}
        ]
        
        results = []
        for obj in objects:
            result = test_dao.create(obj)
            results.append(result)
            assert result is not None
            assert result['name'] == obj['name']
            assert result['email'] == obj['email']
        
        assert len(results) == 2
        assert results[0]['name'] != results[1]['name']
        assert results[0]['email'] != results[1]['email']