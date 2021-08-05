from voluptuous_assertions import assert_response_with_db
import uuid
from http import HTTPStatus

import pytest
from factories import UserFactory

from src.common.messages import Errors
from src.common.models import User


class TestPatchUserAccounts:

    @pytest.fixture(scope='function')
    def populate_single_user(self, db_session):
        user = UserFactory(
            username='TEST_USER_NAME_11',
            email='TEST_EMAIL_11@test.com',
            hashed_password='TEST_PASSWORD_a_11_NOTREALLYHASHED'
        )
        yield user
        # Cleanup and delete the user that was created in this fixture
        db_session.query(User).delete()
        db_session.commit()

    def test_patch_user_email_successful(self, test_client, db_session, populate_single_user):
        user = populate_single_user
        updated_email = 'TEST_EMAIL_11_UPDATED@test.com'
        response = test_client.patch(
            f'admin/{str(user.id)}',
            json={'email': f'{updated_email}'}
        )
        assert response.status_code == HTTPStatus.OK
        user = db_session.query(User).filter(User.email == updated_email).one_or_none()
        assert user is not None
        assert_response_with_db(response.json(), user)

    def test_patch_user_password_successful(
        self, test_client, db_session, populate_single_user
    ):
        user = populate_single_user
        updated_password = 'TEST_PASSWORD_a_11_UPDATED'
        response = test_client.patch(
            f'admin/{str(user.id)}',
            json={'password': f'{updated_password}'}
        )
        assert response.status_code == HTTPStatus.OK
        user = db_session.query(User).filter(User.id == user.id).one_or_none()
        assert user.hashed_password == f'{updated_password}_NOTREALLYHASHED'
        assert_response_with_db(response.json(), user)

    def test_patch_user_id_not_found(self, test_client, db_session):
        fake_id = uuid.uuid4()
        response = test_client.patch(
            'admin/' + str(fake_id),
            json={'email': 'TEST_EMAIL_11_UPDATED@test.com'}
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['detail'] == Errors.ID_NOT_FOUND
