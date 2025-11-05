import pytest
from fastapi.testclient import TestClient

# tests/users 모듈에서 공통으로 사용하는 fixture를 정의
@pytest.fixture
def user_signup_data():
    return {
        "email": "test1234@snu.ac.kr",
        "password": "password123"
    }
