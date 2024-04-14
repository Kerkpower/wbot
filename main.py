from dotenv import dotenv_values

import utils

import discord
from discord.ext import commands

env_vars = dotenv_values(".env")
disc_token = env_vars.get("DISC_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=';', intents=intents)

bot.db = utils.MongoDB
bot.other = utils.Others

cogs = [
    "misc",
    "listeners",
    "gamble",
    "admin",
    "account",
]

for i in cogs:
    bot.load_extension(f'cogs.{i}')


@bot.event
async def on_ready():
    print("bot is ready")


bot.run(disc_token)
