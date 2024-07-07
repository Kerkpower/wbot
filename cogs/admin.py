from discord.ext import commands


class Admin(commands.Cog):
    @commands.command(hidden=True)
    @commands.is_owner()
    async def gm(self, ctx, user_id=None, money: int = None):
        """give money to a user"""
        if not money:
            money = int(user_id)
            user_id = int(ctx.message.author.id)

        elif user_id.startswith('<@') and user_id.endswith('>'):
            # If the user_id is a mention, extract the user ID
            user_id = user_id[2:-1]

        user_id = int(user_id)

        dic = ctx.bot.db.get_user(user_id)
        ctx.bot.db.update_user(user_id, {"cash": dic["cash"] + money})

    @commands.command(hidden=True)
    @commands.is_owner()
    async def emergency(self, ctx):
        print("Emergency exiting...")

        await ctx.reply("Emergency exiting...")

        exit()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def add_field(self, ctx, field, value):
        ctx.bot.db.update_all(field, value)


def setup(bot):
    bot.add_cog(Admin(bot))
