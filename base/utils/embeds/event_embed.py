import discord

from base.utils.embeds.base_embed import EmbedsBase

class EmbedEvent(EmbedsBase):
    def __init__(self):
        super().__init__()

    def welcome_embed(self, guild: discord.Guild, member: discord.Member, verify_channel: discord.TextChannel, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🛬 Willkommen",
            description=f"Willkommen {member.mention} auf {guild.name}.",
            color=self.INFO_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name=" ", value=f"Bitte verifiziere dich in {verify_channel.mention}", inline=False)

        return self.set_standard_footer_and_author(embed, icon)

    def rules_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="📜 Regelwerk",
            description="Bitte lese dir die Regeln durch",
            color=self.INFO_COLOR
        )
        embed.set_thumbnail(url=icon)

        embed.add_field(
            name="            ",
            value="            ",
            inline=False
        )

        embed.add_field(
            name="📜 **Regeln**",
            value="Halte dich bitte an die [Discord TOS](https://discord.com/terms).",
            inline=False
        )


        return self.set_standard_footer_and_author(embed, icon)

    def kick_embed(self, member: discord.Member, reason: str, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="👢 Kick",
            description=f"{member.mention} wurde gekickt.",
            color=self.ERROR_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name="Grund", value=reason, inline=False)

        return self.set_standard_footer_and_author(embed, icon)