import discord

from base.database import Database
from base.utils.utilities import Utilities
from base.utils.embeds.verify_embed import EmbedVerify


class VerifyButton(discord.ui.View):
    def __init__(self, bot: discord.Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.database = Database()
        self.utils = Utilities()

    @discord.ui.button(label="🔒 Verifizierung", style=discord.ButtonStyle.green)
    async def verify(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.utils.config.EINWOHNER_ROLE_ID)
        user = await self.utils.check_user_account(interaction.user)
        channel = self.bot.get_channel(self.utils.config.SUPPORT_WAITING_CHANNEL_ID)
        try:
            if await self.database.check_user(interaction.user.id):
                await interaction.response.send_message(
                    embed=EmbedVerify().verify_already_verified_embed(interaction.guild.icon.url),
                    ephemeral=True
                )
                return

            if user is False:
                await interaction.response.send_message(
                    embed=EmbedVerify().verify_failed_credentials_embed(interaction.guild.icon.url, channel),
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                embed=EmbedVerify().verify_success_embed(interaction.guild.icon.url),
                ephemeral=True
            )

            await interaction.user.add_roles(role, reason="Verifizierung erfolgreich")

            await self.database.add_user(interaction.user.id, interaction.user.name, interaction.user.discriminator)


        except Exception as e:
            await interaction.response.send_message(embed=EmbedVerify().verify_error_embed(interaction.guild.icon.url, e, channel),
                                                    ephemeral=True)


