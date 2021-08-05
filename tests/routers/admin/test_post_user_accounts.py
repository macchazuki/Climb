from http import HTTPStatus
from voluptuous_assertions import assert_response_with_db

import pytest
from factories import UserFactory

from src.common.messages import Errors
from src.common.models import User


class TestPostUserAccounts:
    @pytest.fixture(scope='function')
    def db_cleanup(self, db_session):
        yield
        db_session.query(User).delete()
        db_session.commit()

    @pytest.fixture(scope='function')
    def populate_single_user(self, db_session, db_cleanup):
        user = UserFactory(
            username='TEST_USERNAME_EXISTING',
            email='TEST_EMAIL_EXISTING@test.com',
            hashed_password='TEST_PASSWORD_a_1_EXISTING_NOTREALLYHASHED'
        )
        yield user

    def test_create_user_successful(self, test_client, db_session):
        response = test_client.post(
            'admin/',
            json={
                'username': 'TEST_USERNAME_NEW',
                'email': 'TEST_EMAIL_NEW@test.com',
                'password': 'TEST_PASSWORD_a_1_EXISTING'
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['username'] == 'TEST_USERNAME_NEW'
        user = db_session.query(User).filter(User.id == response.json()['id']).one_or_none()
        assert_response_with_db(response.json(), user)

    def test_create_user_username_already_exists(
        self, populate_single_user, test_client, db_session
    ):
        response = test_client.post(
            'admin/',
            json={
                'username': 'TEST_USERNAME_EXISTING',
                'email': 'TEST_EMAIL_NEW@test.com',
                'password': 'TEST_PASSWORD_a_1_EXISTING'
            }
        )
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()['detail'] == Errors.USERNAME_ALREADY_EXISTS

    def test_create_user_email_already_exists(self, populate_single_user, test_client, db_session):
        response = test_client.post(
            'admin/',
            json={
                'username': 'TEST_USERNAME_NEW',
                'email': 'TEST_EMAIL_EXISTING@test.com',
                'password': 'TEST_PASSWORD_a_1_EXISTING'
            }
        )
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()['detail'] == Errors.EMAIL_ALREADY_EXISTS
