import asyncio
import discord
from discord.errors import Forbidden, HTTPException, NotFound

from base.logger import Logger
from base.config import BotConfig
from base.utils.utilities import Utilities

logger = Logger(__name__).get_logger()

class Manager:
    def __init__(self):
        self.config = BotConfig()
        self.utils = Utilities()

    async def server_channel_status(self, bot: discord.Bot):
        channel_status = bot.get_channel(self.config.SERVER_STATUS_CHANNEL_ID)

        guild = channel_status.guild
        owner = guild.owner

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),  # Alle anderen Mitglieder dürfen den Channel nicht betreten
            owner: discord.PermissionOverwrite(read_messages=True),  # Der Eigentümer darf den Channel betreten
        }

        await channel_status.edit(overwrites=overwrites)
        logger.info(f"Berechtigungen für den Channel {channel_status.name} gesetzt.")

        last_status = None
        while True:
            try:
                current_status = self.utils.check_server_status()

                if current_status != last_status:
                    logger.info(f"Server status updated to: {current_status}")
                    await channel_status.edit(name=f"{current_status}")
                    logger.info(f"Server status wurde erfolgreich aktualisiert.")
                    last_status = current_status
                await asyncio.sleep(2)

            except (Forbidden, HTTPException, NotFound) as e:
                logger.error(f"Error while editing channel: {e}")
                await asyncio.sleep(10)

    async def server_channel_restarter(self, bot: discord.Bot):
        channel_restart = bot.get_channel(self.config.SERVER_RESTART_CHANNEL_ID)

        guild = channel_restart.guild
        owner = guild.owner

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),  # Alle anderen Mitglieder dürfen den Channel nicht betreten
            owner: discord.PermissionOverwrite(read_messages=True),  # Der Eigentümer darf den Channel betreten
        }

        await channel_restart.edit(overwrites=overwrites)
        logger.info(f"Berechtigungen für den Channel {channel_restart.name} gesetzt.")

        last_restart_time = None  # Track the last restart time to avoid redundant updates

        while True:
            try:
                restarter = self.utils.get_restarter_schedule()

                if restarter is None:
                    await channel_restart.edit(name="Kein Restart geplant")
                    logger.info("No restart scheduled")
                    last_restart_time = None

                if restarter != last_restart_time:
                    await channel_restart.edit(name=f"Restart um {restarter} Uhr")
                    logger.info(f"Restart schedule updated to: {restarter}")
                    last_restart_time = restarter

                await asyncio.sleep(120)

            except (Forbidden, HTTPException, NotFound) as e:
                logger.error(f"Error while editing channel: {e}")
                await asyncio.sleep(10)

    async def server_channel_total_members(self, bot: discord.Bot):
        channel_total_members = bot.get_channel(self.config.SERVER_MEMBERS_CHANNEL_ID)

        guild = channel_total_members.guild
        owner = guild.owner

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),  # Alle anderen Mitglieder dürfen den Channel nicht betreten
            owner: discord.PermissionOverwrite(read_messages=True),  # Der Eigentümer darf den Channel betreten
        }

        # Berechtigungen anwenden
        await channel_total_members.edit(overwrites=overwrites)
        logger.info(f"Berechtigungen für den Channel {channel_total_members.name} gesetzt.")

        last_member_count = None  # Track the last member count to avoid redundant updates

        while True:
            try:
                current_member_count = channel_total_members.guild.member_count

                if current_member_count != last_member_count:
                    await channel_total_members.edit(name=f"Total Members: {current_member_count - 1}")
                    logger.info(f"Total members updated to: {current_member_count}")
                    last_member_count = current_member_count  # Update last member count
                await asyncio.sleep(3600)

            except (Forbidden, HTTPException, NotFound) as e:
                logger.error(f"Error while editing channel: {e}")
                await asyncio.sleep(10)  # Wait a bit before retrying to avoid spam on errors
