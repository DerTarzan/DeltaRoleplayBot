import os

import discord
from discord import Button
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.bridge import has_permissions
from discord.ui import View

from base.config import BotConfig
from base.database import Database
from base.utils.embeds.clear_embed import EmbedClear


class Moderation(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.database = Database()
        self.config = BotConfig()

    @slash_command(name="clear", description="Löscht eine bestimmte Anzahl von Nachrichten")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx: discord.ApplicationContext, amount: int = 1):
        await ctx.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)
        await ctx.respond(embed=EmbedClear().clear_embed(amount, ctx.guild.icon.url), ephemeral=True)

    @slash_command(name="clear_all", description="Löscht alle Nachrichten")
    @has_permissions(manage_messages=True)
    async def clear_all(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        if self.config.DEV_MODE:
            await ctx.respond("Dieser Befehl ist nur für den DEV_MODUS", ephemeral=True)
            return


        total_deleted = 0

        for channel in ctx.guild.text_channels:
            try:
                deleted = await channel.purge(check=lambda m: not m.pinned)
                total_deleted += len(deleted)
            except discord.Forbidden as e:
                await ctx.respond(f"Es ist ein Fehler aufgetreten : {e}")

        await ctx.respond(embed=EmbedClear().clear_all_embed(total_deleted, ctx.guild.icon.url), ephemeral=True)

    @slash_command(name="add_users", description="Fügt alle Mitglieder zur Datenbank hinzu")
    @has_permissions(administrator=True)
    async def add_users(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        for member in ctx.guild.members:
            if member.bot:
                continue
            await self.database.add_user(member.id, member.name, member.discriminator)

        await ctx.respond("Alle Mitglieder wurden zur Datenbank hinzugefügt", ephemeral=True)

    @clear.error
    async def clear_error(self, ctx: discord.ApplicationContext, error):

        embed = EmbedClear().clear_error_embed(error, ctx.guild.icon.url)

        file = "error_log.txt"
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(error))

        with open(file, "rb") as f:
            await ctx.respond(file=discord.File(f, "error_log.txt"), embed=embed)

        os.remove(file)

    @clear_all.error
    async def clear_all_error(self, ctx: discord.ApplicationContext, error):
        embed = EmbedClear().clear_error_embed(error, ctx.guild.icon.url)

        file = "error_log.txt"
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(error))

        with open(file, "rb") as f:
            await ctx.respond(file=discord.File(f, "error_log.txt"), embed=embed)

        os.remove(file)

def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))
