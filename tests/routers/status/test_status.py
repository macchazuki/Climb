from http import HTTPStatus


class TestStatus:
    def test_get_healthy_status(self, test_client):
        response = test_client.get('/status')

        assert response.status_code == HTTPStatus.OK
        assert response.json()['database_connection_ok'] == 'OK'
