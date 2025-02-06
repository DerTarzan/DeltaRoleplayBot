import discord

from base.utils.embeds.base_embed import EmbedsBase
from base.utils.utilities import Utilities


class EmbedEvent(EmbedsBase):
    def __init__(self):
        self.utils = Utilities()
        super().__init__()

    def welcome_embed(self, guild: discord.Guild, member: discord.Member, verify_channel: discord.TextChannel) -> discord.Embed:
        embed = discord.Embed(
            title="🛬 Willkommen",
            description=f"Willkommen {member.mention} auf {guild.name}.",
            color=self.INFO_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name=" ", value=f"Bitte verifiziere dich in {verify_channel.mention}", inline=False)

        return self.set_standard_footer_and_author(embed, guild.icon.url)

    def rules_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="📜 **Regelwerk**",
            description="**Bitte lese dir die Regeln durch, um sicherzustellen, dass du die Community-Richtlinien verstehst und einhältst.**\n\n",
            color=self.INFO_COLOR
        )

        # Wichtige Hinweise
        embed.add_field(
            name="📌 **Wichtige Hinweise**",
            value=(
                "• Halte dich bitte an die [Discord TOS](https://discord.com/terms). \n"
                "• Lese dir das komplette Regelwerk durch: [Regelwerk lesen](https://deltaroleplay.de/routes/regelwerk.html).\n"
            ),
            inline=False
        )

        # Fragen oder Unsicherheiten
        embed.add_field(
            name="❓ **Fragen oder Unsicherheiten?**",
            value=(
                "Bei Fragen zum Regelwerk oder Unklarheiten kannst du dich jederzeit an ein Teammitglied wenden.\n\n"
            ),
            inline=False
        )

        embed.set_image(url="https://i.ibb.co/Mk3hGRy/banner-delta-klein.png")

        return self.set_standard_footer_and_author(embed)

    def timeout_embed(self, member: discord.Member, reason: str, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="👢 Timeout",
            description=f"{member.mention} wurde in den Timeout geschickt.",
            color=self.ERROR_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name="Grund", value=reason, inline=False)

        return self.set_standard_footer_and_author(embed, icon_url)

    def info_embed(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="📰 Informationen",
            description="**Willkommen auf unserem" 
                        " Discord-Server. Hier findest du alle wichtigen Informationen über unseren Server.**",
            color=self.INFO_COLOR
        )
        embed.set_image(url="https://i.ibb.co/Mk3hGRy/banner-delta-klein.png")

        embed.add_field(
            name="🔗 **Nützliche Links**",
            value=(
                "• [Regelwerk](http://176.96.138.31/routes/regelwerk.html )\n"

            ),
            inline=False
        )


        return self.set_standard_footer_and_author(embed, icon_url)
