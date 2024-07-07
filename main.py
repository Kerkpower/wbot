import discord
from discord.ext import commands
from dotenv import dotenv_values

import random

import utils

env_vars = dotenv_values(".env")
disc_token = env_vars.get("DISC_TOKEN")

intents = discord.Intents.default()
# noinspection PyDunderSlots
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents)

bot.db = utils.MongoDB
bot.other = utils.Others

cogs = [
    "misc",
    "listeners",
    "gamble",
    "admin",
    "account",
    "society"
]

for i in cogs:
    bot.load_extension(f'cogs.{i}')


class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)


bot.help_command = MyNewHelp()


@bot.event
async def on_ready():
    print("bot is ready")
    activity = random.choice([discord.Game("with the API")])
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run(disc_token)
