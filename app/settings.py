from starlette.config import Config
from starlette.datastructures import Secret


class Settings:
    def __init__(self) -> None:
        try:
            self._config = Config(".env")
        except FileNotFoundError:
            self._config = Config()

        self.DATABASE_URL = self._config("DATABASE_URL", cast=Secret)
        self.TEST_DATABASE_URL = self._config("TEST_DATABASE_URL", cast=Secret)


settings = Settings()
DATABASE_URL = settings.DATABASE_URL
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
