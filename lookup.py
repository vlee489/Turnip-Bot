"""
This cog deals all the lookup commands
that interface with Nookipedia's private API
"""
from discord.ext import commands
import auth
import discord
import datetime
import errors
import aiohttp
import json

timeout = aiohttp.ClientTimeout(total=20)  # Timeout for requests in seconds


def urlConstructor(endPoint, pram):
    """
    Creates a URL to nookipedia
    :param endPoint: str
        The end point to use
    :param pram: str
        Any prams for the end point, e.g. villager name
    :return: str
        The URL constructed
    """
    validEndpoints = ['villager', 'critter', 'fossil']
    if endPoint in validEndpoints:
        return "https://nookipedia.com/api/{}/{}/".format(endPoint, (pram.title()).replace("'", "%27"))
    elif endPoint == 'today':
        return "https://nookipedia.com/api/today"
    else:
        raise errors.EndPointValidation("Invalid Nookipedia Endpoint")


async def fetch(session, URL):
    """
    Async function for the fetching data
    :param session: aiohttp.ClientSession
        The session that should be used
    :param URL: str
        The URL to get the request from
    :return: str
        The response from the request
    """
    async with session.get(URL, headers={"X-API-Key": auth.nookipedia_API_key}, timeout=timeout) as response:
        text = await response.text()  # wait till we get something
        if response.status == 200:  # check the status i.e. if we get a 404
            return text
        else:  # If we get anything else other that a 200(OK) we throw an error to be caught
            raise errors.InvalidAPICall(response.status)


