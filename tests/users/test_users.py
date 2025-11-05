from random import choice

import pytest
from httpx import AsyncClient


# users 모듈의 API 테스트 코드

@pytest.mark.asyncio
async def test_signup(
    async_client: AsyncClient,
    user_signup_data: dict
):
    # Arrange(준비)
    req = user_signup_data

    # Act(실행)
    res = await async_client.post("/api/users/", json=req)
    
    # Assert(검증)
    assert res.status_code == 201
    res_json = res.json()
    assert res_json.get("id") is not None
    assert res_json.get("email") == user_signup_data.get("email")

@pytest.mark.asyncio
async def test_signup_missing_email(
    async_client: AsyncClient,
    user_signup_data: dict
):
    req = { k:v for k, v in user_signup_data.items() if k != "email"}

    res = await async_client.post("/api/users/", json=req)
    
    assert res.status_code == 400
    res_json = res.json()
    assert res_json.get("error_code") == "ERR_002"
    assert res_json.get("error_msg") == "MISSING REQUIRED FIELDS"

@pytest.mark.asyncio
async def test_signup_missing_password(
    async_client: AsyncClient,
    user_signup_data: dict
):
    req = { k:v for k, v in user_signup_data.items() if k != "password"}

    res = await async_client.post("/api/users/", json=req)
    
    assert res.status_code == 400
    res_json = res.json()
    assert res_json.get("error_code") == "ERR_002"
    assert res_json.get("error_msg") == "MISSING REQUIRED FIELDS"

@pytest.mark.asyncio
async def test_signup_invalid_email(
    async_client: AsyncClient,
    user_signup_data: dict
):
    req = { k:v for k, v in user_signup_data.items() if k != "email"}
    req["email"] = "invalid.email.format"

    res = await async_client.post("/api/users/", json=req)
    
    assert res.status_code == 400
    res_json = res.json()
    assert res_json.get("error_code") == "ERR_003"
    assert res_json.get("error_msg") == "INVALID FIELD FORMAT"

@pytest.mark.asyncio
async def test_signup_short_password(
    async_client: AsyncClient,
    user_signup_data: dict
):
    req = { k:v for k, v in user_signup_data.items() if k != "password"}
    req["password"] = "short"

    res = await async_client.post("/api/users/", json=req)

    assert res.status_code == 400
    res_json = res.json()
    assert res_json.get("error_code") == "ERR_003"
    assert res_json.get("error_msg") == "INVALID FIELD FORMAT"

@pytest.mark.asyncio
async def test_signup_long_password(
    async_client: AsyncClient,
    user_signup_data: dict
):
    req = { k:v for k, v in user_signup_data.items() if k != "password"}
    req["password"] = "".join(choice("abcdefghijklmnopqrstuvwxyz") for _ in range(129))

    res = await async_client.post("/api/users/", json=req)

    assert res.status_code == 400
    res_json = res.json()
    assert res_json.get("error_code") == "ERR_003"
    assert res_json.get("error_msg") == "INVALID FIELD FORMAT"


@pytest.mark.asyncio
async def test_signup_email_conflict(
    async_client: AsyncClient,
    user: dict
):
    req = {
        "email": user.get("email"),
        "password": "password321"
    }

    res = await async_client.post("/api/users/", json=req)

    assert res.status_code == 409
    res_json = res.json()
    assert res_json.get("error_code") == "ERR_004"
    assert res_json.get("error_msg") == "EMAIL ALREADY EXISTS"
