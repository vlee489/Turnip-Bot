"""
Contains the cog for the turnip commands.
"""
from discord.ext import commands
import turnipCalculator
import datetime
import turnipSummaryImage
import discord
import errors


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
                if date == "Today":
                    date = datetime.datetime.now()
                else:
                    date = datetime.datetime.strptime(date, '%d/%m/%Y')
                if turnipCalculator.addData(ctx.message.author.id, date, time, bells):
                    response = "Added price of {} bells for {} at {}".format(bells,
                                                                             date.strftime('%d/%m/%Y'),
                                                                             time)
            except errors.InvalidDateTime:
                response = "Time given to internal system was Invalid\n" \
                           "Has to be either `AM` or `PM`"
            except errors.InvalidPeriod:
                response = "You can't give me a time and price for Sunday!"
            except ValueError:
                raise errors.InvalidDateFormat("Date format incorrect")
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

    @commands.command(name='addTurnipPrice', help="No longer used, use <ap instead instead with data at end\n",
                      aliases=['atp', 'addturnipprice'])
    async def addSpecificPrice(self, ctx):
        await ctx.send("This commands has now been deprecated/No Longer Used!\n"
                       "You can now use `<ap time(AM/PM) bells date(DD/MM/YYYY)`")

    @commands.command(name='ts', help="Get your Turnip Summary"
                                      "\n[date]: OPTIONAL Get your summary for a specific week in DD/MM/YYYY",
                      aliases=['TurnipSummary', 'turnipsummary'])
    async def currentTurnipSummary(self, ctx, date="Today"):
        try:
            if date == "Today":
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            date = date + datetime.timedelta(days=1)
            report = turnipCalculator.createTurnipModel(ctx.message.author.id, date).summary()
            if bool(report) is False:
                await ctx.send("Failed to create a report with data provided\n"
                               "You've given some invalid bell amount somewhere\n"
                               "You can run `<removeInvalidData` to try and fix this issue")
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
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.set_image(url=img_URL)
            embedded.set_footer(text="Turnip Bot : {}".format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')))
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
        except ValueError:
            raise errors.InvalidDateFormat("Date format incorrect")
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
            if date == "Today":
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            date = date + datetime.timedelta(days=1)
            report = turnipCalculator.createTurnipModel(ctx.message.author.id, date).summary()
            if bool(report) is False:
                await ctx.send("Failed to create a report with data provided\n"
                               "You've given some invalid bell amount somewhere\n"
                               "You can run `<removeInvalidData` to try and fix this issue")
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
        except ValueError:
            raise errors.InvalidDateFormat("Date format incorrect")
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
            if date == "Today":
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            date = date + datetime.timedelta(days=1)
            report = turnipCalculator.createTurnipModel(ctx.message.author.id, date).summary()
            if bool(report) is False:
                await ctx.send("Failed to create a report with data provided\n"
                               "You've given some invalid bell amount somewhere\n"
                               "You can run `<removeInvalidData` to try and fix this issue")
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
                                icon_url="https://vleedn.fra1.cdn.digitaloceanspaces.com/TurnipBot/icon.png")
            embedded.set_image(url=img_URL)
            embedded.set_footer(text="Turnip Bot : {}".format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')))
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
        except ValueError:
            raise errors.InvalidDateFormat("Date format incorrect")
        except Exception as e:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(tsg.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           e))
            return

    @commands.command(name='setBuyPrice',
                      help="Set the Price you bought the turnips for from Daisy Mae this week."
                           "\n<bells>: The amount of bells each turnip cost."
                           "\n[date]: OPTIONAL Set a price for a specific week in DD/MM/YYYY",
                      aliases=['setbuyprice', 'sbp'])
    async def setBuyPrice(self, ctx, bells, date="Today"):
        if not bells.isdigit():
            await ctx.send("Bells must be given as a number! E.g 1-9")
            return
        try:
            if date == "Today":
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            turnipCalculator.addBuyPrice(ctx.message.author.id, date, bells)
            await ctx.send("Added purchase price of {} bells from Daisy Mae on {}".format(bells, date))
        except errors.BellsOutOfRange as e:
            await ctx.send("Purchase price must be between 90-110 bells")
            return
        except ValueError:
            raise errors.InvalidDateFormat("Date format incorrect")
        except Exception as error:
            await ctx.send("Internal Error, sorry >.<\n "
                           "Issue has been reported to operator.\n"
                           "(sbp.catch.rest)")
            print("ERROR:\nDiscordID: {}\nTime:{}\nError:{}\n-----".format(ctx.message.author.id,
                                                                           datetime.datetime.now(),
                                                                           error))
            return

    @commands.command(name='removeInvalidData',
                      help="Helps find and remove invalid data from to make your turnip summary generate.\n",
                      aliases=["correctErrors", "removeinvaliddata", 'rid'])
    async def correctErrors(self, ctx, date="Today"):
        if date == "Today":
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
        try:
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


def setup(bot):
    bot.add_cog(Turnips(bot))
