from discord.ext import commands
from utils import crud


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await crud.add_memberjoinlog(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await crud.add_memberleavelog(member.id)


def setup(bot):
    bot.add_cog(Logs(bot))
