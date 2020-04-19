"""
This file contains all the main event handlers for the
Turnip Bot. All the functions are separated into their own
python classes.
"""

import auth
from discord.ext import commands
import random
import turnipCalculator
import datetime

TOKEN = auth.discord_Token
bot = commands.Bot(command_prefix='>')


@bot.command(name='ap', help="Adds today's price to the turnip  "
                             "\n <Time> Either PM or AM "
                             "\n <bells> The bells you get for selling turnips")
async def addTurnipPrice(ctx, time, bells):
    """
    This function adds the user's turnip price to the database
    :param ctx: command object
    :param time: the PM/AM time from the user
    :param bells: The bells from the user
    :return: nothing
    """
    response = "An Error Has Occured!"
    time = time.upper()  # Turns the time given into Uppercase
    if not bells.isdigit():
        response = "Bells must be given as a number! E.g 1-9"
    elif time == 'AM' or time == 'PM':
        try:
            if turnipCalculator.addData(ctx.message.author.id, datetime.datetime.now(), time, bells):
                response = "Added price of {} bells for {} at {}".format(bells,
                                                                         (datetime.datetime.now()).strftime('%d/%m/%Y'),
                                                                         time)
        except AttributeError:
            response = "Time given to internal system was Invalid\n" \
                       "Has to be either `AM` or `PM`"
        except ValueError:
            response = "You can't give me a time for Sunday Morning!\n" \
                       "That's when Daisy Mae visits ejjit!"
    else:
        response = "Time isn't correct, has to be either `AM` or `PM`"

    await ctx.send(response)

bot.run(TOKEN)
