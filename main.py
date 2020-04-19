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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command doesn't Exist!\n"
                       "You can use `>help` to see what commands there are")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing data, you got got to enter something after the command!\n"
                       "You can use `>help` for help")
    else:
        await ctx.send("Invalid command!\n"
                       "You can use `>help` to see what commands there are")


if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)
