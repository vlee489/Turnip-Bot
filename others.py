"""
Contains all the other commands that have no specific
home.
"""
from discord.ext import commands
import discord
import pyjokes
import numpy
import os
from dotenv import load_dotenv

load_dotenv(".env")

petPicNumber = 65


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CDNLink = os.environ.get("CDNLink")

    @commands.command(name='joke',
                      help="Get a random programmer joke.")
    async def joke(self, ctx):
        joke = pyjokes.get_joke()
        embedded = discord.Embed(title=joke, color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        embedded.set_footer(text="Jokes from pyjok.es", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='credits',
                      help="The credits for the bot")
    async def credits(self, ctx):
        embedded = discord.Embed(title='Credits', description='Credits of Turnip bot',
                                 url='https://github.com/vlee489/Turnip-Bot/wiki/Credits',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        embedded.set_footer(text="Turnip Bot by vlee489", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='add',
                      help="Add the bot to your own server")
    async def add(self, ctx):
        embedded = discord.Embed(title='Turnip Bot', description='Add Turnip Bot Here',
                                 url='https://github.com/vlee489/Turnip-Bot/',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        embedded.set_footer(text="Turnip Bot by vlee489", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='stats',
                      help="Gets the stats & support for the bot")
    async def stats(self, ctx):
        embedded = discord.Embed(title='Turnip Bot Stats', url='https://github.com/vlee489/Turnip-Bot/',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        embedded.add_field(name="Version:", value="Alpha 7.0 RC1", inline=True)
        embedded.add_field(name="Latency:", value="{}ms".format(round(self.bot.latency * 1000, 2)), inline=True)

        embedded.add_field(name="Used in number of servers:", value="{} servers".format(len(self.bot.guilds)),
                           inline=False)
        embedded.add_field(name="Contributors:", value="1", inline=False)
        embedded.add_field(name="Kofi Donations", value="https://ko-fi.com/vlee489", inline=False)
        embedded.add_field(name="Issues report", value="https://github.com/vlee489/Turnip-Bot/issues", inline=False)
        embedded.add_field(name="Discord Support Server", value="https://discord.gg/JPrC6c2", inline=False)
        embedded.set_footer(text="Turnip Bot by vlee489", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='pet', help="Get a picture of a pet",
                      pass_context=True)
    async def pet(self, ctx):
        embedded = discord.Embed(title='Pets!', url='https://github.com/vlee489/Turnip-Bot/wiki/Credits',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        ran = numpy.random.randint(0, petPicNumber)
        embedded.set_image(url="{}/TurnipBot/pets/{}.png".format(self.CDNLink, ran))
        embedded.set_footer(text="Turnip Bot | Picture No.{}".format(ran),
                            icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)


def setup(bot):
    bot.add_cog(Others(bot))
