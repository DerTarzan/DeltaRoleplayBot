import discord

from base.utils.embeds.base_embed import EmbedsBase
from base.utils.utilities import Utilities


class ChangelogEmbed(EmbedsBase):
    def __init__(self):
        super().__init__()
        self.utils = Utilities()

    def changelog_embed(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(title="Changelog", description="Die neuesten Änderungen", color=discord.Color.blurple())

        if icon_url:
            embed.set_thumbnail(url=icon_url)

        changelog_data = self.utils.load_changelog()

        for section, entries in changelog_data.items():
            if entries:
                changelog_str = "\n".join([f"{key}: {value}" for key, value in entries.items()])
                embed.add_field(name=section, value=f"```{changelog_str}```", inline=False)

        embed.set_footer(text=f"DeltaRoleplayBot | © {self.now}")

        return embed