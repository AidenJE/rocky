import gino
import disnake
import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler
from disnake.ext import commands
from utils.models import db


TOKEN = os.environ.get('TOKEN')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_USER}" 


cogs = (
    "cogs.logs",
    "cogs.fun",
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

    def __init__(self):
        intents = disnake.Intents(guilds=True, members=True, reactions=True, bans=True)
        mentions = disnake.AllowedMentions(everyone=False, roles=False)
        super().__init__(
                command_prefix=commands.when_mentioned_or(*['.', '!']),
                description="The coolest pigeon on the block.",
                intents=intents,
                allowed_mentions=mentions,
                case_insensitive=True
        )

        self.engine = None
        self.load_cogs()

    async def connect_database(self):
        if self.engine:
            return

        try:
            engine = await gino.create_engine(DB_URL)
            db.bind = engine
            self.engine = engine
            logger.info("Connected to PostgreSQL server")
        except:
            logger.exception("Failed to connect to postgreSQL server")
            sys.exit(1)

    async def on_ready(self):
        await self.connect_database()
        logger.info("Rocky is now ready!")

    async def close(self):
        await super().close()
        await db.pop_bind().close()

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

if __name__ == '__main__':
    setup_logger()

    logger.info("Starting rocky")
    bot = Rocky() 
    bot.help_command = commands.DefaultHelpCommand()
    bot.run(TOKEN)