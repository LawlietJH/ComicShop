import json
import os
import sys

import pytest

sys.path.append(f'{os.path.dirname(__file__)}/../src')


class MockData:
    json_data: dict = {}
    base: str = 'tests/unit_tests/mock_data/'

    @classmethod
    def response_from_json(cls) -> dict:
        files = next(os.walk(cls.base))[2]
        files = list(
            filter(lambda filename: filename.endswith('.json'), files))
        files = list(map(lambda filename: filename[:-5], files))
        return {path: json.load(open(f'{cls.base}{path}.json')) for path in
                files}

    @classmethod
    def set_json_data(cls) -> None:
        cls.json_data = cls.response_from_json()


@pytest.fixture
def test_data(request):
    if not MockData.json_data:
        MockData.set_json_data()
    return MockData.json_data
