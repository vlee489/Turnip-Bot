"""
This file contains all the main event handlers for the
Turnip Bot. All the separate categories are in their own
cogs (.py files)
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv(".env")
TOKEN = os.environ.get("discord_Token")
# This is the list of cogs that discord.py loads in as file names without the .py extension
extensions = [
    'turnipsPredictor',
    'lookup',
    'others',
    'user'
]


# Gets the prefix for the servers
def getPrefix(client, message):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=getPrefix)

helloMessage = "Hello There :wave:, use `<help` to get started"
if os.path.exists("join.txt"):
    with open("join.txt", 'r') as f:
        helloMessage = f.read()


# When the bot is loaded
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("Used in {} servers".format(len(bot.guilds)))
    print('------')
    await bot.change_presence(activity=discord.Game(name="<help to get started on the Stalk Market"))
    # Following checks if a message.txt file exists on boot, it it does we message all servers with it and then delete
    # it. The message.txt file supports Discord flavoured markdown.
    if os.path.exists("message.txt"):
        with open("message.txt") as file:  # Open txt file
            broadcastMessage = file.read()  # read in txt file
            for server in bot.guilds:  # for each server/guild the bot is in
                for channel in server.text_channels:  # go through the text channels
                    if channel.permissions_for(server.me).send_messages:  # if it has perms to post in it, post there
                        await channel.send(broadcastMessage)  # send message
                        break  # Break so it doesn't spam the server with more than one message
        os.remove("message.txt")  # remove message.txt file


# Handles incorrect input from user
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing data, you got got to enter something after the command!\n"
                       "You can use `<help` for help")


@bot.event
async def on_guild_join(guild):
    # This adds the prefix to the file
    with open('prefix.json', 'r') as prefixFile:
        prefixes = json.load(prefixFile)
    prefixes[str(guild.id)] = "<"
    with open('prefix.json', 'w') as prefixFile:
        json.dump(prefixes, prefixFile, indent=4)
    # Send the hello message
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(helloMessage)
            break


@bot.event
async def on_guild_remove(guild):
    # Removed guild from prefix file if bot is removed
    with open('prefix.json', 'r') as prefixFile:
        prefixes = json.load(prefixFile)
    prefixes.pop(str(guild.id))
    with open('prefix.json', 'w') as prefixFile:
        json.dump(prefixes, prefixFile, indent=4)


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
