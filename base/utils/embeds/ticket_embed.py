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

    def ticket_already_open_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket bereits offen",
            description="Du hast bereits ein Ticket offen.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_confirm_close_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket schließen",
            description="Möchtest du das Ticket wirklich schließen?",
            color=self.INFO_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_close_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket schließen",
            description="Das Ticket wurde geschlossen.",
            color=self.INFO_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_close_by_reason_embed(self, icon: str,reason: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket geschlossen",
            description=f"Das Ticket wurde geschlossen.",
            color=self.INFO_COLOR
        )

        embed.add_field(
            name="Grund",
            value=reason
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_invalid_id_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Weiterleitung",
            description="Die eingegebene User-ID ist ungültig.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_invalid_userid_embed(self, id: int, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Weiterleitung",
            description=f"Kein Benutzer mit der ID `{id}` konnte gefunden werden. Bitte überprüfe die User-ID.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_forwarded_embed(self, icon: str, user: discord.User) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket weitergeleitet",
            description=f"Das Ticket wurde erfolgreich an {user.mention} weitergeleitet.",
            color=self.INFO_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_cannot_close_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket schließen",
            description="Du kannst das Ticket nicht schließen.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_closed_error_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket schließen",
            description="Das Ticket konnte nicht geschlossen werden. Es ist ein fehler aufgetreten.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_claimed_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Anspruch",
            description="Du hast dieses Ticket übernommen.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_not_found_embed(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket nicht gefunden",
            description="Das Ticket konnte nicht gefunden werden.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_no_perm_claim(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Anspruch",
            description="Du hast keine Berechtigung dieses Ticket zu übernehmen.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)

    def ticket_no_perm_forward(self, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Weiterleitung",
            description="Du hast keine Berechtigung dieses Ticket weiterzuleiten.",
            color=self.ERROR_COLOR
        )

        return self.set_standard_footer_and_author(embed, icon)