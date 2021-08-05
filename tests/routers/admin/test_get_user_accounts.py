from voluptuous_assertions import assert_list_response_with_db, assert_response_with_db
import uuid
from http import HTTPStatus

import pytest
from factories import UserFactory

from src.common.messages import Errors
from src.common.models import User

class TestGetUserAccounts:
    @pytest.fixture(scope='class')
    def db_cleanup(self, db_session):
        yield
        db_session.query(User).delete()
        db_session.commit()

    @pytest.fixture(scope='class')
    def populate_users(self, db_cleanup):
        for user_id in range(10):
            UserFactory(
                username=f'TEST_USER_NAME_{user_id}',
                email=f'TEST_EMAIL_{user_id}@test.com',
                hashed_password=f'TEST_PASSWORD_a_{user_id}_NOTREALLYHASHED'
            )

    @pytest.fixture(scope='function')
    def populate_single_user(self, db_session):
        user = UserFactory(
            username='TEST_USER_NAME_11',
            email='TEST_EMAIL_11@test.com',
            hashed_password='TEST_PASSWORD_a_11_NOTREALLYHASHED'
        )
        yield user
        # Cleanup and delete the user that was created in this fixture
        db_session.query(User).filter(User.id == user.id).delete()
        db_session.commit()

    def test_get_users(self, populate_users, test_client, db_session):
        responses = test_client.get('admin/')
        assert responses.status_code == HTTPStatus.OK
        assert_list_response_with_db(responses.json(), db_session.query(User).all())

    def test_get_user_by_username_successful(self, populate_users, test_client, db_session):
        username = 'TEST_USER_NAME_0'
        user = db_session.query(User).filter(User.username == username).one_or_none()
        response = test_client.get(f'admin/username/{username}/')
        assert response.status_code == HTTPStatus.OK
        assert_response_with_db(response.json(), user)

    def test_get_user_by_username_username_not_found(self, populate_users, test_client):
        username = 'TEST_USER_NAME_11'
        response = test_client.get(f'admin/username/{username}/')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['detail'] == Errors.USERNAME_NOT_FOUND

    def test_get_user_by_email_successful(self, populate_users, test_client, db_session):
        email = 'TEST_EMAIL_0@test.com'
        user = db_session.query(User).filter(User.email == email).one_or_none()
        response = test_client.get(f'admin/email/{email}/')
        assert response.status_code == HTTPStatus.OK
        assert_response_with_db(response.json(), user)

    def test_get_user_by_email_email_not_found(self, populate_users, test_client):
        email = 'TEST_EMAIL_11@test.com'
        response = test_client.get(f'admin/email/{email}/')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['detail'] == Errors.EMAIL_NOT_FOUND

    def test_get_user_by_id_successful(self, test_client, db_session, populate_single_user):
        user = populate_single_user
        response = test_client.get(f'admin/{str(user.id)}')
        assert response.status_code == HTTPStatus.OK
        assert_response_with_db(response.json(), user)

    def test_get_user_by_id_id_not_found(self, populate_users, test_client, db_session):
        fake_id = uuid.uuid4()
        response = test_client.get(f'admin/{str(fake_id)}')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['detail'] == Errors.ID_NOT_FOUND
