from discord.ext import commands
from utils import crud


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Logs(bot))
