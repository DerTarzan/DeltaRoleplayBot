import discord

from base.utils.embeds.base_embed import EmbedsBase

class EmbedTicket(EmbedsBase):
    def __init__(self):
        super().__init__()

    def create_ticket_embed(self, guild: discord.Guild, team_role: discord.Role) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket erstellen",
            description="Bitte wähle eine Kategorie aus, um ein Ticket zu erstellen:",
            color=self.INFO_COLOR
        )
        embed.add_field(
            name=f"Willkommen beim Ticket-Support von {guild.name}",
            value=f"""
            **Kategorien:**
            > ❓ Allgemein
            > 📝 Team Bewerbung
            > 🔧 Technischer Support
            > 🔓 Entbannungsantrag
            > 🏳️ Fraktionsanliegen
            > 🔗 Sonstiges
            
            Das {team_role.mention} wird sich so schnell wie möglich um dein Anliegen kümmern.
            """,
            inline=False
        )
        return self.set_standard_footer_and_author(embed, guild.icon.url)

    def ticket_disabled(self, reason: str ,icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket-System deaktiviert",
            description="Das Ticket-System wurde vorübergehend deaktiviert.",
            color=self.WARNING_COLOR
        )

        embed.add_field(
            name="Grund:",
            value=reason,
            inline=False
        )

        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_created(self, channel: discord.TextChannel, ticket) -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket erstellt",
            description="Dein Ticket wurde erfolgreich erstellt.",
            color=self.INFO_COLOR
        )
        embed.add_field(
            name="🔗 Ticket Informationen",
            value=(
                f"Kanal: {channel.mention}\n"
                f"Ticket Kategorie: {str(ticket[2])}\n"
                f"Ticket ID: `{ticket[0]}`"
            ),
            inline=False
        )
        # Standard-Footer und -Author hinzufügen
        return self.set_standard_footer_and_author(embed, channel.guild.icon.url)

    def ticket_channel_info(self, category: discord.CategoryChannel, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket Kanal",
            description=f"Du hast ein Ticket in der Kategorie `{category.name}` erstellt.",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_already_open(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket bereits geöffnet",
            description="Du hast bereits ein offenes Ticket.",
            color=self.WARNING_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def confirm_ticket_close(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket schließen",
            description="Möchtest du das Ticket wirklich schließen?",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_closed(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket geschlossen",
            description="Das Ticket wurde erfolgreich geschlossen.",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_closed_with_reason(self, reason: str, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket geschlossen",
            description="Das Ticket wurde erfolgreich geschlossen.",
            color=self.INFO_COLOR
        )
        embed.add_field(
            name="Grund:",
            value=reason,
            inline=False
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def invalid_user_id(self, user_id: int, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ungültige Benutzer-ID",
            description=f"Es wurde kein Benutzer mit der ID `{user_id}` gefunden. Bitte überprüfe die ID.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def user_offline(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Benutzer offline",
            description="Der angegebene Benutzer ist derzeit offline und kann nicht kontaktiert werden.",
            color=self.WARNING_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def no_team_role(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Keine Teamrolle",
            description="Der angegebene Benutzer ist kein Mitglied des Teams.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_forwarded(self, user: discord.User, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket weitergeleitet",
            description=f"Das Ticket wurde erfolgreich an {user.mention} weitergeleitet.",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_no_perm_forward(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Keine Berechtigung",
            description="Du hast keine Berechtigung, dieses Ticket weiterzuleiten.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def no_permission_close(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Keine Berechtigung",
            description="Du hast keine Berechtigung, dieses Ticket zu schließen.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_not_found(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket nicht gefunden",
            description="Das Ticket konnte nicht gefunden werden.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_claimed(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket beansprucht",
            description="Das Ticket wurde erfolgreich von dir beansprucht.",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_no_perm_claim(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Keine Berechtigung",
            description="Du hast keine Berechtigung, dieses Ticket zu beanspruchen.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def ticket_renamed(self, new_name: str, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Ticket umbenannt",
            description=f"Das Ticket wurde erfolgreich in `{new_name}` umbenannt.",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def no_permission_rename(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Keine Berechtigung",
            description="Du hast keine Berechtigung, dieses Ticket umzubenennen.",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def already_in_team(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🎫 Bereits im Team",
            description="Du bist bereits Mitglied des Teams und kannst keine weiteren Teamrollen übernehmen.",
            color=self.WARNING_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)
