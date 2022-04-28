import discord
import mariadb
import os

from discord.ext import commands


class MinecraftManager:
    def __init__(self):
        USER = os.environ.get('MC_USER')
        PASSWORD = os.environ.get('MC_PASSWORD')
        HOST = os.environ.get('MC_HOST')
        PORT = int(os.environ.get('MC_PORT'))
        DATABASE = os.environ.get('MC_DATABASE')

        self.conn = mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE,
        )

        self.conn.auto_reconnect = True
        self.cur = self.conn.cursor()

    def is_code_valid(self, code):
        self.cur.execute("SELECT COUNT(1) FROM code WHERE code = ?", (code, ))
        return 1 in self.cur.fetchall()[0]

    def is_player_whitelisted(self, code):
        self.cur.execute("SELECT whitelisted FROM player WHERE uuid IN (SELECT player_uuid FROM code WHERE code = ?)", (code, ))
        return 1 in self.cur.fetchall()[0]

    def whitelist_player(self, code):
        self.cur.execute("UPDATE player SET whitelisted = 1 WHERE uuid IN (SELECT player_uuid FROM code WHERE code = ?)", (code, ))
        self.bot.conn.commit()


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = MinecraftManager()

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
        embed = discord.Embed(
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
        embed = discord.Embed(title="Account already whitelisted",
                              description="Please double check that you can connect to the server.",
                              colour=0xFFAE00)
        embed.add_field(name="I still can't connect, what do I do?",
                        value="Contact Auden.", inline=False)
        await ctx.reply(embed=embed)

    async def send_success_message(self, ctx):
        embed = discord.Embed(title="Account succesfully whitelisted",
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
