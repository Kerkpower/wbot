import discord
from discord.ext import commands
from dotenv import dotenv_values

import utils

env_vars = dotenv_values(".env")
disc_token = env_vars.get("DISC_TOKEN")

intents = discord.Intents.default()
# noinspection PyDunderSlots
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents, help_command=commands.HelpCommand())

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


class SupremeHelpCommand(commands.DefaultHelpCommand):
    def get_command_signature(self, command):
        signature = command.signature.replace('"', '').replace('|', ' | ')
        return f'{self.context.prefix}{command.qualified_name} {signature}'

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Bot Help", color=discord.Color.blurple())

        for cog, cmnds in mapping.items():
            filtered_commands = await self.filter_commands(commands, sort=True)
            if filtered_commands:
                cog_name = cog.qualified_name if cog else "No Category"
                command_signatures = [self.get_command_signature(c) for c in filtered_commands]
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.blurple())
        if command.help:
            embed.description = command.help
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(group), color=discord.Color.blurple())
        if group.help:
            embed.description = group.help

        subcommands = group.commands
        if subcommands:
            subcommands_text = "\n".join([self.get_command_signature(cmd) for cmd in subcommands])
            embed.add_field(name="Subcommands", value=subcommands_text, inline=False)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        cog_name = cog.qualified_name if cog else "No Category"
        embed = discord.Embed(title=f'{cog_name} Category', color=discord.Color.blurple())
        if cog and cog.description:
            embed.description = cog.description

        cog_commands = cog.get_commands() if cog else self.context.bot.commands
        if cog_commands:
            command_signatures = [self.get_command_signature(c) for c in cog_commands]
            embed.add_field(name="Commands", value="\n".join(command_signatures), inline=False)

        await self.get_destination().send(embed=embed)


bot.help_command = SupremeHelpCommand()


@bot.event
async def on_ready():
    print("bot is ready")


bot.run(disc_token)
