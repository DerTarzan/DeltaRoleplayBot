import discord


from base.utils.embeds.base_embed import EmbedsBase

class EmbedClear(EmbedsBase):
    def __init__(self):
        super().__init__()

    def clear_embed(self, amount: int, icon: str) -> discord.Embed:
        title = "🗑️ Nachricht gelöscht" if amount == 1 else "🗑️ Nachrichten gelöscht"
        description = (
            f"Es wurde {amount} Nachricht gelöscht"
            if amount == 1
            else f"Es wurden {amount} Nachrichten gelöscht"
        )

        embed = discord.Embed(
            title=title,
            description=description,
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon)

    def clear_all_embed(self, amount: int, icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="🗑️ Es wurden alle Narichten gelöscht",
            description=f"Es wurden {amount} Narichten gelöscht",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon)

    def clear_error_embed(self, error , icon: str) -> discord.Embed:
        embed = discord.Embed(
            title="❌ Fehler",
            description="Es ist ein Fehler aufgetreten",
            color=self.ERROR_COLOR
        )
        embed.add_field(name="⚠️ Fehlermeldung", value=error)
        return self.set_standard_footer_and_author(embed, icon)