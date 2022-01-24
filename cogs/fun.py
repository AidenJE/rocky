from disnake.ext import commands
from pathlib import Path


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def badapple(self, ctx):
        message = await ctx.send("Loading...")

        path = Path("data/frames/")
        for file in [file for file in path.iterdir()]:
            with file.open() as frame:
                await message.edit(content=f"```{frame.read()}```")



def setup(bot):
    bot.add_cog(Fun(bot))
