import discord

from base.bot import Bot

from base.logger import Logger

logger = Logger(__name__).get_logger()

class DeltaRoleplay(Bot):
    def __init__(self):
        super().__init__()

    def start_bot(self):
        try:
            self.load_cogs("base/cogs")
            self.run(self.config.TOKEN)
        except discord.LoginFailure:
            if not self.utils.is_token_valid():
                logger.error("❌ Invalid Token. Please check your .env file.")
                return

if __name__ == "__main__":
    delta = DeltaRoleplay()
    delta.start_bot()