class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='villager',
                      help="Get an overview of a villager and their trites.\n"
                           "<villager>: The villager you want to search for",
                      aliases=['Villager', 'Villagers', 'villagers'])
    async def villagerOverview(self, ctx, villager):
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await fetch(session, urlConstructor('villager', villager))
                    if resp is None:  # If the response is None, it means that aiohttp has timed out.
                        await ctx.send("Unable to connect to Nookipedia")
                        print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                       datetime.datetime.now(),
                                                                                       "Timeout on API Call"))
                    else:
                        resp = json.loads(resp)  # Load in reponse as JSON
                        # Create the discord embed and send it.
                        embedded = discord.Embed(title=resp['name'], description=resp['message'], url=resp['link'],
                                                 color=0xCF70D3)
                        if resp['image']:  # Checks if there's an image
                            embedded.set_thumbnail(url=resp['image'])
                        embedded.set_author(name="Turnip Bot",
                                            url="https://github.com/vlee489/Turnip-Bot/",
                                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
                        if resp['species']:
                            embedded.add_field(name="Species:", value=resp['species'], inline=True)
                        if resp['personality']:
                            embedded.add_field(name="Personality:", value=resp['personality'], inline=True)
                        if resp['sign']:
                            embedded.add_field(name="Sign:", value=resp['sign'], inline=True)
                        if resp['phrase']:
                            embedded.add_field(name="Phrase:", value=resp['phrase'], inline=True)
                        if resp['birthday']:
                            embedded.add_field(name="Birthday:", value=resp['birthday'], inline=True)
                        if resp['gender']:
                            embedded.add_field(name="Gender:", value=resp['gender'], inline=True)
                        if resp['quote']:
                            embedded.add_field(name="Quote:", value=resp['quote'], inline=False)
                        embedded.set_footer(text="Info from nookipedia.com")
                        await ctx.send(embed=embedded)
                        return
                except errors.InvalidAPICall:
                    await ctx.send("Couldn't find villager\n"
                                   "If the villager's name is in 2 part, use \" to enclose the name.\n"
                                   "E.G. \"Agent S\"")
                    return
                except errors.EndPointValidation as e:
                    await ctx.send("Internal Error, sorry >.<\n "
                                   "Issue has been reported to operator.\n"
                                   "(EndPointInvalid)")
                    print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                   datetime.datetime.now(),
                                                                                   e))
                    return

    @commands.command(name='critter',
                      help="Get an overview of a critter and their trites.\n"
                           "<critter>: The critter you want to search for",
                      aliases=['bug', 'fish', 'Critter', 'Bug', 'Fish', 'critters', 'Critters'])
    async def critterOverview(self, ctx, critter):
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await fetch(session, urlConstructor('critter', critter))
                    if resp is None:  # If the response is None, it means that aiohttp has timed out.
                        await ctx.send("Unable to connect to Nookipedia")
                        print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                       datetime.datetime.now(),
                                                                                       "Timeout on API Call"))
                    else:
                        jsonData = json.loads(resp)  # Load in reponse as JSON
                        # Create the discord embed and send it.
                        embedded = discord.Embed(title=jsonData['name'], description=jsonData['message'],
                                                 url=jsonData['link'],
                                                 color=0xCF70D3)
                        if jsonData['image']:  # Checks if there's an image
                            embedded.set_thumbnail(url=jsonData['image'])
                        embedded.set_author(name="Turnip Bot",
                                            url="https://github.com/vlee489/Turnip-Bot/",
                                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
                        if jsonData['time-year']:
                            embedded.add_field(name="Time of Year:", value=jsonData['time-year'], inline=False)
                        if jsonData['time-day']:
                            embedded.add_field(name="Time of Day:", value=jsonData['time-day'], inline=False)
                        if jsonData['size']:
                            embedded.add_field(name="Size:", value=jsonData['size'], inline=True)
                        if jsonData['rarity']:
                            embedded.add_field(name="Rarity:", value=jsonData['rarity'], inline=True)
                        if jsonData['family']:
                            embedded.add_field(name="Family:", value=jsonData['family'], inline=True)
                        if jsonData['price']:
                            embedded.add_field(name="Sale Price:", value=jsonData['price'], inline=False)
                        if jsonData['caught']:
                            embedded.add_field(name="Catch Phrase:", value=jsonData['caught'], inline=False)
                        embedded.set_footer(text="Info from nookipedia.com")
                        await ctx.send(embed=embedded)
                        return
                except errors.InvalidAPICall:
                    await ctx.send("Couldn't find villager\n"
                                   "If the villager's name is in 2 part, use \" to enclose the name.\n"
                                   "E.G. \"Agent S\"")
                    return
                except errors.EndPointValidation as e:
                    await ctx.send("Internal Error, sorry >.<\n "
                                   "Issue has been reported to operator.\n"
                                   "(EndPointInvalid)")
                    print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                   datetime.datetime.now(),
                                                                                   e))
                    return

    @commands.command(name='fossil',
                      help="Get an overview of a fossil and their trites.\n"
                           "<fossil>: The fossil you want to search for",
                      aliases=['fossils', 'Fossil', 'Fossils'])
    async def fossilOverview(self, ctx, fossil):
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await fetch(session, urlConstructor('fossil', fossil))
                    if resp is None:  # If the response is None, it means that aiohttp has timed out.
                        await ctx.send("Unable to connect to Nookipedia")
                        print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                       datetime.datetime.now(),
                                                                                       "Timeout on API Call"))
                    else:
                        jsonData = json.loads(resp)  # Load in response as JSON
                        # Create the discord embed and send it.
                        embedded = discord.Embed(title=jsonData['name'], description=jsonData['message'],
                                                 url=jsonData['link'],
                                                 color=0xCF70D3)
                        if jsonData['image']:  # Checks if there's an image
                            embedded.set_thumbnail(url=jsonData['image'])
                        embedded.set_author(name="Turnip Bot",
                                            url="https://github.com/vlee489/Turnip-Bot/",
                                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
                        if jsonData['sections']:
                            embedded.add_field(name="Sections:", value=jsonData['sections'], inline=False)
                        if jsonData['price']:
                            embedded.add_field(name="price:", value=jsonData['price'], inline=False)
                        if jsonData['length']:
                            embedded.add_field(name="Length:", value=jsonData['length'], inline=True)
                        if jsonData['period']:
                            embedded.add_field(name="Period:", value=jsonData['period'], inline=True)
                        if jsonData['scientific-name']:
                            embedded.add_field(name="Scientific Name:", value=jsonData['scientific-name'], inline=True)
                        embedded.set_footer(text="Info from nookipedia.com")
                        await ctx.send(embed=embedded)
                        return
                except errors.InvalidAPICall:
                    await ctx.send("Couldn't find villager\n"
                                   "If the villager's name is in 2 part, use \" to enclose the name.\n"
                                   "E.G. \"Agent S\"")
                    return
                except errors.EndPointValidation as e:
                    await ctx.send("Internal Error, sorry >.<\n "
                                   "Issue has been reported to operator.\n"
                                   "(EndPointInvalid)")
                    print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                   datetime.datetime.now(),
                                                                                   e))
                    return

    @commands.command(name='eventsToday',
                      help="Get an overview of all the events on today in AC\n",
                      aliases=['eventstoday'])
    async def todayOverview(self, ctx):
        URL = "https://nookipedia.com/api/today/"
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await fetch(session, URL)
                    if resp is None:  # If the response is None, it means that aiohttp has timed out.
                        await ctx.send("Unable to connect to Nookipedia")
                        print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                       datetime.datetime.now(),
                                                                                       "Timeout on API Call"))
                    else:
                        jsonData = json.loads(resp)  # Load in response as JSON
                        if len(jsonData['events']) < 1:  # We Check that there are events today first
                            await ctx.send("No events are on today in Animal Crossing\n")
                            return
                        embedded = discord.Embed(title='Events Today', description=jsonData['message'], color=0xCF70D3)
                        embedded.set_author(name="Turnip Bot",
                                            url="https://github.com/vlee489/Turnip-Bot/",
                                            icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
                        for x in range(len(jsonData['events'])):  # For each event we add a field and the event info
                            embedded.add_field(name="Events {}:".format(x + 1), value=jsonData['events'][x],
                                               inline=False)
                        embedded.set_footer(text="Info from nookipedia.com")
                        await ctx.send(embed=embedded)
                        return
                except errors.InvalidAPICall:
                    await ctx.send("Couldn't find villager\n"
                                   "If the villager's name is in 2 part, use \" to enclose the name.\n"
                                   "E.G. \"Agent S\"")
                    return
                except errors.EndPointValidation as e:
                    await ctx.send("Internal Error, sorry >.<\n "
                                   "Issue has been reported to operator.\n"
                                   "(EndPointInvalid)")
                    print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                   datetime.datetime.now(),
                                                                                   e))
                    return


def setup(bot):
    bot.add_cog(Lookup(bot))
