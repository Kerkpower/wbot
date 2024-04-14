import discord
from discord.ext import commands


class Currency(commands.Cog):
    @commands.command(aliases=["bal"])
    async def balance(self, ctx, *, user_id=None):
        """Check the balance of a user"""
        if not user_id:
            user_id = ctx.message.author.id

        dic = ctx.bot.db.get_user(user_id)

        emb = discord.Embed(
            title=f"{(await ctx.bot.fetch_user(user_id)).display_name}'s balance",
            colour=discord.Colour.random()
        )
        emb.add_field(name="Cash:", value=dic["cash"], inline=False)
        emb.add_field(name="Bank:", value=f"{dic['bank']}/{dic['bank_max']}", inline=False)
        emb.set_footer(text=f"{ctx.message.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=emb, mention_author=False)

    @commands.command(aliases=["dep"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount=0):
        dic = ctx.bot.db.get_user(ctx.message.author.id)

        if str(amount).lower() in ("max", "all"):
            amount = dic["cash"]
        try:
            int(amount)
        except TypeError:
            await ctx.reply(f"You need to specify a number", mention_author=False)
            return

        if amount < 1:
            await ctx.reply("You need to deposit at least $1", mention_author=False)

        elif dic["cash"] < amount:
            await ctx.reply("You cant deposit more than you own", mention_author=False)

        else:
            dep = min(amount, dic["bank_max"] - dic["bank"])
            ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] - dep, "bank": dic["bank"] + dep})

            await ctx.reply(f"Deposited ${dep}", mention_author=False)

    @commands.command(aliases=["with"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount=0):
        dic = ctx.bot.db.get_user(ctx.message.author.id)

        if str(amount).lower() in ("max", "all"):
            amount = dic["bank"]

        if amount < 1:
            await ctx.reply("You need to withdraw at least $1", mention_author=False)

        elif dic["cash"] < amount:
            await ctx.reply("You cant withdraw more than you own", mention_author=False)

        else:
            wit = min(amount, dic["bank"])
            ctx.bot.db.update_user(ctx.message.author.id, {"cash": dic["cash"] + wit, "bank": dic["bank"] - wit})

            await ctx.reply(f"Withdrew ${wit}", mention_author=False)


def setup(bot):
    bot.add_cog(Currency(bot))