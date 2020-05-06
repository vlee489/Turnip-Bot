import dbl
from discord.ext import commands
import datetime
import os
from dotenv import load_dotenv

load_dotenv(".env")


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ.get("topGG_API_Key")  # set this to your DBL token
        # Autopost will post your guild count every 30 minutes
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def on_guild_post(self):
        print("Server count posted successfully @ {}".format(datetime.datetime.now()))


def setup(bot):
    bot.add_cog(TopGG(bot))
