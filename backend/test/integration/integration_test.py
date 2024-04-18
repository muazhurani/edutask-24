import pytest
from pymongo import errors
from bson.objectid import ObjectId
from src.util.dao import DAO

@pytest.mark.integration
def test_integration_rule_violation_one():
    user_access = DAO("user")
    profile_data = {'lastName': 'Doe', 'email': 'John@doe.com'}

    with pytest.raises(Exception) as error_capture:
        newly_created_user = user_access.create(profile_data)
        user_identifier = newly_created_user['_id']['$oid']
        user_access.collection.delete_one({'_id': ObjectId(user_identifier)})
    assert error_capture.type == errors.WriteError


@pytest.mark.integration
def test_integration_rule_violation_three():
    user_access = DAO("user")
    initial_user = {'firstName': 'John', 'lastName': 'Doe', 'email': 'John@doe.com'}
    duplicate_user = {'firstName': 'Enaj', 'lastName': 'Eod', 'email': 'John@doe.com'}
    first_user_created = user_access.create(initial_user)

    first_user_id = first_user_created['_id']['$oid']

    with pytest.raises(Exception) as error_capture:
        second_user_created = user_access.create(duplicate_user)
        second_user_id = second_user_created['_id']['$oid']
        user_access.collection.delete_one({'_id': ObjectId(second_user_id)})
        user_access.collection.delete_one({'_id': ObjectId(first_user_id)})

    user_access.collection.delete_one({'_id': ObjectId(first_user_id)})
    assert error_capture.type == errors.WriteError

@pytest.mark.integration
def test_user_profile_creation():
    user_access = DAO("user")
    new_user_profile = {'firstName': 'John', 'lastName': 'Doe', 'email': 'John@doe.com'}

    user_profile_created = user_access.create(new_user_profile)

    profile_identifier = user_profile_created['_id']['$oid']

    user_access.collection.delete_one({'_id': ObjectId(profile_identifier)})

    del user_profile_created['_id']

    assert user_profile_created == new_user_profile

@pytest.mark.integration
def test_integration_rule_violation_two():
    user_access = DAO("user")
    profile_data = {'firstName': 10, 'lastName': 'Doe', 'email': 'John@doe.com'}

    with pytest.raises(Exception) as error_capture:
        newly_created_user = user_access.create(profile_data)
        user_identifier = newly_created_user['_id']['$oid']
        user_access.collection.delete_one({'_id': ObjectId(user_identifier)})
    assert error_capture.type == errors.WriteError

@pytest.mark.integration
def test_user_profile_update():
    user_access = DAO("user")
    new_user_profile = {'firstName': 'John', 'lastName': 'Doe', 'email': 'John@doe.com'}

    user_profile_created = user_access.create(new_user_profile)
    profile_identifier = user_profile_created['_id']['$oid']

    updated_profile_data = {'firstName': 'John', 'lastName': 'Doe', 'email': 'John.doe.updated@gmail.com'}
    user_access.collection.update_one({'_id': ObjectId(profile_identifier)}, {'$set': updated_profile_data})

    updated_user_profile = user_access.collection.find_one({'_id': ObjectId(profile_identifier)})

    user_access.collection.delete_one({'_id': ObjectId(profile_identifier)})

    del updated_user_profile['_id']

    assert updated_user_profile == updated_profile_data

@pytest.mark.integration
def test_user_profile_deletion():
    user_access = DAO("user")
    new_user_profile = {'firstName': 'John', 'lastName': 'Doe', 'email': 'John@doe.com'}

    user_profile_created = user_access.create(new_user_profile)
    profile_identifier = user_profile_created['_id']['$oid']

    user_access.collection.delete_one({'_id': ObjectId(profile_identifier)})

    deleted_user_profile = user_access.collection.find_one({'_id': ObjectId(profile_identifier)})

    assert deleted_user_profile is None