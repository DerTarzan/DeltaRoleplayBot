import discord
import uuid

from base.config import BotConfig
from base.database import Database
from base.utils.embeds.ticket_embed import EmbedTicket
from base.utils.modals.ticket_modal import TicketReasonModal, TicketForwardModal, TicketRenameModal
from base.logger import Logger
from base.utils.utilities import Utilities

class ConfirmClose(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.logger = Logger(__name__).get_logger()
        self.database = Database()

    @discord.ui.button(label="Ja ✅", style=discord.ButtonStyle.green)
    async def confirm(self, _, interaction: discord.Interaction):
        ticket = await self.database.get_ticket_by_channel_id(interaction.channel.id)
        await interaction.channel.delete()
        await self.database.remove_ticket(ticket[0])


    @discord.ui.button(label="Nein ❌", style=discord.ButtonStyle.red)
    async def cancel(self, _, interaction: discord.Interaction):
        await interaction.message.delete()


class UserButton(discord.ui.View):
    def __init__(self, bot: discord.Bot, member: discord.Member):
        super().__init__(timeout=None)
        self.bot = bot
        self.config = BotConfig()
        self.utils = Utilities()
        self.logger = Logger(__name__).get_logger()
        self.database = Database()
        self.ticket_user = member

    @discord.ui.button(label="Ticket übernehmen", style=discord.ButtonStyle.red, emoji="🔁")
    async def take_over(self, _, interaction: discord.Interaction):
        if self.utils.check_user_has_role(interaction.user, self.config.DELTA_TEAM_ROLE_ID):
            await interaction.response.send_message(embed=EmbedTicket().ticket_claimed(interaction.guild.icon.url), ephemeral=True)
            await interaction.channel.set_permisison(self.utils.ticket_takeover_permission(interaction.user, self.ticket_user))
            return
        await interaction.response.send_message(embed=EmbedTicket().ticket_no_perm_claim(interaction.guild.icon.url), ephemeral=True)


    @discord.ui.button(label="Ticket zuweisen", style=discord.ButtonStyle.red, emoji="🔀")
    async def forward(self, _, interaction: discord.Interaction):
        if self.utils.check_user_has_role(interaction.user, self.config.DELTA_TEAM_ROLE_ID):
            await interaction.response.send_modal(TicketForwardModal(interaction.guild))
            return
        await interaction.response.send_message(embed=EmbedTicket().ticket_no_perm_forward(interaction.guild.icon.url), ephemeral=True)

    @discord.ui.button(label="Umbenennen", style=discord.ButtonStyle.red, emoji="📝")
    async def rename(self, _, interaction: discord.Interaction):
        if self.utils.check_user_has_role(interaction.user, self.config.DELTA_TEAM_ROLE_ID):
            await interaction.response.send_modal(TicketRenameModal())
            return
        await interaction.response.send_message(embed=EmbedTicket().no_permission_rename(interaction.guild.icon.url), ephemeral=True)

    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.primary, emoji="🔒")
    async def close_ticket(self, _, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=EmbedTicket().confirm_ticket_close(interaction.guild.icon.url),
            view=ConfirmClose(), ephemeral=True
        )

    @discord.ui.button(label="Ticket schließen mit Grund", style=discord.ButtonStyle.secondary, emoji="📝")
    async def close_ticket_reason(self, _, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketReasonModal())

    @discord.ui.button(label="Transcript", style=discord.ButtonStyle.primary, emoji="📜")
    async def transcript(self, _, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.utils.transcript(interaction, self.bot)


class TicketDropdown(discord.ui.Select):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.logger = Logger(__name__).get_logger()
        self.database = Database()
        self.utils = Utilities()
        self.config = BotConfig()

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
                description="Erstelle ein Entbannungsantrag",
                emoji="🔓"
            ),
            discord.SelectOption(
                label="Fraktionsanliegen",
                description="Fragen oder Wünsche mit d/einer Fraktion",
                emoji="🏳️"
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

        if interaction.guild.get_role(self.config.DELTA_TEAM_ROLE_ID) in interaction.user.roles:
            await interaction.response.send_message(embed=EmbedTicket().already_in_team(interaction.guild.icon.url), ephemeral=True)
            return

        existing_ticket = await self.database.get_tickets(interaction.user.id)

        if existing_ticket:
            await interaction.response.send_message(
                embed=EmbedTicket().ticket_already_open(interaction.guild.icon.url),
                ephemeral=True
            )
            return

        category = discord.utils.get(interaction.guild.categories, name=selected_category)
        if not category:
            category = await interaction.guild.create_category(selected_category)

        ticket_uuid = str(uuid.uuid4())

        ticket_channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=self.utils.ticket_permission(interaction),
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
            await ticket_channel.send(interaction.user.mention,
                                      embed=EmbedTicket().ticket_channel_info(category, interaction.guild.icon.url),
                                      view=UserButton(self.bot, interaction.user))

            ticket = await self.database.get_ticket_by_channel_id(ticket_channel.id)
            await interaction.response.send_message(
                embed=EmbedTicket().ticket_created(ticket_channel, ticket),
                ephemeral=True
            )

        except Exception as e:
            self.logger.error(f"Fehler beim Senden der Nachricht im Ticket-Kanal: {e}")
            await interaction.response.send_message(
                "Dein Ticket wurde erstellt, aber eine Nachricht konnte nicht gesendet werden.",
                ephemeral=True
            )
            raise e

        view = TicketView(self.bot)
        await interaction.message.edit(view=view)
        await interaction.delete_original_response(delay=10)


class TicketView(discord.ui.View):
    def __init__(self, bot: discord.Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(TicketDropdown(self.bot))
