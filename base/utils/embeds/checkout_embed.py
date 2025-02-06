import discord
from base.utils.embeds.base_embed import EmbedsBase

class CheckoutEmbed(EmbedsBase):
    def __init__(self):
        super().__init__()

    def checkout_embed(self, username: discord.Member, reason, duration):
        embed = discord.Embed(
            title="Abmeldung",
            description="Abmeldung eines Teammitglieds",
            color=self.INFO_COLOR
        )

        embed.add_field(name="Abgemeldet von", value=username.mention, inline=False)
        embed.add_field(name="Grund", value=reason, inline=False)
        embed.add_field(name="Dauer", value="Bis zum: " + duration, inline=False)

        embed.set_thumbnail(url=username.avatar.url)

        return embed