import os
import asyncio
import discord

from base.database import Database
from base.logger import Logger
from base.config import BotConfig
from base.utils.manager import Manager
from base.utils.utilities import Utilities

logger = Logger(__name__).get_logger()


class Bot(discord.Bot):
    def __init__(self):
        self.config = BotConfig()
        self.utils = Utilities()
        self.manger = Manager()
        self.database = Database()
        super().__init__(intents=discord.Intents.all())

    def load_cogs(self, directory: str, is_root: bool = True) -> None:
        if is_root:
            logger.info("📦 Loading Cogs...")

        for filename in os.listdir(directory):
            if os.path.isdir(f'{directory}/{filename}'):
                self.load_cogs(f'{directory}/{filename}', is_root=False)
            elif filename.endswith('.py'):
                try:
                    self.load_extension(f'{directory.replace("/", ".")}.{filename[:-3]}')
                    logger.info(f'- ✅ Loaded Cog: {directory}/{filename}')
                except Exception as e:
                    logger.error(f'❌ Failed to load cog {filename}: {e}')
        if is_root:
            logger.info("🎉 All Cogs Loaded Successfully.")

    def create_coroutine_task(self, *coros) -> None:
        for coro in coros:
            if asyncio.iscoroutine(coro):
                logger.info(f" - ⚙️ Creating task for {coro.__name__}...")
                self.loop.create_task(coro)
            else:
                logger.error(f"❌ Invalid task: {coro} is not a coroutine.")

    async def on_ready(self) -> None:
        logger.info("=" * 50)
        logger.info(f"🤖 Bot Name      : {self.user.name}")
        logger.info(f"🆔 Bot ID        : {self.user.id}")
        logger.info(f"🏓 Latency       : {round(self.latency * 1000)} ms")
        logger.info("=" * 50)
        logger.info(f"🏰 Guild Name    : {self.guilds[0].name}")
        logger.info(f"🆔 Guild ID      : {self.guilds[0].id}")
        logger.info(f"👥 Member Count  : {self.guilds[0].member_count}")
        logger.info(
            f"👑 Owner         : {self.guilds[0].owner.name}#{self.guilds[0].owner.discriminator}, ID: {self.guilds[0].owner.id}")

        logger.info("-" * 50)

        logger.info("🔧 Creating presence update task...")
        self.create_coroutine_task(
            self.presence(),
            self.database.create_database(),
            self.manger.server_channel_total_members(self),
            self.manger.server_channel_restarter(self),
            self.manger.server_channel_status(self)
        )

        logger.info("-" * 50)
        logger.info("Delta Roleplay Bot is now online. 🚀")

    async def presence(self) -> None:
        while True:
            players = self.utils.server_players()
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=players))
            await asyncio.sleep(60)