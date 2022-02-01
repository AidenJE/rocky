import disnake
import mariadb

from disnake.ext import commands
from utils import minecraft


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = minecraft.MinecraftManager()

    @commands.command(help="Register your lunchclub token here.")
    @commands.cooldown(2, 3.0, commands.BucketType.user)
    async def register(self, ctx, code: str):
        code = code.upper()

        if not self.manager.is_code_valid(code):
            await self.send_error_message(ctx)
        elif self.manager.is_player_whitelisted(code):
            await self.send_reminder_message(ctx)
        else:
            self.manager.whitelist_player(code)
            await self.send_success_message(ctx)

    async def send_error_message(self, ctx):
        embed = disnake.Embed(
            title="Invalid token",
            description="The token you provided is invalid, please double check it.\n To register your token, type: `!register YOURTOKENHERE`",
            colour=0xFF0000)
        embed.add_field(name="What's a token?",
                        value="You can get a token by connecting to the Lunch Club SMP server. Register your token to get your account whitelisted.",
                        inline=False)
        embed.add_field(name="Everything's broken, help!",
                        value="Contact Auden.", inline=False)
        await ctx.reply(embed=embed)

    async def send_reminder_message(self, ctx):
        embed = disnake.Embed(title="Account already whitelisted",
                              description="Please double check that you can connect to the server.",
                              colour=0xFFAE00)
        embed.add_field(name="I still can't connect, what do I do?",
                        value="Contact Auden.", inline=False)
        await ctx.reply(embed=embed)

    async def send_success_message(self, ctx):
        embed = disnake.Embed(title="Account succesfully whitelisted",
                              description="Your account has been whitelisted and you should now be able to join the Lunch Club SMP server!",
                              colour=0x00FF00)
        await ctx.reply(embed=embed)

    @register.error
    async def register_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply('You are currently on cooldown, please wait up to 3 seconds.')
        elif isinstance(error, mariadb.Error):
            self.bot.logger.error(f'{error}')
            await ctx.reply('Something went horribly wrong, contact Auden.')


def setup(bot):
    bot.add_cog(Minecraft(bot))
