"""
Contains the cog for the turnip commands.
"""
from discord.ext import commands
import turnipCalculator
import datetime
import turnipSummaryImage
import discord
import errors
import timezoner

getDateAcquirer = timezoner.Timezoner("userData")


def getDate(date: str, discordID: str) -> datetime:
    try:
        if date == "Today":
            date = getDateAcquirer.getCurrentDatetime(discordID)
        else:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        raise errors.InvalidDateFormat
    return date


class Turnips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ap', help="Adds price to the turnip price storage"
                                      "\n<Time> : Either PM or AM "
                                      "\n<bells> : The bells you get for selling turnips"
                                      "\n[date]: OPTIONAL the date you want to enter price for in DD/MM/YYYY",
                      aliases=['AddPrice', 'addprice'])
    async def addTurnipPrice(self, ctx, time, bells, date="Today"):
        response = "An Error Has Occurred!"
        time = time.upper()  # Turns the time given into Uppercase
        if not bells.isdigit():
            response = "Bells must be given as a number! E.g 1-9"
        elif time == 'AM' or time == 'PM':
            try:
                date = getDate(date, ctx.message.author.id)
                if turnipCalculator.addData(ctx.message.author.id, date, time, bells):
                    response = "Added price of {} bells for {} at {}".format(bells,
                                                                             date.strftime('%d/%m/%Y'),
                                                                             time)
            except errors.InvalidDateTime:
                response = "Time given to internal system was Invalid\n" \
                           "Has to be either `AM` or `PM`"
            except errors.InvalidPeriod:
                response = "You can't give me a time and price for Sunday!"
            except errors.InvalidDateFormat:
                await ctx.send("Error: Invalid Date format given")
            except errors.AWSError as error:
                response = "Unable to store data!\nError been reported to operator"
                print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                               datetime.datetime.now(),
                                                                               error))
            except Exception as e:
                response = "Internal Error, sorry >.<\nIssue has been reported to operator.\n(ap.catch.rest)"
                print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                               datetime.datetime.now(),
                                                                               e))
        else:
            response = "Time isn't correct, has to be either `AM` or `PM`"
        await ctx.send(response)

    @commands.command(name='ts', help="Get your Turnip Summary"
                                      "\n[date]: OPTIONAL Get your summary for a specific week in DD/MM/YYYY",
                      aliases=['TurnipSummary', 'turnipsummary'])
    async def currentTurnipSummary(self, ctx, date="Today"):
        try:
            date = getDate(date, ctx.message.author.id)
            date = date + datetime.timedelta(days=1)
            report = turnipCalculator.createTurnipModel(ctx.message.author.id, date).summary()
            if bool(report) is False:
                await ctx.send("Failed to create a report with data provided\n"
                               "You've given some invalid bell amount somewhere\n"
                               "You can run `<removeInvalidData` to try and fix this issue\n"
                               "There's a guide to help fix this at https://bit.ly/turnipBot")
                print("REPORT ERROR:\nDiscordID: {}\nTime:{}\n-----".format(ctx.message.author.id,
                                                                            datetime.datetime.now(), ))
                return
            newImage = turnipSummaryImage.SummaryImage(report, ctx.message.author.id)
            newImage.createImage()
            img_URL = newImage.uploadImage()
            embedded = discord.Embed(title="Turnip Prediction", description="Your current turnip prediction",
                                     color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            embedded.set_image(url=img_URL)
            embedded.set_footer(text="Turnip Bot", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            embedded.timestamp = datetime.datetime.now()
            await ctx.send(embed=embedded)
        except errors.FileNotCreated as e:
            await ctx.send("Failed to create image of summary >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return
        except errors.AWSError as e:
            await ctx.send("Failed to upload image >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
        except errors.NoData:
            await ctx.send("No Data to create model with\n "
                           "So your prices will be somewhere between 0 to 700.\n"
                           "Use `<ap` and/or `<setBuyPrice` to get started!")
        except errors.InvalidDateFormat:
            await ctx.send("Error: Invalid Date format given")
        except Exception as e:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(ts.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return

    @commands.command(name='tst', help="Get your Turnip Summary as text\n"
                                       "This is built for people using screen readers, use <ts if you can"
                                       "\n[date]: OPTIONAL Get your summary for a specific week in DD/MM/YYYY",
                      aliases=['TurnipSummaryText', 'turnipsummarytext'])
    async def currentTurnipSummaryText(self, ctx, date="Today"):
        try:
            date = getDate(date, ctx.message.author.id)
            date = date + datetime.timedelta(days=1)
            report = turnipCalculator.createTurnipModel(ctx.message.author.id, date).summary()
            if bool(report) is False:
                await ctx.send("Failed to create a report with data provided\n"
                               "You've given some invalid bell amount somewhere\n"
                               "You can run `<removeInvalidData` to try and fix this issue\n"
                               "There's a guide to help fix this at https://bit.ly/turnipBot")
                print("REPORT ERROR:\nDiscordID: {}\nTime:{}\n-----".format(ctx.message.author.id,
                                                                            datetime.datetime.now(), ))
                return
            reply = "Turnip Summary\n```"
            reply = reply + "    {:15} {:13} {:13} {:6}\n".format('Time', 'Price(Bells)', 'Likely(bells)', 'Odds(%)')
            for periods in report:
                reply = reply + "    {:15} {:13} {:13} {:6}\n".format(periods,
                                                                      report[periods]['price'],
                                                                      report[periods]['likely'],
                                                                      report[periods]['chance'])
            reply = reply + '```'
            await ctx.send(reply)
        except errors.NoData:
            await ctx.send("No Data to create model with\n "
                           "So your prices will be somewhere between 0 to 700.\n"
                           "Use `<ap` and/or `<setBuyPrice` to get started!")
        except errors.AWSError as e:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(ts.AWS)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
        except errors.InvalidDateFormat:
            await ctx.send("Error: Invalid Date format given")
        except Exception as e:
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(ts.catch.rest)")
            return

    @commands.command(name='tsgraph',
                      help="Get your Turnip Summary Graph"
                           "\n[date]: OPTIONAL Get your summary for a specific week in DD/MM/YYYY",
                      aliases=['tsg', 'turnipsummarygraph', 'turnipSummaryGraph'])
    async def tsgraph(self, ctx, date="Today"):
        try:
            date = getDate(date, ctx.message.author.id)
            date = date + datetime.timedelta(days=1)
            report = turnipCalculator.createTurnipModel(ctx.message.author.id, date).summary()
            if bool(report) is False:
                await ctx.send("Failed to create a report with data provided\n"
                               "You've given some invalid bell amount somewhere\n"
                               "You can run `<removeInvalidData` to try and fix this issue\n"
                               "There's a guide to help fix this at https://bit.ly/turnipBot")
                print("REPORT ERROR:\nDiscordID: {}\nTime:{}\n-----".format(ctx.message.author.id,
                                                                            datetime.datetime.now(), ))
                return
            newImage = turnipSummaryImage.SummaryImage(report, ctx.message.author.id)
            newImage.createGraph()
            img_URL = newImage.uploadGraphImage()
            embedded = discord.Embed(title="Turnip Prediction Graph", description="Your current turnip prediction",
                                     color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            embedded.set_image(url=img_URL)
            embedded.set_footer(text="Turnip Bot", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            embedded.timestamp = datetime.datetime.now()
            await ctx.send(embed=embedded)
        except errors.FileNotCreated as e:
            await ctx.send("Failed to create image of summary >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
        except errors.AWSError as e:
            await ctx.send("Failed to upload image >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
        except errors.NoData:
            await ctx.send("No Data to create model with\n "
                           "So your prices will be somewhere between 0 to 700.\n"
                           "Use `<ap` and/or `<setBuyPrice` to get started!")
        except errors.InvalidDateFormat:
            await ctx.send("Error: Invalid Date format given")
        except Exception as e:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(tsg.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return

    @commands.command(name='setBuyPrice',
                      help="Set the Price you bought the turnips for from Daisy Mae this week.\n"
                           "This should be the price from YOUR OWN ISLAND!!!"
                           "\n<bells>: The amount of bells each turnip cost."
                           "\n[date]: OPTIONAL Set a price for a specific week in DD/MM/YYYY",
                      aliases=['setbuyprice', 'sbp'])
    async def setBuyPrice(self, ctx, bells, date="Today"):
        if not bells.isdigit():
            await ctx.send("Bells must be given as a number! E.g 1-9")
            return
        try:
            date = getDate(date, ctx.message.author.id)
            turnipCalculator.addBuyPrice(ctx.message.author.id, date, bells)
            await ctx.send("Added purchase price of {} bells from Daisy Mae on {}".format(bells,
                                                                                          date.strftime("%d/%m/%Y")))
        except errors.BellsOutOfRange as e:
            await ctx.send("Purchase price must be between 90-110 bells")
            return
        except errors.InvalidDateFormat:
            await ctx.send("Error: Invalid Date format given")
        except Exception as error:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(sbp.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           error))
            return

    @commands.command(name='removeInvalidData',
                      help="Attempts to find and remove invalid data to make your turnip summary generate.\n",
                      aliases=["correctErrors", "removeinvaliddata", 'rid'])
    async def correctErrors(self, ctx, date="Today"):
        try:
            date = getDate(date, ctx.message.author.id)
            removedDate = turnipCalculator.clearErrors(ctx.message.author.id, date)
            await ctx.send("I've removed all the data that was causing an error now!\n"
                           "You should be able to run summary commands again now.\n"
                           "The following days have been removed.\n"
                           "{}".format(removedDate))
        except errors.AWSError as e:
            await ctx.send("Failed to access dataStore >.<\n "
                           "Issue has been reported to operator.\n")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
        except errors.DataCorrect:
            await ctx.send("Data is already correct and can create a summary\n")
        except errors.NoData:
            await ctx.send("No Data to create model with\n")
        except errors.InternalError as error:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(rid.tooManyResponses)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           error))
        except Exception as error:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(rid.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           error))

    @commands.command(name='removePrice', help="Remove a price from turnip price storage"
                                               "\n<Time> : Either PM or AM "
                                               "\n<date> : The date you want to enter price for in DD/MM/YYYY",
                      aliases=['RemovePrice', 'rp', 'removeprice'])
    async def removePrice(self, ctx, time, date):
        time = time.upper()  # Turns the time given into Uppercase
        try:
            date = getDate(date, ctx.message.author.id)
            responseBool = turnipCalculator.removePrice(str(ctx.message.author.id), date, time)
            if responseBool:
                await ctx.send("We have removed the the entry for {} on {}".format(time, date.strftime("%d/%m/%Y")))
                return
            else:
                await ctx.send("We where **Unable** to remove the entry for {} on {} "
                               "\nLikely doesn't exist".format(time, date.strftime("%d/%m/%Y")))
                return
        except errors.InvalidDateTime:
            await ctx.send("Error: Invalid date given!")
        except errors.InvalidDateFormat:
            await ctx.send("Error: Invalid Date format given")
        except errors.AWSError:
            await ctx.send("There was an error getting to the database")

    @commands.command(name='getPrice', help="View the prices you have given to Turnip Bot"
                                             "\n[date]: OPTIONAL Set a price for a specific week in DD/MM/YYYY",
                      aliases=['gp', 'GetPrice', 'getprice'])
    async def viewPrice(self, ctx, date="Today"):
        try:
            date = getDate(date, ctx.message.author.id)
            printOut = "```\n"
            prices = turnipCalculator.getPrices(str(ctx.message.author.id), date)
            for items in prices:
                printOut = printOut + "{:16}: {:4}\n".format(items, prices[items])
            printOut = printOut + "```"
            embedded = discord.Embed(title="Turnip Price List", description="The Turnip Prices you've given",
                                     color=0xCF70D3)
            embedded.set_author(name="Turnip Bot",
                                url="https://github.com/vlee489/Turnip-Bot/",
                                icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            embedded.add_field(name="Price on file:", value=printOut, inline=False)
            embedded.set_footer(text="Turnip Bot", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
            embedded.timestamp = datetime.datetime.now()
            await ctx.send(embed=embedded)
        except errors.InvalidDateFormat:
            await ctx.send("Error: Invalid Date Format")

    @commands.command(name='setTimezone', help="Set your default timezone"
                                               "\n<timezone>: The TZ database name of your timezone"
                                               "\nA list of valid TZ dataabse names are at "
                                               "https://bit.vlee.me.uk/TZ",
                      aliases=['SetTimezone', 'settimezone'])
    async def setTimezone(self, ctx, timezone):
        try:
            response = getDateAcquirer.addTimezone(ctx.message.author.id, timezone)
            if response:
                await ctx.send("Set your timezone to {}".format(timezone.title()))
            else:
                await ctx.send("Timezone your provided was invalid, please choose a valid timezone,\n"
                               "from https://bit.vlee.me.uk/TZ")
            return
        except errors.AWSError:
            await ctx.send("Couldn't add your timezone, try again later.")


def setup(bot):
    bot.add_cog(Turnips(bot))
