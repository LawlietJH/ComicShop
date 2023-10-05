import pytest
from fastapi.testclient import TestClient

from main import app, prefix


@pytest.mark.infrastructure
@pytest.mark.routes
class TestIntegrationRoutes:
    client = TestClient(app)
    hello_world = "Hello World"

    @pytest.mark.invalids
    def test_invalid_endpoint(self):
        with self.client as client:
            response = client.get(f'{prefix}/prefix')
            data = response.json()
            assert response.status_code == 404
            assert 'data' in data
            assert 'meta' in data

    @pytest.mark.invalids
    def test_invalid_method(self):
        with self.client as client:
            response = client.post(f'{prefix}/')
            data = response.json()
            assert response.status_code == 405
            assert 'data' in data
            assert 'meta' in data

    @pytest.mark.checks
    @pytest.mark.endpoints
    def test_liveness(self):
        with self.client as client:
            response = client.get(f'{prefix}/liveness')
            data = response.json()
            assert response.status_code == 200
            assert 'status' in data
            assert data['status'] == 'Success'

    @pytest.mark.checks
    @pytest.mark.endpoints
    def test_readiness(self):
        with self.client as client:
            response = client.get(f'{prefix}/readiness')
            data = response.json()
            assert response.status_code == 200
            assert 'data' in data
            assert 'meta' in data
            assert 'status' in data['data']
            assert data['data']['status'] == 'Mongo is alive'

    @pytest.mark.checks
    @pytest.mark.endpoints
    def test_hello_world(self):
        with self.client as client:
            response = client.get(f'{prefix}')
            data = response.json()
            assert response.status_code == 200
            assert 'data' in data
            assert 'meta' in data
            assert 'status' in data['data']
            assert data['data']['status'] == self.hello_world

    @pytest.mark.checks
    @pytest.mark.endpoints
    def test_get_hello_person(self):
        with self.client as client:
            query_params = {'name': 'Juan', 'age': 30}
            response = client.get(f'{prefix}/person', params=query_params)
            data = response.json()
            assert response.status_code == 200
            assert 'data' in data
            assert 'meta' in data
            assert 'status' in data['data']
            assert data['data']['status'] == self.hello_world

    @pytest.mark.checks
    @pytest.mark.endpoints
    def test_post_hello_person(self):
        with self.client as client:
            person_id = 1
            body = {'name': 'Juan', 'age': 30}
            response = client.post(f'{prefix}/person/{person_id}', json=body)
            data = response.json()
            assert response.status_code == 200
            assert 'data' in data
            assert 'meta' in data
            assert 'status' in data['data']
            assert data['data']['status'] == self.hello_world

    # TODO: It is necessary to add here each of your routes and their possible
    #  http responses.
