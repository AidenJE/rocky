from disnake.ext import commands


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.slash_command()
    async def close(self, inter):
        await inter.response.send_message("Initiated self-destruct sequence")
        await self.bot.close()


def setup(bot):
    bot.add_cog(Maintenance(bot))