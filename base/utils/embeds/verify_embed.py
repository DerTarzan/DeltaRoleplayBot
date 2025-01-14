import discord

from base.utils.embeds.base_embed import EmbedsBase

class EmbedVerify(EmbedsBase):
    def __init__(self):
        super().__init__()

    def verify_embed(self, channel:discord.TextChannel, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🔒 Verifizierung",
            description="       ",
            color=self.INFO_COLOR
        )
        embed.add_field(
            name="**INFO**",
            value=f"> Das Regelwerk findest du im {channel.mention}\n > sowie die Discord TOS Richtlinien. ",
            inline=False
        )

        embed.set_image(url="https://i.ibb.co/Mk3hGRy/banner-delta-klein.png")

        return self.set_standard_footer_and_author(embed, icon_url)

    def verify_success_embed(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🔓 Verifizierung",
            description="Du wurdest erfolgreich verifiziert ✅",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def verify_already_verified_embed(self, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="❌ Verifizierung fehlgeschlagen",
            description="Du bist bereits verifiziert",
            color=self.ERROR_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def verify_failed_credentials_embed(self, channel: discord.VoiceChannel, icon_url: str  = "") -> discord.Embed:
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

        return self.set_standard_footer_and_author(embed, icon_url)

    def verify_error_embed(self, error: str, channel: discord.VoiceChannel, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="❌ Fehler",
            description="Es ist ein Fehler aufgetreten",
            color=self.ERROR_COLOR
        )
        embed.add_field(name="⚠️ Fehlermeldung", value=error)
        embed.add_field(name="🔧 Lösung", value=f"Bitte versuche es erneut oder melde dich im {channel.mention} für weitere Hilfe.")

        return self.set_standard_footer_and_author(embed, icon_url)