import json
import os.path
import discord
from datetime import datetime, timedelta

import requests
from base.logger import Logger
from base.config import BotConfig

class Utilities:
    def __init__(self):
        self.config = BotConfig()
        self.logger = Logger(__name__).get_logger()

    def is_token_valid(self) -> bool:
        token = self.config.TOKEN
        return len(token) == 59

    def is_server_online(self) -> bool:
        url = self.config.SERVER_INFO_URL
        try:
            requests.get(url, timeout=5)
            return True
        except requests.exceptions.ConnectionError:
            return False

    @staticmethod
    async def ban_bot(bot) -> bool:
        try:
            await bot.ban(reason="Bot-Verbot")
        except Exception as e:
            return False

    @staticmethod
    async def check_user_account(member: discord.Member) -> bool:
        current_date = datetime.now().strftime("%Y-%m-%d")
        member_date = member.created_at.strftime("%Y-%m-%d")

        if (datetime.strptime(current_date, "%Y-%m-%d") - datetime.strptime(member_date, "%Y-%m-%d")).days < 7 and not member.bot:
            return False

    def check_server_status(self) -> bool | str:
        url = self.config.SERVER_INFO_URL
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return "🟢 Server ist online"
            else:
                self.logger.error(f"Server ist erreichbar, aber Statuscode {response.status_code}")
                return "🟡 Server Started grade"
        except requests.exceptions.ConnectionError:
            print("Server ist offline 🔴")
            return "🔴 Server ist offline"
        except requests.exceptions.Timeout:
            print("Zeitüberschreitung beim Verbinden zum Server 🔴")
            return "🔴 Server ist offline"
        except Exception as e:
            print(f"Unbekannter Fehler: {str(e)} 🔴")
            return "🔴 Server ist offline"

    def get_server_players_count(self) -> int | dict[str, str]:
        url = self.config.SERVER_PLAYERS_URL

        if not self.is_server_online():
            return {"error": "Server ist offline"}

        try:
            response = requests.get(url, headers={'Cache-Control': 'no-cache'})
            response.raise_for_status()

            data = response.json()
            self.logger.debug(f"JSON-Daten erfolgreich geladen: {data}")

            return len(data)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Fehler beim Abrufen der Daten: {e}")
            return {"error": "Fehler beim Abrufen der Daten"}
        except ValueError as e:
            self.logger.error(f"❌ Fehler beim Verarbeiten der JSON-Daten: {e}")
            return {"error": "Fehler beim Verarbeiten der Daten"}

    def server_players(self) -> str:
        player_count = self.get_server_players_count()

        if isinstance(player_count, int):
            return f"{player_count} Spieler"
        elif isinstance(player_count, dict):
            return player_count.get("error", "Unbekannter Fehler")
        else:
            return "Fehler bei der Spielerabfrage"

    def get_server_config(self):
        config = self.config.SERVER_CONFIG

        if os.path.exists(config):
            try:
                with open(config, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Fehler: Die Config-Datei ist keine gültige JSON-Datei.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
        else:
            print(f"Die Datei {config} existiert nicht!")
        return {}

    def get_restarter_schedule(self):
        config = self.get_server_config()

        restarter_schedule = config.get("monitor", {}).get("restarterSchedule", [])

        if not restarter_schedule:
            return None

        now = datetime.now()

        restarter_times = [datetime.strptime(t, "%H:%M").time() for t in restarter_schedule]

        next_restart = None
        for restart_time in restarter_times:
            restart_datetime = datetime.combine(now.date(), restart_time)
            if restart_datetime > now:
                next_restart = restart_datetime
                break
        if not next_restart:
            restart_datetime = datetime.combine(now.date() + timedelta(days=1), restarter_times[0])
            next_restart = restart_datetime
        return next_restart.strftime("%H:%M")



