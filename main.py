"""
This file contains all the main event handlers for the
Turnip Bot. All the functions are separated into their own
python classes.
"""

import auth
import discord
from discord.ext import commands

TOKEN = auth.discord_Token

extensions = [
    'turnipsPredictor'
]

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)
