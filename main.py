"""
This file contains all the main event handlers for the
Turnip Bot. All the separate categories are in their own
cogs (.py files)
"""

import auth
import discord
from discord.ext import commands

TOKEN = auth.discord_Token

extensions = [
    'turnipsPredictor',
    'lookup',
    'others'
]

bot = commands.Bot(command_prefix='<')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="<help to get started on the Turnip Stock Market"))


# Handles incorrect input from user
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing data, you got got to enter something after the command!\n"
                       "You can use `<help` for help")


# Runs the whole show
if __name__ == "__main__":
    for extension in extensions:
        try:
            # Loads in cogs
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)
