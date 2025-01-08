import discord

from base.utils.embeds.base_embed import EmbedsBase

class EmbedVerify(EmbedsBase):
    def __init__(self):
        super().__init__()

    def verify_embed(self, channel:discord.TextChannel, thumbnail: str) -> discord.Embed:
        embed = discord.Embed(
            title="🔒 Verifizierung",
            description="Bitte lese dir die Regeln durch",
            color=self.INFO_COLOR
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(
            name="📜 **Regeln**",
            value="Halte dich bitte an die [Discord TOS](https://discord.com/terms).",
            inline=False
        )
        embed.add_field(
            name="📌 **Weitere Hinweise**",
            value=f"Alle spezifischen Regeln findest du in {channel.mention}. Bitte lies diese vollständig durch, um zu verstehen, was von dir erwartet wird.",
            inline=False
        )

        return self.set_standard_footer_and_author(embed, thumbnail)

    def verify_success_embed(self, thumbnail: str) -> discord.Embed:
        embed = discord.Embed(
            title="🔓 Verifizierung",
            description="Du wurdest erfolgreich verifiziert ✅",
            color=self.INFO_COLOR
        )
        embed.set_thumbnail(url=thumbnail)
        return self.set_standard_footer_and_author(embed, thumbnail)

    def verify_already_verified_embed(self, thumbnail: str) -> discord.Embed:
        embed = discord.Embed(
            title="❌ Verifizierung fehlgeschlagen",
            description="Du bist bereits verifiziert",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, thumbnail)

    def verify_failed_credentials_embed(self, thumbnail: str, channel: discord.VoiceChannel) -> discord.Embed:
        # Erstelle die Embed-Nachricht mit einem klaren Titel und einer Fehlermeldung
        embed = discord.Embed(
            title="❌ Verifizierung fehlgeschlagen",
            description="Leider konnte dein Account nicht verifiziert werden.",
            color=self.ERROR_COLOR
        )

        embed.add_field(
            name="⚠️ Grund der Ablehnung",
            value=(
                f"Dein Account ist noch zu jung, was aus Sicherheitsgründen erforderlich ist. "
                f"Bitte stelle sicher, dass du mindestens 7 Tage alt bist, um dich zu verifizieren. "
                f"Du kannst dich weiterhin im {channel.mention} melden, falls du weitere Fragen hast."
            )
        )

        return self.set_standard_footer_and_author(embed, thumbnail)

    def verify_error_embed(self, thumbnail: str, error: str, channel: discord.VoiceChannel) -> discord.Embed:
        embed = discord.Embed(
            title="❌ Fehler",
            description="Es ist ein Fehler aufgetreten",
            color=self.ERROR_COLOR
        )
        embed.add_field(name="⚠️ Fehlermeldung", value=error)
        embed.add_field(name="🔧 Lösung", value=f"Bitte versuche es erneut oder melde dich im {channel.mention} für weitere Hilfe.")

        return self.set_standard_footer_and_author(embed, thumbnail)