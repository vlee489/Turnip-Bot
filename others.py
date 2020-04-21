"""
Contains all the other commands that have no specific
home.
"""
from discord.ext import commands
import discord
import pyjokes


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joke',
                          help="Get a random joke.")
    async def joke(self, ctx):
        joke = pyjokes.get_joke()
        embedded = discord.Embed(title=joke, color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.set_footer(text="Jokes from pyjok.es")
        await ctx.send(embed=embedded)

    @commands.command(name='credits',
                      help="The credits for the bot")
    async def credits(self, ctx):
        embedded = discord.Embed(title='Credits', description='Credits of Turnip bot',
                                 url='https://github.com/vlee489/Turnip-Bot/wiki/Credits',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.set_footer(text="Turnip Bot by vlee489")
        await ctx.send(embed=embedded)

    @commands.command(name='add',
                      help="Add the bot to your own server")
    async def add(self, ctx):
        embedded = discord.Embed(title='Turnip Bot', description='Add Turnip Bot Here',
                                 url='https://github.com/vlee489/Turnip-Bot/',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.set_footer(text="Turnip Bot by vlee489")
        await ctx.send(embed=embedded)


def setup(bot):
    bot.add_cog(Others(bot))
