import discord
from datetime import datetime
from discord.ext import tasks

from base.database import Database
from base.utils.utilities import Utilities
from base.utils.embeds.checkout_embed import CheckoutEmbed

class CheckoutModal(discord.ui.Modal):
    def __init__(self):
        self.utils = Utilities()
        self.database = Database()
        super().__init__(title="Checkout", timeout=None)

        self.reason = discord.ui.InputText(
            label="Warum meldest du dich ab?",
            placeholder="Bitte gebe einen Grund für deine Abmeldung an",
            required=True,
            max_length=200
        )
        self.duration = discord.ui.InputText(
            label="Bis wann bist du abwesend?",
            placeholder="dd/mm/yyyy",
            required=True,
            max_length=10
        )

        self.add_item(self.reason)
        self.add_item(self.duration)

    async def callback(self, interaction: discord.Interaction):
        reason = self.reason.value
        duration_str = self.duration.value
        try:
            end_date = datetime.strptime(duration_str, "%d/%m/%Y")
            now = datetime.now()

            if end_date <= now:
                await interaction.response.send_message(
                    "Das eingegebene Datum muss in der Zukunft liegen.", ephemeral=True
                )
                return

        except ValueError:
            await interaction.response.send_message(
                "Ungültiges Datumsformat! Bitte verwende das Format dd/mm/yyyy.", ephemeral=True
            )
            return

        await self.database.add_checkout(interaction.user.id, reason, duration_str)

        await interaction.response.send_message(
            embed=CheckoutEmbed().checkout_embed(interaction.user, reason, duration_str))


class CheckoutManager:
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()
        self.check_checkout_expiration.start()

    @tasks.loop(minutes=5)
    async def check_checkout_expiration(self):
        expired_checkouts = await self.database.get_expired_checkouts()

        for checkout in expired_checkouts:
            user_id = checkout["user_id"]
            await self.database.remove_checkout(user_id)

            user = self.bot.get_user(user_id)
            if user:
                try:
                    await user.send("Dein Checkout ist abgelaufen und wurde entfernt.")
                except discord.HTTPException:
                    pass

    @check_checkout_expiration.before_loop
    async def before_check_checkout_expiration(self):
        await self.bot.wait_until_ready()
