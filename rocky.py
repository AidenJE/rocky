from ast import AsyncFunctionDef
import gino
import disnake
import logging
import os
import sys
import asyncio

from logging.handlers import TimedRotatingFileHandler
from disnake.ext import commands
from utils.models import db


TOKEN = os.environ.get('TOKEN')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_USER}" 


cogs = (
    "cogs.fun",
    "cogs.maintenance",
)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s')

    if not os.path.exists('data'):
        os.makedirs('data')

    file_handler = TimedRotatingFileHandler(filename='data/rocky.log', when='midnight', encoding='utf-8', backupCount=7)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


logger = logging.getLogger(__name__)


class Rocky(commands.Bot):

    def __init__(self, command_prefix):
        intents = disnake.Intents(guilds=True, members=True, reactions=True, bans=True)
        mentions = disnake.AllowedMentions(everyone=False, roles=False)
        super().__init__(
                #command_prefix=commands.when_mentioned_or(*command_prefix),
                command_prefix=command_prefix,
                description="The coolest pigeon on the block.",
                intents=intents,
                allowed_mentions=mentions,
                case_insensitive=True
        )

        self.load_cogs()

    async def on_ready(self):
        logger.info("Rocky is now ready")

    async def close(self):
        await super().close()
        await db.pop_bind().close()
        logger.info("Rocky was closed")

    def load_cogs(self):
        for extension in cogs:
            try:
                self.load_extension(extension)
                logger.info(f'{extension} loaded.')
            except BaseException:
                logger.error(f'{extension} failed to load')

    async def on_command_error(self, ctx: commands.Context, e: disnake.DiscordException):
        if isinstance(e, commands.CommandNotFound):
            return


async def main():
    setup_logger()

    try:
        engine = await gino.create_engine(DB_URL)
        db.bind = engine
    except:
        logger.exception("Failed to connect to PostgreSQL server")
        return

    logger.info("Starting rocky")
    bot = Rocky(command_prefix='.')
    bot.help_command = commands.DefaultHelpCommand()
    await bot.start(TOKEN)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()