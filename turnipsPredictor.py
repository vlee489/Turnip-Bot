"""
Contains the cog for the turnip commands.
"""
from discord.ext import commands
import turnipCalculator
import datetime
import turnipSummaryImage
import discord


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
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           error))
            return
        await ctx.send(response)

    @commands.command(name='ts', help="Get your Turnip Summary for the next week",
                      aliases=['TurnipSummary', 'turnipsummary'])
    async def currentTurnipSummary(self, ctx):
        try:
            report = turnipCalculator.createCurrentSummary(ctx.message.author.id)
            newImage = turnipSummaryImage.SummaryImage(report, ctx.message.author.id)
            newImage.createImage()
            img_URL = newImage.uploadImage()
            embedded = discord.Embed(title="Turnip Prediction", description="Your current turnip prediction",
                                     color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.set_image(url=img_URL)
            embedded.set_footer(text="Turnip Bot @ {}".format(datetime.datetime.now().strftime('%H:%M')))
            await ctx.send(embed=embedded)
        except AttributeError as e:
            await ctx.send("Failed to create image of summary >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return
        except Exception as e:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(ts.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return

    @commands.command(name='tst', help="Get your Turnip Summary for the next week as text\n"
                                       "This is built for people using screen readers, use <ts if you can",
                      aliases=['TurnipSummaryText', 'turnipsummarytext'])
    async def currentTurnipSummaryText(self, ctx):
        try:
            report = turnipCalculator.createCurrentSummary(ctx.message.author.id)
            reply = "Turnip Summary\n```"
            reply = reply + "    {:15} {:13} {:13} {:6}\n".format('Time', 'Price(Bells)', 'Likely(bells)', 'Odds(%)')
            for periods in report:
                reply = reply + "    {:15} {:13} {:13} {:6}\n".format(periods,
                                                                      report[periods]['price'],
                                                                      report[periods]['likely'],
                                                                      report[periods]['chance'])
            reply = reply + '```'
            await ctx.send(reply)
        except Exception as e:
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(ts.catch.rest)")
            return

    @commands.command(name='tsgraph',
                      help="Get your Turnip Summary Graph for the next week",
                      aliases=['tsg', 'turnipsummarygraph', 'turnipSummaryGraph'])
    async def tsgraph(self, ctx):
        try:
            report = turnipCalculator.createCurrentSummary(ctx.message.author.id)
            newImage = turnipSummaryImage.SummaryImage(report, ctx.message.author.id)
            newImage.createGraph()
            img_URL = newImage.uploadGraphImage()
            embedded = discord.Embed(title="Turnip Prediction Graph", description="Your current turnip prediction",
                                     color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.set_image(url=img_URL)
            embedded.set_footer(text="Turnip Bot @ {}".format(datetime.datetime.now().strftime('%H:%M')))
            await ctx.send(embed=embedded)
        except AttributeError as e:
            await ctx.send("Failed to create image of summary >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
        except Exception as e:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(ts.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return

    @commands.command(name='setBuyPrice',
                      help="Set the Price you bought the turnips for from Daisy Mae this week.\n"
                           "<bells> : The amount of bells each turnip cost.",
                      aliases=['setbuyprice', 'sbp'])
    async def setBuyPrice(self, ctx, bells):
        try:
            response = turnipCalculator.addPurchasePrice(ctx.message.author.id, bells)
        except Exception as error:
            await ctx.send(error)
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           error))
            return
        await ctx.send(response)


def setup(bot):
    bot.add_cog(Turnips(bot))
