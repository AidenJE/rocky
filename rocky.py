import asyncio
import gino
import discord
import logging
import os

from logging.handlers import TimedRotatingFileHandler
from discord.ext import commands
from utils.models import db


TOKEN = os.environ.get('TOKEN')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_USER}" 


cogs = (
    "cogs.logs",
)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s')

    if not os.path.exists('data'):
        os.makedirs('data')

    file_handler = TimedRotatingFileHandler(filename='data/rocky.log', when='midnight', encoding='utf-8', backupCount=7)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


logger = logging.getLogger(__name__)


class Rocky(commands.Bot):

    def __init__(self, engine):
        intents = discord.Intents(guilds=True, members=True, reactions=True, bans=True)
        mentions = discord.AllowedMentions(everyone=False, roles=False)
        super().__init__(
                command_prefix=commands.when_mentioned_or('!'),
                description="The coolest pigeon on the block.",
                intents=intents,
                allowed_mentions=mentions,
                case_insensitive=True
        )

        self.engine = engine
        self.load_cogs()

    async def close(self):
        await super().close()
        await db.pop_bind().close()

    def load_cogs(self):
        for extension in cogs:
            try:
                self.load_extension(extension)
            except BaseException:
                logger.error(f'{extension} failed to load')

    async def on_command_error(self, ctx: commands.Context, e: discord.DiscordException):
        if isinstance(e, commands.CommandNotFound):
            return


async def startup():
    setup_logger()

    try:
        engine = await gino.create_engine(DB_URL)
        db.bind = engine
    except:
        logger.exception("Failed to connect to postgreSQL server")
        return

    logger.info("Starting rocky")
    bot = Rocky(engine) 
    bot.help_command = commands.DefaultHelpCommand(dm_help=None)
    await bot.start(TOKEN)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
