import asyncio

from discord.ext import commands


class Listeners(commands.Cog):
    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}')

        elif isinstance(error, commands.UserInputError):
            await ctx.reply(error, mention_author=False)

        elif isinstance(error, commands.NotOwner):
            await ctx.reply(error, mention_author=False)

        elif isinstance(error, commands.CommandNotFound):
            print(f"The user @{ctx.author.name} ({ctx.author.id}) tried to use the command `{ctx.message.content[1:]}`")

        else:
            print(error)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id == 1231263378719379567:
            await msg.add_reaction('🌌')
            await asyncio.sleep(15)
            await msg.delete()


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Listeners(bot))  # add the cog to the bot
