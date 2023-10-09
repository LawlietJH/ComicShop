import pytest
from fastapi.testclient import TestClient

from main import app, prefix


@pytest.mark.infrastructure
@pytest.mark.routes
class TestIntegrationRoutes:
    client = TestClient(app)

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
