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

        await welcome_channel.send(embed=EmbedEvent().welcome_embed(member.guild, member, verify_channel))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        if not await self.database.check_user(member.id):
            return

        await self.database.remove_user(member.id, member.name)

    @commands.Cog.listener()
    async def on_ready(self):
        button = discord.ui.Button(style=discord.ButtonStyle.link, label="Regelwerk", url="https://deltaroleplay.de/routes/regelwerk.html")
        view = discord.ui.View()
        view.add_item(button)
        rules_channel = self.bot.get_channel(self.config.RULES_CHANNEL_ID)
        await rules_channel.purge(limit=1)
        await rules_channel.send(embed=EmbedEvent().rules_embed(self.bot.guilds[0].icon.url), view=view)


        button = discord.ui.Button(style=discord.ButtonStyle.link, label="Connect", url="https://cfx.re/join/g96edx")
        view = discord.ui.View()
        view.add_item(button)
        channel = self.bot.get_channel(self.config.INFO_CHANNEL_ID)
        await channel.purge(limit=1)
        await channel.send(embed=EmbedEvent().info_embed(self.bot.guilds[0].icon.url), view=view)


def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))