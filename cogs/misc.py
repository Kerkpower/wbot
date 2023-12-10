import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Misc(bot))  # add the cog to the bot
