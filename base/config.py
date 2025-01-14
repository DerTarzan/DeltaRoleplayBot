import os
import platform
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class ConfigError(Exception):
    pass


class BotConfigHandler:
    _instance: Optional["BotConfigHandler"] = None

    def __new__(cls, *args, **kwargs) -> "BotConfigHandler":
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, dev_mode=True):
        self.DEV_MODE = dev_mode

        if self.DEV_MODE is True:
            if platform.system() == "Linux":
                exit("❌ Development mode is not supported on Linux.")

        self.load_dotenvs()

    @staticmethod
    def load_dotenv_file(path: Path) -> None:
        if not load_dotenv(path):
            raise FileNotFoundError(f"Fehler beim Laden der Konfigurationsdatei: {path}")

    def load_dotenvs(self) -> None:
        base_dir = Path(__file__).parent / "resources"

        try:
            if self.DEV_MODE:
                self.load_dotenv_file(base_dir / "dev_config.env")
                os.environ["DEV_MODE"] = "True"
            else:
                self.load_dotenv_file(base_dir / "config.env")
                os.environ["DEV_MODE"] = "False"

            self.load_dotenv_file(base_dir / "token.env")

        except FileNotFoundError:
            raise ConfigError("Konfigurationsdatei nicht gefunden")

class BotConfig(BotConfigHandler):
    def __init__(self):
        super().__init__()

    @property
    def TOKEN(self) -> str:
        if self.DEV_MODE:
            return self._get_env_var("DRP_DEVELOPER_BOT_TOKEN")
        return self._get_env_var("DISCORD_BOT_TOKEN")

    @property
    def SERVER_PLAYERS_URL(self) -> str:
        return self._get_env_var("SERVER_PLAYERS_URL")

    @property
    def SERVER_INFO_URL(self) -> str:
        return self._get_env_var("SERVER_INFO_URL")

    @property
    def SERVER_CONFIG(self):
        return self._get_env_var("SERVER_CONFIG_PATH")

    @property
    def DATABASE(self) -> str:
        return self._get_env_var("DATABASE_PATH")

    @property
    def TICKET_REASONS_PATH(self) -> str:
        return self._get_env_var("TICKET_REASONS_PATH")

    @property
    def ASSETS_PATH(self) -> str:
        return self._get_env_var("ASSETS_PATH")

    @property
    def CHANGELOG_PATH(self) -> str:
        return self._get_env_var("CHANGELOG_PATH")

    @property
    def WELCOME_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("WELCOME_CHANNEL_ID"))

    @property
    def SERVER_STATUS_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("SERVER_STATUS_CHANNEL_ID"))

    @property
    def SERVER_RESTART_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("SERVER_RESTART_CHANNEL_ID"))

    @property
    def SERVER_MEMBERS_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("SERVER_TOTAL_MEMBERS_CHANNEL_ID"))

    @property
    def VERIFY_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("VERIFY_CHANNEL_ID"))

    @property
    def RULES_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("RULES_CHANNEL_ID"))

    @property
    def TICKET_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("TICKET_CHANNEL_ID"))

    @property
    def ID_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("ID_CHANNEL_ID"))

    @property
    def SUPPORT_WAITING_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("SUPPORT_WAITING_CHANNEL_ID"))

    @property
    def INFO_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("INFO_CHANNEL_ID"))

    @property
    def DELTA_TEAM_ROLE_ID(self) -> int:
        return int(self._get_env_var("DELTA_TEAM_ROLE_ID"))

    @property
    def EINWOHNER_ROLE_ID(self) -> int:
        return int(self._get_env_var("EINWOHNER_ROLE_ID"))

    @staticmethod
    def _get_env_var(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ConfigError(f"Die Umgebungsvariable '{key}' konnte nicht geladen werden")
        return value