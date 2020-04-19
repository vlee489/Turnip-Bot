"""
This cog deals with the villager commands
"""
from discord.ext import commands
import requests
import auth
import discord


class Villager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='villager',
                      help="Get an overview of a villager and their trites.\n"
                           "<villager>: The villager you want to search for")
    async def villagerOverview(self, ctx, villager):
        villager_URL = "https://nookipedia.com/api/villager/{}/".format(villager)
        try:
            api_response = requests.get(villager_URL, headers={"X-API-Key": auth.nookipedia_API_key})
            if api_response.status_code != 200:
                await ctx.send("Error in finding villager")
                return
            jsonData = api_response.json()
            print(jsonData)
            embedded = discord.Embed(title=jsonData['name'], description=jsonData['message'], url=jsonData['link'],
                                     color=0xCF70D3)
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
            embedded.set_footer(text="Info from https://nookipedia.com/")
            await ctx.send(embed=embedded)
            return
        except ValueError:
            await ctx.send("Unable to read data from Nookipedia")
            return
        except requests.exceptions.RequestException:
            await ctx.send("Unable to connect to Nookipedia")
            return


def setup(bot):
    bot.add_cog(Villager(bot))
