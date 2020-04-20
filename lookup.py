"""
This cog deals all the lookup commands
that interface with Nookipedia's private API
"""
from discord.ext import commands
import requests
import auth
import discord


class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='villager',
                      help="Get an overview of a villager and their trites.\n"
                           "<villager>: The villager you want to search for",
                      aliases=['Villager'])
    async def villagerOverview(self, ctx, villager):
        villager_URL = "https://nookipedia.com/api/villager/{}/".format(villager.title())
        try:
            api_response = requests.get(villager_URL, headers={"X-API-Key": auth.nookipedia_API_key})
            if api_response.status_code != 200:
                await ctx.send("Couldn't find villager\n"
                               "If the villager's name is in 2 part, use \" to enclose the name.\n"
                               "E.G. \"Agent S\"")
                return
            jsonData = api_response.json()
            embedded = discord.Embed(title=jsonData['name'], description=jsonData['message'], url=jsonData['link'],
                                     color=0xCF70D3)
            if jsonData['image']:  # Checks if there's an image
                embedded.set_thumbnail(url=jsonData['image'])
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.add_field(name="Species:", value=jsonData['species'], inline=True)
            embedded.add_field(name="Personality:", value=jsonData['personality'], inline=True)
            embedded.add_field(name="Sign:", value=jsonData['sign'], inline=True)
            embedded.add_field(name="Phrase:", value=jsonData['phrase'], inline=True)
            embedded.add_field(name="Birthday:", value=jsonData['birthday'], inline=True)
            embedded.add_field(name="Gender:", value=jsonData['gender'], inline=True)
            embedded.add_field(name="Quote:", value=jsonData['quote'], inline=False)
            embedded.set_footer(text="Info from nookipedia.com")
            await ctx.send(embed=embedded)
            return
        except ValueError:
            await ctx.send("Unable to read data from Nookipedia")
            return
        except requests.exceptions.RequestException:
            await ctx.send("Unable to connect to Nookipedia")
            return

    @commands.command(name='critter',
                      help="Get an overview of a critter and their trites.\n"
                           "<critter>: The critter you want to search for",
                      aliases=['bug', 'fish', 'Critter', 'Bug', 'Fish'])
    async def critterOverview(self, ctx, critter):
        critter_URL = "https://nookipedia.com/api/critter/{}/".format(critter.title())
        try:
            response = requests.get(critter_URL, headers={"X-API-Key": auth.nookipedia_API_key})
            if response.status_code != 200:
                await ctx.send("Couldn't find critter\n"
                               "If the critter's name is in 2 part, use \" to enclose the name.\n"
                               "E.G. \"Common Bluebottle\"")
                return
            jsonData = response.json()
            embedded = discord.Embed(title=jsonData['name'], description=jsonData['message'], url=jsonData['link'],
                                     color=0xCF70D3)
            if jsonData['image']:  # Checks if there's an image
                embedded.set_thumbnail(url=jsonData['image'])
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.add_field(name="Time of Year:", value=jsonData['time-year'], inline=False)
            embedded.add_field(name="Time of Day:", value=jsonData['time-day'], inline=False)
            embedded.add_field(name="Size:", value=jsonData['size'], inline=True)
            embedded.add_field(name="Rarity:", value=jsonData['rarity'], inline=True)
            embedded.add_field(name="Family:", value=jsonData['family'], inline=True)
            embedded.add_field(name="Sale Price:", value=jsonData['price'], inline=False)
            embedded.add_field(name="Catch Phrase:", value=jsonData['caught'], inline=False)
            embedded.set_footer(text="Info from nookipedia.com")
            await ctx.send(embed=embedded)
            return
        except ValueError:
            await ctx.send("Unable to read data from Nookipedia")
            return
        except requests.exceptions.RequestException:
            await ctx.send("Unable to connect to Nookipedia")
            return

    @commands.command(name='fossil',
                      help="Get an overview of a fossil and their trites.\n"
                           "<fossil>: The fossil you want to search for",
                      aliases=['fossils', 'Fossil', 'Fossils'])
    async def fossilOverview(self, ctx, fossil):
        fossil_URL = "https://nookipedia.com/api/fossil/{}/".format(fossil.title())
        try:
            response = requests.get(fossil_URL, headers={"X-API-Key": auth.nookipedia_API_key})
            if response.status_code != 200:
                await ctx.send("Couldn't find fossil\n"
                               "If the fossil's name is in 2 part, use \" to enclose the name.\n"
                               "E.G. \"Tyrannosaurus Rex\"")
                return
            jsonData = response.json()
            embedded = discord.Embed(title=jsonData['name'], description=jsonData['message'], url=jsonData['link'],
                                     color=0xCF70D3)
            if jsonData['image']:  # Checks if there's an image
                embedded.set_thumbnail(url=jsonData['image'])
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.add_field(name="Sections:", value=jsonData['sections'], inline=False)
            embedded.add_field(name="price:", value=jsonData['price'], inline=False)
            embedded.add_field(name="Length:", value=jsonData['length'], inline=True)
            embedded.add_field(name="Period:", value=jsonData['period'], inline=True)
            embedded.add_field(name="Scientific Name:", value=jsonData['scientific-name'], inline=True)
            embedded.set_footer(text="Info from nookipedia.com")
            await ctx.send(embed=embedded)
        except ValueError:
            await ctx.send("Unable to read data from Nookipedia")
            return
        except requests.exceptions.RequestException:
            await ctx.send("Unable to connect to Nookipedia")
            return

    @commands.command(name='eventsToday',
                      help="Get an overview of all the events on today in AC\n",
                      aliases=['eventstoday'])
    async def todayOverview(self, ctx):
        URL = "https://nookipedia.com/api/today/"
        try:
            response = requests.get(URL, headers={"X-API-Key": auth.nookipedia_API_key})
            if response.status_code != 200:
                await ctx.send("Couldn't find events today\n")
                return
            jsonData = response.json()
            if len(jsonData['events']) < 1:
                await ctx.send("No events are on today in Animal Crossing\n")
                return
            embedded = discord.Embed(title='Events Today', description=jsonData['message'], color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            for x in range(len(jsonData['events'])):
                embedded.add_field(name="Events {}:".format(x + 1), value=jsonData['events'][x], inline=False)
            embedded.set_footer(text="Info from nookipedia.com")
            await ctx.send(embed=embedded)
        except ValueError:
            await ctx.send("Unable to read data from Nookipedia")
            return
        except requests.exceptions.RequestException:
            await ctx.send("Unable to connect to Nookipedia")
            return


def setup(bot):
    bot.add_cog(Lookup(bot))
