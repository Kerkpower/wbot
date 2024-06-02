import json
import random
from datetime import datetime
from datetime import timezone
from math import prod
from typing import Union

import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
        with open("./quotes/suntzu.json", 'r') as f:
            quotes = json.load(f)

        await ctx.reply(f"> {random.choice(quotes)}\n> —Sun Tzu, The Art of War", mention_author=False)

    @commands.command()
    async def howgay(self, ctx, *, user: Union[discord.User, str] = None):
        """Note: All scores are 100% accurate."""
        if user is None:
            user = ctx.author

        now = datetime.now(timezone.utc)

        if isinstance(user, str):
            seed = prod(ord(c) + i for i, c in enumerate(user)) * now.month * now.year
        else:
            seed = user.id * now.month * now.year

        random.seed(seed)
        gayness = random.random()

        if now.month == 6:  # pride month
            gayness **= 0.25

        if user == 'gay':
            gayness = 1

        if user == ctx.author:
            await ctx.reply(f"You are {gayness:.1%} gay.", mention_author=False)
        else:
            name = user if isinstance(user, str) else user.name
            await ctx.reply(f"{name} is {gayness:.1%} gay.", mention_author=False)
        random.seed()

    @commands.command()
    @commands.is_owner()
    async def foo(self, ctx):
        ...


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Misc(bot))  # add the cog to the bot
