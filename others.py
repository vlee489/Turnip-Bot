"""
Contains all the other commands that have no specific
home.
"""
from discord.ext import commands
import discord
import pyjokes
import numpy
import auth

petPicNumber = 32

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

    @commands.command(name='stats',
                      help="Gets the stats on the bot")
    async def stats(self, ctx):
        embedded = discord.Embed(title='Turnip Bot Stats', url='https://github.com/vlee489/Turnip-Bot/',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.add_field(name="Version:", value="Alpha 6.0 RC7", inline=False)
        embedded.add_field(name="Used in number of servers:", value="{} servers".format(len(self.bot.guilds)),
                           inline=False)
        embedded.add_field(name="Contributors:", value="1", inline=False)
        embedded.add_field(name="Kofi Donations", value="https://ko-fi.com/vlee489", inline=False)
        embedded.add_field(name="Issues report", value="https://github.com/vlee489/Turnip-Bot/issues", inline=False)
        embedded.set_footer(text="Turnip Bot by vlee489")
        await ctx.send(embed=embedded)

    @commands.command(name='ping',
                      help="Get the ping to the bot's server",
                      pass_context=True)
    async def ping(self, ctx):
        embedded = discord.Embed(title='Turnip Bot Ping!', url='https://github.com/vlee489/Turnip-Bot/',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.add_field(name="Latency:", value="{}ms".format(round(self.bot.latency * 1000, 2)), inline=True)
        embedded.set_footer(text="Turnip Bot by vlee489")
        await ctx.send(embed=embedded)

    @commands.command(name='Support', help="Join My Server for support",
                      pass_context=True, aliases=['support'])
    async def support(self, ctx):
        embedded = discord.Embed(title='Turnip Support Server!', url='https://discord.gg/JPrC6c2',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.add_field(name="Discord Support Server", value="https://discord.gg/JPrC6c2", inline=False)
        embedded.set_footer(text="Turnip Bot by vlee489")
        await ctx.send(embed=embedded)

    @commands.command(name='test', help="Join My Server for support",
                      pass_context=True)
    async def test(self, ctx):
        print('hi')
        embeded = {
                      'author': {
                          'name': 'embedTest',
                          'icon_url': 'https://vlee.me.uk'
                      },
                      'title': "This is an embed",
                      'url': "http://google.com",
                      'description': "This is a test embed to showcase what they look like and what they can do.",
        }
        await ctx.send(embed=discord.Embed.from_dict(embeded))

    @commands.command(name='pet', help="Get a picture of a pet",
                      pass_context=True)
    async def pet(self, ctx):
        embedded = discord.Embed(title='Pets!', url='https://github.com/vlee489/Turnip-Bot/wiki/Credits',
                                 color=0xCF70D3)
        embedded.set_author(name="Turnip Bot",
                            url="https://github.com/vlee489/Turnip-Bot/",
                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
        embedded.set_image(url="{}/TurnipBot/pets/{}.png".format(auth.CDNLink, numpy.random.randint(0, petPicNumber)))
        await ctx.send(embed=embedded)


def setup(bot):
    bot.add_cog(Others(bot))
