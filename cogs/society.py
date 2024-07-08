import random

from datetime import datetime, timedelta

import discord
from discord.ext import commands


class Society(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        if luck := random.randint(1, 100) >= 90:
            money = random.randint(1000, 2000)

            await ctx.reply(f"You work your ass off and get {money}", mention_author=False)

        elif luck >= 50:
            money = random.randint(400, 900)

            await ctx.reply(f"You do a respectable amount of work and gain {money}", mention_author=False)

        else:
            money = random.randint(1, 200)

            await ctx.reply(f"You do the bare minimum and gain {money}", mention_author=False)

        dic = ctx.bot.db.get_user(ctx.message.author.id)
        ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] + money})

    @commands.group(invoke_without_command=True)
    async def stocks(self, ctx, user=None):
        user_id = user

        if not user_id:
            user_id = ctx.message.author.id

        elif user_id.startswith('<@') and user_id.endswith('>'):
            # If the user_id is a mention, extract the user ID
            user_id = user_id[2:-1]

        dic = ctx.bot.db.get_user(int(user_id))
        global_var = ctx.bot.db.get_global()

        try:
            if dic["prof_stock"]:
                ...
        except KeyError:
            ctx.bot.db.update_user(ctx.message.author.id, {"prof_stock": 0, "stocks": 0})
            dic = ctx.bot.db.get_user(ctx.message.author.id)

        emb = discord.Embed(
            title=f"{(await ctx.bot.fetch_user(user_id)).display_name}'s balance",
            colour=ctx.bot.other.random_hex()
        )
        emb.add_field(name="Current price of $WIFU", value=global_var["stock_price"], inline=False)
        emb.add_field(name="$WIFU owned:", value=dic["stocks"], inline=False)
        emb.set_footer(text=f"{ctx.message.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=emb, mention_author=False)

    @stocks.command()
    async def buy(self, ctx, amount: int):
        if amount > 100:
            await ctx.reply(f"Can't buy more than 100 stocks at a time", mention_author=False)
            return

        dic_user = ctx.bot.db.get_user(ctx.message.author.id)
        dic_global = ctx.bot.db.get_global()

        try:
            if dic_user["prof_stock"]:
                ...
        except KeyError:
            ctx.bot.db.update_user(ctx.message.author.id, {"prof_stock": 0, "stocks": 0})
            dic_user = ctx.bot.db.get_user(ctx.message.author.id)

        price_curr = dic_global["stock_price"]
        price_change = dic_global["stock_price_change"]

        total_cost = 0

        for i in range(amount):
            total_cost += price_curr
            price_curr += price_change

        if total_cost > dic_user["cash"]:
            await ctx.reply(f"You dont have enough cash to buy that many stocks", mention_author=False)
            return

        ctx.bot.db.update_global({"stock_price": dic_global["stock_price"] + price_change * amount})
        ctx.bot.db.update_user(
            ctx.message.author.id, {
                "cash": dic_user["cash"] - total_cost,
                "prof_stock": dic_user["prof_stock"] - total_cost,
                "stocks": dic_user["stocks"] + amount,
            }
        )

        await ctx.reply(f"You paid {total_cost} and got {amount} $WIFU", mention_author=False)

    @stocks.command()
    async def sell(self, ctx, amount: int):

        # Limit the amount of stocks a user can sell
        if amount > 100:
            await ctx.reply(f"Can't sell more than 100 stocks at a time", mention_author=False)
            return

        user_data = ctx.bot.db.get_user(ctx.message.author.id)
        global_data = ctx.bot.db.get_global()

        try:
            if user_data["prof_stock"]:
                ...
        except KeyError:
            ctx.bot.db.update_user(ctx.message.author.id, {"prof_stock": 0, "stocks": 0})
            user_data = ctx.bot.db.get_user(ctx.message.author.id)

        if amount > user_data["stocks"]:
            await ctx.reply("You don't have that many stocks", mention_author=False)
            return

        current_price = global_data["stock_price"]
        price_change = global_data["stock_price_change"]

        total_gain = 0

        # Calculate the total gain from selling the stocks
        for i in range(amount):
            current_price -= price_change
            total_gain += current_price

        # Update global and user data after the sale
        ctx.bot.db.update_global({"stock_price": global_data["stock_price"] - price_change * amount})
        ctx.bot.db.update_user(
            ctx.message.author.id, {
                "cash": user_data["cash"] + total_gain,
                "prof_stock": user_data["prof_stock"] + total_gain,
                "stocks": user_data["stocks"] - amount,
            }
        )

        # Confirm the sale to the user
        await ctx.reply(f"You received {total_gain} and sold {amount} $WIFU stocks", mention_author=False)

    @commands.command()
    async def daily(self, ctx):
        user = ctx.bot.db.get_user(ctx.message.author.id)
        old_time = user["daily_last"]
        new_time = datetime.now()

        diff = old_time - new_time

        if diff > timedelta(hours=24):
            ctx.bot.db.update_user(ctx.message.author.id,
                                   {
                                       "cash": user["cash"] + 750 + 250 * user["daily_streak"],
                                       "daily_last": new_time,
                                       "daily_streak": user["daily_streak"] + 1
                                   })

            await ctx.reply(f"You got ${750 + 250 * user["daily_streak"]} from your daily", mention_author=False)

        else:
            remaining_time = timedelta(hours=24) - old_time
            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
            minutes = remainder // 60

            if hours >= 1:
                await ctx.reply(f"You need to wait {int(hours)} hours before claiming your next daily",
                                mention_author=False)
            else:
                await ctx.reply(f"You need to wait {int(minutes)} minutes before claiming your next daily",
                                mention_author=False)


def setup(bot):
    bot.add_cog(Society(bot))
