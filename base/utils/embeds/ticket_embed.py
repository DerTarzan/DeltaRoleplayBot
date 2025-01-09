import discord

from base.utils.embeds.base_embed import EmbedsBase

class EmbedTicket(EmbedsBase):
    def __init__(self):
        super().__init__()

    def ticket_embed(self, guild: discord.Guild, team: discord.Role , icon: str, ) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket erstellen",
            description="Bitte wähle eine Kategorie aus, um ein Ticket zu erstellen",
            color=self.INFO_COLOR
        )

        embed.add_field(
            name=f"Willkommen beim TicketSupport von {guild.name}",
            value=f"""
            
            **Kategorien:**
            > Allgemein
            > Team Bewerbung
            > Technischer Support
            > Entbannungsantrag
            > Fraktionsanliegen
            > Sonstiges
            
            Das {team.mention} wird sich so schnell wie möglich um dein Anliegen kümmern.
            
            """
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_created_embed(self, channel: discord.TextChannel, ticket_uuid: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket erstellt",
            description="Dein Ticket wurde erfolgreich erstellt",
            color=self.INFO_COLOR
        )

        embed.add_field(
            name="🔗 Ticket Link",
            value=f"channel: {channel.mention}\nTicket ID: {ticket_uuid}"
        )

        return self.set_standard_footer_and_author(embed, channel.guild.icon.url)

    def ticket_channel_embed(self, icon: str, category: discord.Option) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Kanal",
            description=f"Du hast ein Ticket erstellt: {category.name}",
            color=self.INFO_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)