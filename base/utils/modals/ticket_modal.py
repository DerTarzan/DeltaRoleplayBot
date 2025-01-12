import asyncio

import discord

from base.utils.embeds.ticket_embed import EmbedTicket


class TicketReasonModal(discord.ui.Modal):
    def __init__(self):
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

        await interaction.response.send_message(embed=EmbedTicket().ticket_close_by_reason_embed(interaction.guild.icon.url, reason), ephemeral=True)
        await asyncio.sleep(2)
        await interaction.channel.delete()

class TicketForwardModal(discord.ui.Modal):
    def __init__(self, guild: discord.Guild):
        super().__init__(title="Ticket Weiterleitung", timeout=60)
        self.guild = guild
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
                embed=EmbedTicket().ticket_invalid_id_embed(interaction.guild.icon.url),
                ephemeral=True
            )
            return

        member = self.guild.get_member(user_id)
        if not member:
            await interaction.response.send_message(
                embed=EmbedTicket().ticket_invalid_userid_embed(user_id, interaction.guild.icon.url),
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=EmbedTicket().ticket_forwarded_embed(interaction.guild.icon.url, member),
            ephemeral=True
        )

        await interaction.channel.set_permissions(member, read_messages=True, send_messages=True, view_channel=True)