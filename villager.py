"""
This cog deals with the villager commands
"""
from discord.ext import commands
import requests
import auth
import json


class Turnips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='villager',
                      help="Get an overview of a villager and their trites.\n"
                           "<villager>: The villager you want to search for")
    async def villagerOverview(self, ctx, villager):
        villager_URL = "https://nookipedia.com/api/villager/{}".format(villager)
        try:
            api_response = requests.get(villager_URL, headers={'X-API-Key': auth.nookipedia_API_key})
            if api_response.status_code != 200:
                await ctx.send("Error in finding villager")
                return
            jsonData = api_response.json()
            print(jsonData)
        except ValueError:
            await ctx.send("Unable to read data from Nookipedia")
            return
        except requests.exceptions.RequestException:
            await ctx.send("Unable to connect to Nookipedia")
            return


def setup(bot):
    bot.add_cog(Turnips(bot))
