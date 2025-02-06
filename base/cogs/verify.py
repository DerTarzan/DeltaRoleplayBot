import discord

from discord.ext import commands
from base.config import BotConfig
from base.database import Database

from base.utils.views.verify_view import VerifyButton
from base.utils.embeds.verify_embed import EmbedVerify

class VerifySystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.config = BotConfig()
        self.database = Database()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.config.VERIFY_CHANNEL_ID)
        rule_channel = self.bot.get_channel(self.config.RULES_CHANNEL_ID)
        await channel.purge(limit=1)
        await channel.send(embed=EmbedVerify().verify_embed(rule_channel), view=VerifyButton(self.bot))

def setup(bot):
    bot.add_cog(VerifySystem(bot))