from typing import TYPE_CHECKING, AsyncGenerator

import pytest_asyncio

if TYPE_CHECKING:
    from httpx import AsyncClient
 
# 하위 테스트 모듈에서 공통으로 사용할 플러그인/픽스처 로드
pytest_plugins = [
    "tests.users.conftest"
]


@pytest_asyncio.fixture(autouse=True, scope="session")
async def set_test_env():
    import os
    os.environ["ENV"] = "test"

@pytest_asyncio.fixture(scope="function")
async def async_client(set_test_env) -> AsyncGenerator["AsyncClient", None]:
    from httpx import AsyncClient, ASGITransport

    from wapang.main import app
    from wapang.database.common import Base
    from wapang.database.async_connection import async_db_manager
    
    # 데이터베이스 초기화 및 스키마 반영
    async with async_db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/"
    ) as client:
        yield client
    
    # 데이터베이스 스키마 삭제 및 초기화
    async with async_db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_db_manager.engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def user(
    async_client: "AsyncClient",
    user_signup_data: dict
) -> dict:
    req = user_signup_data

    res = await async_client.post("/api/users/", json=req)
    
    return res.json()