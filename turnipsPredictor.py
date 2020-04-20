"""
Contains the cog for the turnip commands.
"""
from discord.ext import commands
import turnipCalculator
import datetime


class Turnips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ap', help="Adds today's price to the turnip  "
                                      "\n <Time> : Either PM or AM "
                                      "\n <bells> : The bells you get for selling turnips",
                      aliases=['AddPrice', 'addprice'])
    async def addTurnipPrice(self, ctx, time, bells):
        response = "An Error Has Occured!"
        time = time.upper()  # Turns the time given into Uppercase
        if not bells.isdigit():
            response = "Bells must be given as a number! E.g 1-9"
        elif time == 'AM' or time == 'PM':
            try:
                if turnipCalculator.addData(ctx.message.author.id, datetime.datetime.now(), time, bells):
                    response = "Added price of {} bells for {} at {}".format(bells,
                                                                             (datetime.datetime.now()).strftime(
                                                                                 '%d/%m/%Y'),
                                                                             time)
            except AttributeError:
                response = "Time given to internal system was Invalid\n" \
                           "Has to be either `AM` or `PM`"
            except ValueError:
                response = "You can't give me a time for Sunday!"
        else:
            response = "Time isn't correct, has to be either `AM` or `PM`"

        await ctx.send(response)

    @commands.command(name='addTurnipPrice', help="Add Turnip price data for a specific date & time. \n"
                                                  "<date> : The date to add the price for in DD/MM/YYYY\n"
                                                  "<Time> : Either PM or AM.\n"
                                                  "<bells> : The bells you get for selling turnips.",
                      aliases=['atp', 'addturnipprice'])
    async def addSpecificPrice(self, ctx, date, time, bells):
        try:
            response = turnipCalculator.addSpecifiedData(ctx.message.author.id, date, time, bells)
        except Exception as error:
            await ctx.send(error)
            return
        await ctx.send(response)

    @commands.command(name='ts', help="Get your Turnip Summary for the next week",
                      aliases=['TurnipSummary', 'turnipsummary'])
    async def currentTurnipSummary(self, ctx):
        try:
            report = turnipCalculator.createCurrentSummary(ctx.message.author.id)
        except Exception as error:
            await ctx.send(error)
            return

        await ctx.send("Turnip Summary for this week:\n {}".format(report))

    @commands.command(name='setBuyPrice',
                      help="Set the Price you bought the turnips for from Daisy Mae this week.\n"
                           "<bells> : The amount of bells each turnip cost.",
                      aliases=['setbuyprice', 'sbp'])
    async def setBuyPrice(self, ctx, bells):
        try:
            response = turnipCalculator.addPurchasePrice(ctx.message.author.id, bells)
        except Exception as error:
            await ctx.send(error)
            return
        await ctx.send(response)


def setup(bot):
    bot.add_cog(Turnips(bot))
