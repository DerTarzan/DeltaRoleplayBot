import discord

from base.config import BotConfig
from base.database import Database
from base.utils.embeds.ticket_embed import EmbedTicket
from base.utils.utilities import Utilities


class TicketReasonModal(discord.ui.Modal):
    def __init__(self):
        self.utils = Utilities()
        self.database = Database()
        super().__init__(title="Ticket Grund", timeout=60)

        self.reason = discord.ui.InputText(
            label="Grund",
            placeholder="Bitte gebe einen Grund für dein Ticket an",
            required=True,
            max_length=200
        )
        self.add_item(self.reason)

    async def callback(self, interaction: discord.Interaction):
        name = interaction.user.name
        reason = self.reason.value

        await interaction.response.send_message(embed=EmbedTicket().ticket_closed_with_reason(interaction.guild.icon.url, reason), ephemeral=True)
        await self.utils.dm_transcript(interaction, name)
        await interaction.channel.delete()

        ticket = await self.database.get_ticket_by_channel_id(interaction.channel.id)
        await self.database.remove_ticket(ticket[0])

        await self.utils.save_ticket_reasons(interaction, reason, ticket)

        await self.utils.delete_last_category(interaction.channel.category)

class TicketForwardModal(discord.ui.Modal):
    def __init__(self, guild: discord.Guild):
        super().__init__(title="Ticket Weiterleitung", timeout=60)
        self.guild = guild
        self.config = BotConfig()
        self.forward = discord.ui.InputText(
            label="User-ID",
            placeholder="Bitte gebe die User-ID an, an die das Ticket weitergeleitet werden soll",
            required=True,
            max_length=18
        )
        self.add_item(self.forward)

    async def callback(self, interaction: discord.Interaction):
        user_id = self.forward.value

        try:
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                embed=EmbedTicket().invalid_user_id(user_id, interaction.guild.icon.url),
                ephemeral=True
            )
            return

        member = self.guild.get_member(user_id)
        if not member:
            await interaction.response.send_message(
                embed=EmbedTicket().invalid_user_id(user_id, interaction.guild.icon.url),
                ephemeral=True
            )
            return

        if member.bot:
            await interaction.response.send_message(
                embed=EmbedTicket().invalid_user_id(user_id, interaction.guild.icon.url),
                ephemeral=True
            )
            return

        if member.status == discord.Status.offline:
            await interaction.response.send_message(
                embed=EmbedTicket().user_offline(interaction.guild.icon.url),
                ephemeral=True
            )
            return

        if member.guild.get_role(self.config.DELTA_TEAM_ROLE_ID) in member.roles:
            await interaction.response.send_message(
                embed=EmbedTicket().no_team_role(interaction.guild.icon.url),
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=EmbedTicket().ticket_forwarded(interaction.guild.icon.url, member),
            ephemeral=True
        )

        await interaction.channel.set_permissions(member, read_messages=True, send_messages=True, view_channel=True)

class TicketRenameModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Ticket umbenennen", timeout=60)
        self.new_name = discord.ui.InputText(
            label="Neuer Name",
            placeholder="Bitte gebe den neuen Namen für das Ticket an",
            required=True,
            max_length=100
        )
        self.add_item(self.new_name)

    async def callback(self, interaction: discord.Interaction):
        await interaction.channel.edit(name=self.new_name.value)
        await interaction.response.send_message(embed=EmbedTicket().ticket_renamed(self.new_name.value, interaction.guild.icon.url), ephemeral=True)

class TicketSystemCloseModal(discord.ui.Modal):
    def __init__(self, bot: discord.Bot):
        self.config = BotConfig()
        self.bot = bot
        super().__init__(title="Ticket schließen", timeout=60)

        self.reason = discord.ui.InputText(
            label="Grund",
            placeholder="Bitte gebe einen Grund für das Schließen des TicketSystem an",
            required=True,
            max_length=200
        )
        self.add_item(self.reason)

    async def callback(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(self.config.TICKET_CHANNEL_ID)
        await channel.purge(limit=1)
        await channel.send(embed=EmbedTicket().ticket_disabled(self.reason.value, interaction.guild.icon.url))
        await interaction.response.send_message("Das Ticket-System wurde erfolgreich deaktiviert.", ephemeral=True)