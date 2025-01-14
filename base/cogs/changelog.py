import discord
from discord import slash_command
from discord.ext import commands
from base.utils.embeds.changelog_embed import ChangelogEmbed

class Changelog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(name="changelog", description="Sendet den Changelog")
    async def changelog(self, ctx: discord.ApplicationContext):
        await ctx.respond("Changelog wird gesendet", ephemeral=True)
        await ctx.send(embed=ChangelogEmbed().changelog_embed())


def setup(bot):
    bot.add_cog(Changelog(bot))