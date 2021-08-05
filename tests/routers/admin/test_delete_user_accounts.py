from voluptuous_assertions import assert_response_with_db
import uuid
from http import HTTPStatus

import pytest
from factories import UserFactory

from src.common.messages import Errors
from src.common.models import User


class TestDeleteUserAccounts:
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

    def test_delete_user_successful(self, test_client, db_session, populate_single_user):
        user = populate_single_user
        response = test_client.delete(f'/admin/{str(user.id)}')
        assert response.status_code == HTTPStatus.OK
        assert_response_with_db(response.json(), user)
        assert db_session.query(User).filter(User.id == user.id).one_or_none() is None

    def test_delete_user_id_not_found(self, test_client, db_session, populate_single_user):
        fake_id = uuid.uuid4()
        response = test_client.delete(f'admin/{str(fake_id)}')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['detail'] == Errors.ID_NOT_FOUND
