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


def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))