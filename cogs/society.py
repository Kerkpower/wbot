from discord.ext import commands

import random


class Society(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        if luck := random.randint(1, 100) >= 90:
            money = random.randint(1000, 2000)

            await ctx.reply(f"You do work your ass off and get {money}", mention_author=False)

        elif luck >= 50:
            money = random.randint(400, 900)

            await ctx.reply(f"You do a respectable amount of work and gain {money}", mention_author=False)

        else:
            money = random.randint(1, 200)

            await ctx.reply(f"You do the bare minimum and gain {money}", mention_author=False)

        dic = ctx.bot.db.get_user(ctx.message.author.id)
        ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] + money})


def setup(bot):
    bot.add_cog(Society(bot))
