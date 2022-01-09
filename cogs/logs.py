from discord.ext import commands
from utils import crud


class Logs(commands.Cog):
    """
    Register and track users.

    This cog serves as a baseline for all games and 
    utilities that require some form of data storage.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            crud.register_guild(guild)

            for member in guild.members:
                if await crud.is_member_registered(member):
                    crud.register_guildmember(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await crud.is_member_registered(member):
            crud.register_guildmember(member)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        crud.register_guild(guild)

    @commands.command()
    async def register(self, ctx):
        await crud.register_member(ctx.author) 
        await ctx.reply("Your account was succesfully created!")


def setup(bot):
    bot.add_cog(Logs(bot))
