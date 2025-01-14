import discord
from datetime import datetime


class EmbedsBase:
    # Standardfarben für Embeds
    MAIN_COLOR = discord.Color.from_rgb(96, 233, 176)  # Türkis
    INFO_COLOR = discord.Color.from_rgb(0, 255, 0)     # Grün
    ERROR_COLOR = discord.Color.from_rgb(255, 0, 0)    # Rot
    WARNING_COLOR = discord.Color.from_rgb(255, 255, 0)  # Gelb

    def __init__(self):
        # Automatisch das aktuelle Jahr setzen
        self.year = datetime.now().year

    def set_standard_footer_and_author(self, embed: discord.Embed, icon_url: str = "") -> discord.Embed:
        if icon_url.startswith("http"):
            embed.set_author(name="DeltaRoleplayBot 🤖", icon_url=icon_url)
        else:
            embed.set_author(name="DeltaRoleplayBot 🤖")

        embed.set_footer(text=f"DeltaRoleplayBot | © {self.year}")
        return embed