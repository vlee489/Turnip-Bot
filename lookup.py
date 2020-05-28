"""
This cog deals all the lookup commands
"""
import asyncio
from discord.ext import commands, tasks
import discord
from lookupAPI import nookipediaAPI
import os
from dotenv import load_dotenv

load_dotenv(".env")


async def getVillagerList():
    return await nookipediaAPI.NookipediaAPI(os.environ.get("nookipedia_API_key")).getVillagerList()


class Lookup(commands.Cog):
    nookAPI = nookipediaAPI.NookipediaAPI(os.environ.get("nookipedia_API_key"))

    def __init__(self, bot):
        loop = asyncio.get_event_loop()
        self.villagerList = loop.run_until_complete(getVillagerList())
        self.bot = bot

    @tasks.loop(hours=6)
    async def updateLists(self):
        self.villagerList = await self.nookAPI.getVillagerList()
        await self.nookAPI.clearOutdatedCache()

    @commands.command(name='villager',
                      help="Get an overview of a villager and their trites.\n"
                           "<villager>: The villager you want to search for",
                      aliases=['Villager', 'Villagers', 'villagers'])
    async def villagerOverview(self, ctx, villager):
        with ctx.typing():
            villager = villager.title()
            response = await self.nookAPI.getVillager(villager)
            if response is None:
                await ctx.send("Couldn't find villager\n"
                               "If the villager's name is in 2 part, use \" to enclose the name.\n"
                               "E.G. \"Agent S\"")
                return
            embeded = discord.Embed.from_dict(response.response)
            await ctx.send(embed=embeded)

    @commands.command(name='critter',
                      help="Get an overview of a critter and their trites.\n"
                           "<critter>: The critter you want to search for",
                      aliases=['bug', 'fish', 'Critter', 'Bug', 'Fish', 'critters', 'Critters'])
    async def critterOverview(self, ctx, critter):
        with ctx.typing():
            critter = critter.title()
            response = await self.nookAPI.getCritter(critter)
            if response is None:
                await ctx.send("Couldn't find critter\n"
                               "If the critter's name is in 2 part, use \" to enclose the name.\n"
                               "E.G. \"Banded Dragonfly\"")
                return
            embeded = discord.Embed.from_dict(response.response)
            await ctx.send(embed=embeded)

    @commands.command(name='fossil',
                      help="Get an overview of a fossil and their trites.\n"
                           "<fossil>: The fossil you want to search for",
                      aliases=['fossils', 'Fossil', 'Fossils'])
    async def fossilOverview(self, ctx, fossil):
        with ctx.typing():
            fossil = fossil.title()
            response = await self.nookAPI.getFossil(fossil)
            if response is None:
                await ctx.send("Couldn't find fossil\n"
                               "If the fossil's name is in 2 part, use \" to enclose the name.\n"
                               "E.G. \"Tyrannosaurus Rex\"")
                return
            embeded = discord.Embed.from_dict(response.response)
            await ctx.send(embed=embeded)


    @commands.command(name='eventsToday',
                      help="Get an overview of all the events on today in AC\n",
                      aliases=['eventstoday'])
    async def todayOverview(self, ctx):
        with ctx.typing():
            events = await self.nookAPI.getToday()
            if events is None:
                await ctx.send("Unable to get events today >.<")
                return
            if len(events['events']) < 1:  # We Check that there are events today first
                await ctx.send("No events are on today in Animal Crossing\n")
                return
            embedded = discord.Embed(title='Events Today', description=events['message'], color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            for x in range(len(events['events'])):  # For each event we add a field and the event info
                embedded.add_field(name="Events {}:".format(x + 1), value=events['events'][x],
                                   inline=False)
            embedded.set_footer(text="Info from nookipedia.com",
                                icon_url="https://cdn.vlee.me.uk/TurnipBot/Nookipedia.png")
            await ctx.send(embed=embedded)


def setup(bot):
    bot.add_cog(Lookup(bot))
