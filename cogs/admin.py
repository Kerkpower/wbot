from discord.ext import commands


class Admin(commands.Cog):
    @commands.command(hidden=True)
    @commands.is_owner()
    async def gm(self, ctx, money: int, user_id=None):
        """give money to a user"""
        if not user_id:
            user_id = ctx.message.author.id

        dic = ctx.bot.db.get_user(user_id)
        ctx.bot.db.update_user(user_id, {"cash": dic["cash"] + money})


def setup(bot):
    bot.add_cog(Admin(bot))
