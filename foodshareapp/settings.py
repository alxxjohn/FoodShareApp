import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings
from yarl import URL
from aioredis import from_url


TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    redis_host: str = "cache"
    redis_port: int = 6379
    redis_username: str = " "
    redis_password: str = "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"
    rd_db: int = 1

    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "foodshareapp_api"
    db_pass: str = "foodshareapp_api"
    db_base: str = "foodshareapp_api"
    db_echo: bool = False
    db_ssl_enable = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    async def redis_conn(self) -> str:
        """
        Assemble Redis URL from self.
        Args:
            self ( _obj_ ) : object reference.
        Returns:
            str: The assembled Redis host URL.
        """
        return await from_url(
            "redis://"
            + self.redis_username
            + ":"
            + self.redis_password
            + "@"
            + self.redis_host
            + ":"
            + self.redis_port
            + "/"
            "0",
            decode_responses=True,
        )

    class Config:
        env_file = ".env"
        env_prefix = "FOODSHAREAPP_API_"
        env_file_encoding = "utf-8"


settings = Settings()
