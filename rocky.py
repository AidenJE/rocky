import discord
import logging
import os

from logging.handlers import TimedRotatingFileHandler
from discord.ext import commands


cogs = ("cogs.minecraft",)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s')

    file_handler = TimedRotatingFileHandler(
        filename='logs/rocky.log', when='midnight', encoding='utf-8', backupCount=7)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


logger = logging.getLogger(__name__)


class Rocky(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(
            command_prefix=command_prefix,
            description="The coolest pigeon on the block.",
        )

        self.logger = logger
        self.load_cogs()

    def load_cogs(self):
        for extension in cogs:
            try:
                self.load_extension(extension)
                logger.info(f'{extension} loaded.')
            except BaseException as e:
                logger.error(f'{extension} failed to load.')
                logger.error(e)

    async def on_command_error(self, ctx: commands.Context, e: discord.DiscordException):
        if isinstance(e, commands.CommandNotFound):
            return


if __name__ == '__main__':
    setup_logger()

    TOKEN = os.environ.get('TOKEN')
    logger.info("Starting rocky")
    bot = Rocky(command_prefix=':>')
    bot.run(TOKEN)
