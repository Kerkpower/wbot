import asyncio
import random
import typing

import discord
from discord.ext import commands


class Gamble(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slots(self, ctx, *, money=0):
        """Slots machine, maybe you'll win!"""
        dic = ctx.bot.db.get_user(ctx.message.author.id)
        if money < 100:
            await ctx.reply("You need to gamble at least $100", mention_author=False)

        elif dic["cash"] < money:
            await ctx.reply(f"You dont have ${money}", mention_author=False)

        else:
            ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] - money})
            symbols = ("🐱", "🐷", "🐸", "🦆", "🐺", "🐵")

            frst = random.choice(symbols)
            scnd = random.choice(symbols)
            thrd = random.choice(symbols)

            tmpl = """You bet ${money} and...
    {a}\t|\t{b}\t|\t{c}
    --------------------
    {d}\t|\t{e}\t|\t{f}
    --------------------
    {g}\t|\t{h}\t|\t{i}"""

            mess = await ctx.send(tmpl.format(
                money=money,
                a=random.choice(symbols), b=random.choice(symbols), c=random.choice(symbols),
                d=random.choice(symbols), e=random.choice(symbols), f=random.choice(symbols),
                g=random.choice(symbols), h=random.choice(symbols), i=random.choice(symbols)))

            await asyncio.sleep(1.5)

            for _ in (1, 2):
                await mess.edit(content=tmpl.format(
                    money=money,
                    a=random.choice(symbols), b=random.choice(symbols), c=random.choice(symbols),
                    d=random.choice(symbols), e=random.choice(symbols), f=random.choice(symbols),
                    g=random.choice(symbols), h=random.choice(symbols), i=random.choice(symbols)))

                await asyncio.sleep(1.5)

            if frst == scnd == thrd:
                await mess.edit(content=tmpl.format(
                    money=money,
                    a=random.choice(symbols), b=random.choice(symbols), c=random.choice(symbols),
                    d=random.choice(frst), e=random.choice(scnd), f=random.choice(thrd),
                    g=random.choice(symbols), h=random.choice(symbols), i=random.choice(symbols)) +
                                        f"\nYou won the jackpot! Money multiplied x5, you got ${-money + money * 5}")
                dic = ctx.bot.db.get_user(ctx.message.author.id)
                ctx.bot.db.update_user(ctx.message.author.id, {
                    "cash": dic["cash"] + money * 5,
                    "profit": {"prof_slots": dic["profit"]["prof_slots"] + money * 5}
                })

            elif frst == scnd or scnd == thrd:
                await mess.edit(content=tmpl.format(
                    money=money,
                    a=random.choice(symbols), b=random.choice(symbols), c=random.choice(symbols),
                    d=random.choice(frst), e=random.choice(scnd), f=random.choice(thrd),
                    g=random.choice(symbols), h=random.choice(symbols), i=random.choice(symbols)) +
                                        f"\nYou got two in a row! Money multiplied x2, you got ${-money + money * 2}")
                dic = ctx.bot.db.get_user(ctx.message.author.id)
                ctx.bot.db.update_user(ctx.message.author.id, {
                    "cash": dic["cash"] + money * 2,
                    "profit": {"prof_slots": dic["profit"]["prof_slots"] + money * 2}
                })

            else:
                await mess.edit(content=tmpl.format(
                    money=money,
                    a=random.choice(symbols), b=random.choice(symbols), c=random.choice(symbols),
                    d=random.choice(frst), e=random.choice(scnd), f=random.choice(thrd),
                    g=random.choice(symbols), h=random.choice(symbols), i=random.choice(symbols)) +
                                        f"\nYou lost ${money} lmao")
                dic = ctx.bot.db.get_user(ctx.message.author.id)
                ctx.bot.db.update_user(ctx.message.author.id, {
                    "profit": {"prof_slots": dic["profit"]["prof_slots"] - money}
                })

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx, *, money=0):
        """50% chance of winning. Might as well, right?"""
        dic = ctx.bot.db.get_user(ctx.message.author.id)
        if money < 0 or money > 100:
            await ctx.reply("You can gamble between $1-100", mention_author=False)

        elif dic["cash"] < money:
            await ctx.reply(f"You dont have ${money}", mention_author=False)

        else:
            if random.randint(0, 1):
                await ctx.reply(f"Heads! You won ${money}!", mention_author=False)
                ctx.bot.db.get_user(ctx.message.author.id)
                ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] + money})

            else:
                await ctx.reply(f"Tails! You lost ${money}", mention_author=False)
                ctx.bot.db.get_user(ctx.message.author.id)
                ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] - money})

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roulette(self, ctx, colour: typing.Literal["red", "black", "green"], amount: int):
        if colour == "black" or colour == "b":
            colour = 0

        elif colour == "red" or colour == "r":
            colour = 1

        elif colour == "green" or colour == "g":
            colour = 2

        else:
            await ctx.reply("colour must be red/black/green", mention_author=False)
            return

        rlt = random.randint(0, 37)

        if rlt == 0 and colour == 2:
            await ctx.reply(f"jackpot! you won {amount * 10}", mention_author=False)

        elif rlt % 2 and colour == 1:
            await ctx.reply(f"red! you won {amount * 2}", mention_author=False)

        elif rlt % 2 == 0 and colour == 0:
            await ctx.reply(f"black! you won {amount * 2}", mention_author=False)

        else:
            await ctx.reply(f"you lost {amount}", mention_author=False)


def setup(bot):
    bot.add_cog(Gamble(bot))
