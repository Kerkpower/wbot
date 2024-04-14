import discord
from discord.ext import commands


class Listeners(commands.Cog):
    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}')

        else:
            print(error)


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Listeners(bot))  # add the cog to the bot
