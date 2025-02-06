import discord
from discord import slash_command
from discord.ext import commands

from base.utils.modals.checkout_modal import CheckoutModal


class Checkout(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(name="abmeldung", description="Melde dich vom Team ab")
    async def checkout(self, ctx: discord.ApplicationContext):
        await ctx.send_modal(CheckoutModal())


def setup(bot):
    bot.add_cog(Checkout(bot))