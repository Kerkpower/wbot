import asyncio
import random
import typing

from discord.ext import commands


class Gamble(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slots(self, ctx, money):
        """Slots machine, maybe you'll win!"""
        dic = ctx.bot.db.get_user(ctx.message.author.id)

        if money == "max":
            money = dic["cash"]

        money = int(money)

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
    ------------------------------
    {d}\t|\t{e}\t|\t{f}
    ------------------------------
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
                    "prof_slots": dic["prof_slots"] + money * 5
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
                    "prof_slots": dic["prof_slots"] + money * 2
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
                    "prof_slots": dic["prof_slots"] - money
                })

    @commands.command(aliases=["coin"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx, money: int or str):
        """50% chance of winning. Might as well, right?"""
        dic = ctx.bot.db.get_user(ctx.message.author.id)
        if money < 0 or money > 100:
            await ctx.reply("You can gamble between $1-100", mention_author=False)
            return

        if dic["cash"] < money:
            await ctx.reply(f"You dont have ${money}", mention_author=False)
            return

        if str(money).lower() in ["max", "all"]:
            money = 100

        if random.getrandbits(1):
            await ctx.reply(f"Heads! You won ${money}!", mention_author=False)
            ctx.bot.db.get_user(ctx.message.author.id)
            ctx.bot.db.update_user(ctx.message.author.id, {
                "cash": dic["cash"] + money,
                "prof_coin": dic["prof_coin"] + money
            })

        else:
            await ctx.reply(f"Tails! You lost ${money}", mention_author=False)
            ctx.bot.db.get_user(ctx.message.author.id)
            ctx.bot.db.update_user(ctx.message.author.id, {
                "cash": dic["cash"] - money,
                "prof_coin": dic["prof_coin"] - money
            })

    @commands.command(aliases=['rl'])
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def roulette(self, ctx, colour: typing.Literal["red", "black", "green"], money: int = 0):
        symbols = ["⚫", "🔴", "🟢"]
        tmpl = """
--------------------------------------------
{a}\t{b}\t|\t{c}\t|\t{d}\t{e}
--------------------------------------------
"""
        dic = ctx.bot.db.get_user(ctx.message.author.id)

        if money < 1_000:
            await ctx.reply("You need to bet at least 1000$")
            return

        if money > dic["cash"]:
            await ctx.reply(f"You dont have ${money}", mention_author=False)
            return

        if colour == "black":
            colour = 0

        elif colour == "red":
            colour = 1

        elif colour == "green":
            colour = 2

        dic = ctx.bot.db.get_user(ctx.message.author.id)
        ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] - money,
                                                       "prof_roul": dic["prof_roul"] - money
                                                       })

        shuffle_msg = await ctx.reply("Rolling: \n" + tmpl.format(
            a=symbols[0], b=symbols[1], c=symbols[2], d=symbols[0], e=symbols[1]
        ))

        x = ['🔴' if i % 2 else '⚫' for i in range(37)]
        x[-1] = '🟢'

        place = random.randint(0, 32)

        for _ in range(4):
            await asyncio.sleep(1.5)

            await shuffle_msg.edit(content="Rolling: \n" + tmpl.format(
                a=x[place % 37],
                b=x[(place + 1) % 37],
                c=x[(place + 2) % 37],
                d=x[(place + 3) % 37],
                e=x[(place + 4) % 37]
            ))

            place += 1

        place += 1

        dic = ctx.bot.db.get_user(ctx.message.author.id)

        if place == 36 and colour == 2:
            await ctx.reply(f"jackpot! you won {money * 10}$", mention_author=False)
            ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] + money * 10,
                                                           "prof_roul": dic["prof_roul"] + money * 10
                                                           })

        elif (place % 2 and colour == 1) or (place % 2 == 0 and colour == 0):
            await ctx.reply(f"you won {money * 2}$", mention_author=False)
            ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] + money * 2,
                                                           "prof_roul": dic["prof_roul"] + money * 2
                                                           })

        else:
            await ctx.reply(f"it was {x[(place + 2) % 37]} and {place}\nyou lost {money}$", mention_author=False)


def setup(bot):
    bot.add_cog(Gamble(bot))
