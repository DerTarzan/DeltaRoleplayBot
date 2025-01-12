import discord

from discord.ext import commands
from base.config import BotConfig
from base.database import Database

from base.utils.embeds.ticket_embed import EmbedTicket
from base.utils.views.ticket_view import TicketView

class TicketSystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.config = BotConfig()
        self.database = Database()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.config.TICKET_CHANNEL_ID)
        await channel.purge(limit=1)
        await channel.send(embed=EmbedTicket().ticket_embed(channel.guild, channel.guild.get_role(self.config.DELTA_TEAM_ROLE_ID), channel.guild.icon.url), view=TicketView(self.bot))


def setup(bot):
    bot.add_cog(TicketSystem(bot))