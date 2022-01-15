import os

from disnake.ext import commands
from pathlib import Path


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def test(self, ctx):
        print('run')
        await ctx.send("test")

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message)

    @commands.command()
    async def badapple(self, ctx):
        message = await ctx.send("Loading...")

        path = Path("data/frames/")
        for file in [file for file in path.iterdir()]:
            with file.open() as frame:
                await message.edit(content=f"```{frame.read()}```")



def setup(bot):
    bot.add_cog(Fun(bot))
