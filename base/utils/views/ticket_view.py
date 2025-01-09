import discord
import uuid
from base.database import Database
from base.utils.utilities import Utilities
from base.utils.embeds.ticket_embed import EmbedTicket
from base.logger import Logger


class TicketManager(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.logger = Logger(__name__).get_logger()
        self.database = Database()

    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.primary)
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        ticket_uuid = await self.database.get_ticket_by_channel_id(interaction.channel.id)
        ticket = await self.database.get_ticket(ticket_uuid[0])

        if not ticket:
            await interaction.response.send_message("Das Ticket konnte nicht gefunden werden.", ephemeral=True)
            return

        if interaction.user.id != ticket[1]:
            await interaction.response.send_message("Du kannst nur dein eigenes Ticket schließen.", ephemeral=True)
            return

        try:
            await interaction.channel.delete()
            await self.database.remove_ticket(ticket_uuid[0])
        except Exception as e:
            self.logger.error(f"Fehler beim Schließen des Tickets: {e}")
            await interaction.response.send_message("Ein Fehler ist beim Schließen des Tickets aufgetreten.", ephemeral=True)

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        self.logger = Logger(__name__).get_logger()
        self.database = Database()

        options = [
            discord.SelectOption(
                label="Allgemein",
                description="Allgemeine Fragen und Probleme",
                emoji="❓"
            ),
            discord.SelectOption(
                label="Team Bewerbung",
                description="Erstelle ein Ticket, um dich zu bewerben",
                emoji="📝"
            ),
            discord.SelectOption(
                label="Technischer Support",
                description="Probleme mit Mods (Grafik), Server, etc.",
                emoji="🔧"
            ),
            discord.SelectOption(
                label="Entbannungsantrag",
                description="Erstelle ein Ticket, um einen Entbannungsantrag zu stellen",
                emoji="🔓"
            ),
            discord.SelectOption(
                label="Fraktionsanliegen",
                description="Fragen oder Wünsche mit d/einer Fraktion",
            ),
            discord.SelectOption(
                label="Sonstiges",
                description="Alles, was nicht in die anderen Kategorien passt",
                emoji="🔗"
            ),
        ]

        super().__init__(
            placeholder="Bitte wähle eine Kategorie aus",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        selected_category = self.values[0]

        existing_ticket = await self.database.get_tickets(interaction.user.id)
        if existing_ticket:
            await interaction.response.send_message("Du hast bereits ein Ticket erstellt.", ephemeral=True)
            return

        category = discord.utils.get(interaction.guild.categories, name=selected_category)
        if not category:
            category = await interaction.guild.create_category(selected_category)

        ticket_uuid = str(uuid.uuid4())

        ticket_channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True),
            },
            topic=f"Ticket von {interaction.user.name} | Kategorie: {selected_category}",
        )

        try:
            await self.database.add_ticket(
                uuid=ticket_uuid,
                user_id=interaction.user.id,
                category=selected_category,
                channel_id=ticket_channel.id,
                guild_id=interaction.guild.id,
            )
            self.logger.info(f"Ticket {ticket_uuid} erfolgreich erstellt und gespeichert.")
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern des Tickets: {e}")
            await interaction.response.send_message(
                "Ein Fehler ist beim Erstellen deines Tickets aufgetreten. Bitte versuche es später erneut.",
                ephemeral=True
            )
            return

        try:
            await ticket_channel.send(interaction.user.mention, embed=EmbedTicket().ticket_channel_embed(interaction.guild.icon.url, category), view=TicketManager())
            await interaction.response.send_message(
                embed=EmbedTicket().ticket_created_embed(ticket_channel, ticket_uuid),
                ephemeral=True
            )
        except Exception as e:
            self.logger.error(f"Fehler beim Senden der Nachricht im Ticket-Kanal: {e}")
            await interaction.response.send_message(
                "Dein Ticket wurde erstellt, aber eine Nachricht konnte nicht gesendet werden.",
                ephemeral=True
            )


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())
