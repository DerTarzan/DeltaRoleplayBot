import discord
from discord import slash_command

from discord.ext import commands
from base.config import BotConfig
from base.database import Database

from base.utils.embeds.ticket_embed import EmbedTicket
from base.utils.views.ticket_view import TicketView

from base.utils.modals.ticket_modal import TicketSystemCloseModal

class TicketSystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.config = BotConfig()
        self.database = Database()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.config.TICKET_CHANNEL_ID)
        await channel.purge(limit=1)
        await channel.send(embed=EmbedTicket().create_ticket_embed(channel.guild, channel.guild.get_role(self.config.DELTA_TEAM_ROLE_ID)), view=TicketView(self.bot))


    @slash_command(name="disable-ticket", description="Deaktiviere das Ticket-System")
    async def disable_ticket(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("Du hast keine Berechtigung, dieses Command auszuführen.")

        await ctx.send_modal(TicketSystemCloseModal(self.bot))

    @slash_command(name="enable-ticket", description="Aktiviere das Ticket-System")
    async def enable_ticket(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("Du hast keine Berechtigung, dieses Command auszuführen.")

        channel = self.bot.get_channel(self.config.TICKET_CHANNEL_ID)
        await channel.purge(limit=1)
        await channel.send(embed=EmbedTicket().create_ticket_embed(channel.guild, channel.guild.get_role(self.config.DELTA_TEAM_ROLE_ID)), view=TicketView(self.bot))
        await ctx.respond("Das Ticket-System wurde erfolgreich aktiviert.", ephemeral=True, delete_after=5)


def setup(bot):
    bot.add_cog(TicketSystem(bot))