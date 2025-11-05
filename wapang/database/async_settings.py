from pydantic_settings import BaseSettings, SettingsConfigDict
from wapang.settings import SETTINGS


class AsyncDatabaseSettings(BaseSettings):
    dialect: str
    async_driver: str
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        return f"{self.dialect}+{self.async_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="DB_",
        env_file=SETTINGS.env_file,
        extra='ignore'
    )


ASYNC_DB_SETTINGS = AsyncDatabaseSettings()