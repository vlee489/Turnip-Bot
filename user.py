"""
This file contains commands related to user configuration
and management.
"""
from discord.ext import commands, tasks
import discord
import errors
import turnipCalculator
import datetime


class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pendingDelete = []

    @tasks.loop(hours=2)
    async def updateTasks(self):
        self.pendingDelete = []

    @commands.command(name='deleteData',
                      help="Deletes all data we have on you and associated with you")
    async def deleteData(self, ctx):
        if str(ctx.message.author.id) in self.pendingDelete:
            with ctx.typing():
                print("Deleting data on: {}".format(ctx.message.author.id))
                try:
                    turnipCount = turnipCalculator.deleteTurnipData(str(ctx.message.author.id))
                except errors.NoData:
                    await ctx.send("There's no data on you to delete")
                except errors.AWSError as e:
                    print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                   datetime.datetime.now(),
                                                                                   e))
                    await ctx.send("Issues trying to reach database\nIssue been reported to operator")
                except Exception as e:
                    print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                                   datetime.datetime.now(),
                                                                                   e))
                    await ctx.send("Unknown exception!\nIssue been reported to operator")

                await ctx.send("Thanks for using Turnip Bot, your data has been now Deleted!\n"
                            "Turnip Price Data: {} weeks deleted".format(turnipCount))
        else:
            self.pendingDelete.append(str(ctx.message.author.id))
            await ctx.send("You're asking me to delete all associated I have on you {} !\n"
                           "Enter the `<deleteData` command again for me to delete your data :cry:\n"
                           "**THIS CAN NOT BE UNDONE!!**".format(ctx.message.author.mention))


def setup(bot):
    bot.add_cog(Users(bot))
