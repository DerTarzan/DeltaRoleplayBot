import datetime
from collections import defaultdict

import discord
from discord.ext import commands

from base.config import BotConfig
from base.database import Database

from base.utils.embeds.event_embed import EmbedEvent
from base.utils.utilities import Utilities


class Events(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.utils = Utilities()
        self.config = BotConfig()
        self.database = Database()
        self.message_count = defaultdict(list)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = self.bot.get_channel(self.config.WELCOME_CHANNEL_ID)
        verify_channel = self.bot.get_channel(self.config.VERIFY_CHANNEL_ID)

        if member.bot:
            await self.utils.ban_bot(member)

        await welcome_channel.send(embed=EmbedEvent().welcome_embed(member.guild, member, verify_channel, member.guild.icon.url))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        if not await self.database.check_user(member.id):
            return

        await self.database.remove_user(member.id)

    @commands.Cog.listener()
    async def on_ready(self):
        rules_channel = self.bot.get_channel(self.config.RULES_CHANNEL_ID)
        await rules_channel.purge(limit=1)
        await rules_channel.send(embed=EmbedEvent().rules_embed(self.bot.guilds[0].icon.url))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id == self.config.ID_CHANNEL_ID:
            if not message.content == ".":
                await message.delete()

        # Nachrichten-Tracking für Spam-Erkennung
        now = datetime.datetime.now()
        user_id = message.author.id
        self.message_count[user_id].append(now)

        # Nur die letzten 5 Sekunden berücksichtigen
        self.message_count[user_id] = [
            timestamp for timestamp in self.message_count[user_id]
            if now - timestamp <= datetime.timedelta(seconds=5)
        ]

        # Kick den User, wenn er mehr als 10 Nachrichten in 5 Sekunden sendet
        if len(self.message_count[user_id]) > 10:
            try:
                await message.author.kick(reason="Spamming: Mehr als 10 Nachrichten in 5 Sekunden.")
                await message.channel.purge(limit=11)
                await message.channel.send(embed=EmbedEvent().kick_embed(message.author, "Spamming: Mehr als 10 Nachrichten in 5 Sekunden.", message.author.avatar.url), delete_after=10)
            except discord.Forbidden:
                return
            finally:
                # Nachrichten-Tracking des Users zurücksetzen
                del self.message_count[user_id]


def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))