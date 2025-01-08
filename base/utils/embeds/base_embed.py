import discord
from datetime import datetime

class EmbedsBase:
    MAIN_COLOR = discord.Color.from_rgb(96, 233, 176)
    INFO_COLOR = discord.Color.from_rgb(0, 255, 0)
    ERROR_COLOR = discord.Color.from_rgb(255, 0, 0)

    def __init__(self):
        self.year = datetime.now().year

    def set_standard_footer_and_author(self, embed: discord.Embed, thumbnail: str) -> discord.Embed:
        embed.set_author(name="DeltaRoleplayBot 🤖", icon_url=thumbnail)
        embed.set_footer(text=f"DeltaRoleplayBot | © {self.year}")
        return embed
