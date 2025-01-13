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

    def check_user_has_role(self, member: discord.Member, role_id: int) -> bool:
        self.logger.debug(f"Checking if user {member.name} has role {role_id}")
        return any(role.id == role_id for role in member.roles)

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
            return "🔴 Server ist offline"

    def get_server_players_count(self) -> int | dict[str, str]:
        url = self.config.SERVER_PLAYERS_URL

        if not self.is_server_online():
            return {"error": "Server ist offline"}

        try:
            response = requests.get(url, headers={'Cache-Control': 'no-cache'})
            response.raise_for_status()

            data = response.json()

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

    @staticmethod
    async def transcript(interaction: discord.Interaction, bot: discord.Bot) -> str:
        transcript_filename = f"{interaction.channel.id}.md"

        # Check if a transcript is already being generated
        if os.path.exists(transcript_filename):
            return await interaction.followup.send(f"A transcript is already being generated!", ephemeral=True)

        # Open the file for writing the transcript
        with open(transcript_filename, 'a') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n")

            # Iterate through the channel's message history
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")

                # Handle edited messages
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")

                # Check if the message has attachments (files or images)
                if message.attachments:
                    for attachment in message.attachments:
                        # Check if the attachment is an image or a file
                        if attachment.content_type and attachment.content_type.startswith("image/"):
                            f.write(f"  - Image: [Download {attachment.filename}]({attachment.url})\n")
                        else:
                            f.write(f"  - File: [Download {attachment.filename}]({attachment.url})\n")

            # Add generation information to the transcript
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {bot.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")

        # Send the transcript as a file to the user
        with open(transcript_filename, 'rb') as f:
            await interaction.followup.send(file=discord.File(f, f"{interaction.channel.name}.md"), ephemeral=True)

        # Remove the transcript file after sending it
        os.remove(transcript_filename)

    @staticmethod
    async def dm_transcript(interaction: discord.Interaction, user: str) -> str:
        transcript_filename = f"{interaction.channel.id}.md"

        # Check if a transcript is already being generated
        if os.path.exists(transcript_filename):
            return await interaction.followup.send(f"A transcript is already being generated!", ephemeral=True)

        # Open the file for writing the transcript
        with open(transcript_filename, 'a') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n")

            # Iterate through the channel's message history
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")

                # Handle edited messages
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")

                # Check if the message has attachments (files or images)
                if message.attachments:
                    for attachment in message.attachments:
                        # Check if the attachment is an image or a file
                        if attachment.content_type and attachment.content_type.startswith("image/"):
                            f.write(f"  - Image: [Download {attachment.filename}]({attachment.url})\n")
                        else:
                            f.write(f"  - File: [Download {attachment.filename}]({attachment.url})\n")

            # Add generation information to the transcript
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")

        # Send the transcript as a file to the user
        with open(transcript_filename, 'rb') as f:
            await interaction.user.send(f"{interaction.user.mention} wie gewünscht. Das Transkript",file=discord.File(f, f"{interaction.channel.name}.md"))

        # Remove the transcript file after sending it
        os.remove(transcript_filename)



    async def save_ticket_reasons(self, interaction: discord.Interaction, reason: str, ticket) -> None:

        if not os.path.exists(self.config.TICKET_REASONS_PATH):
            os.makedirs(self.config.TICKET_REASONS_PATH)

        with open(self.config.TICKET_REASONS_PATH + f"{interaction.user.id}-{ticket[0][:6]}-ticket_reason.txt", "a") as file:
            file.write(f"""
Ticket Infos:
Channel: {interaction.channel.name}
User: {interaction.user.name} ({interaction.user.id})
Time: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}

Ticket ID: {ticket[0]}
Ticket Kategorie: {ticket[2]}

Ticket Grund:
---------------------------------------
""" + reason + """
---------------------------------------
            """)

    @staticmethod
    async def delete_last_category(category: discord.CategoryChannel) -> None:
            if len(category.channels) == 0:
                await category.delete()

    def ticket_takeover_permission(self, interaction: discord.Interaction, ticket_user: discord.Member) -> dict:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.guild.get_role(self.config.DELTA_TEAM_ROLE_ID): discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True,
                                                          read_message_history=True, attach_files=True, manage_messages=True),

            ticket_user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, read_message_history=True, attach_files=True)
        }
        return overwrites

    def ticket_permission(self, interaction: discord.Interaction) -> dict:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.guild.get_role(self.config.DELTA_TEAM_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, read_message_history=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, read_message_history=True, attach_files=True)
        }
        return overwrites