"""
turnipCalculator.py

Contains all the functions for adding a user's turnip pricing to
the turnip Database as well as calculating turnip price trends.
"""
import json
import boto3
import auth
import turnips.meta
from boto3.dynamodb.conditions import Key
import decimal
import datetime

# Starts the dynamoDB connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(auth.turnipDB_Table)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def addData(discordID, date, time, bells):
    """
    adds Turnip Price data to the database
    :param discordID: str
        User's Discord User ID
    :param date: datetime
    The date to add the data for
    :param time: str
    the time of the turnip price, Either AM or PM
    :param bells: int
    the price of turnip sale
    :return: True if operation successful
    """
    # Works out the date for the beginning of the week
    date = date.date()
    beginningOfWeek = date - datetime.timedelta(days=date.weekday())
    day = date.strftime('%A')
    # Works out the field to place the data into.
    if time == 'AM':
        day = day + '_AM'
    elif time == 'PM':
        day = day + '_PM'
    else:
        raise AttributeError('In valid time operator')
    # Check that the day generated isn't Sunday
    if "Sunday" in day:
        raise ValueError("Sunday isn't valid, Daisy Mae visits then!")
    # Check is if an entry is already available for the user
    response = table.query(
        KeyConditionExpression=Key('discordID').eq(str(discordID)) &
                               Key('weekBegining').eq(str(beginningOfWeek.strftime('%d/%m/%Y')))
    )
    # If there isn't we create a new base entry to work from
    if len(response['Items']) == 0:
        table.put_item(
            Item={
                'discordID': str(discordID),
                'weekBegining': str(beginningOfWeek.strftime('%d/%m/%Y')),
                'timeline': {}
            }
        )
    # Then we update the entry available on database with the new turnip data
    table.update_item(
        Key={
            'discordID': str(discordID),
            'weekBegining': str(beginningOfWeek.strftime('%d/%m/%Y'))
        },
        UpdateExpression="set timeline.{} = :b".format(day),
        ExpressionAttributeValues={
            ':b': int(bells)
        },
        ReturnValues="UPDATED_NEW"
    )

    return True


def numericalTimeSlot(day):
    """
    Returns the numerical day of thr timeslot given
    :param day: str
        the day to turn into
    :return: int
        The corresponding numerical time slot
    """
    switch = {
        "Sunday_AM": 1,
        "Monday_AM": 2,
        "Monday_PM": 3,
        "Tuesday_AM": 4,
        "Tuesday_PM": 5,
        "Wednesday_AM": 6,
        "Wednesday_PM": 7,
        "Thursday_AM": 8,
        "Thursday_PM": 9,
        "Friday_AM": 10,
        "Friday_PM": 11,
        "Saturday_AM": 12,
        "Saturday_PM": 13
    }
    return switch.get(day, -1)


class TurnipClass:
    """
    A class for dealing with creating models and handing the model the data
    in the correct order.
    """
    Sunday_AM = None
    Monday_AM = None
    Monday_PM = None
    Tuesday_AM = None
    Tuesday_PM = None
    Wednesday_AM = None
    Wednesday_PM = None
    Thursday_AM = None
    Thursday_PM = None
    Friday_AM = None
    Friday_PM = None
    Saturday_AM = None
    Saturday_PM = None

    def addPrice(self, period, bells):
        """
        Add the price and period to objects
        :param period: int
            date period
        :param bells: int
            Sale price
        :return: boolean
            if successful
        """
        try:
            bells = int(bells)
        except ValueError:
            raise ValueError("Give bells as an Int")
        if period == 1:
            self.Sunday_AM = bells
        elif period == 2:
            self.Monday_AM = bells
        elif period == 3:
            self.Monday_PM = bells
        elif period == 4:
            self.Tuesday_AM = bells
        elif period == 5:
            self.Tuesday_PM = bells
        elif period == 6:
            self.Wednesday_AM = bells
        elif period == 7:
            self.Wednesday_PM = bells
        elif period == 8:
            self.Thursday_AM = bells
        elif period == 9:
            self.Thursday_PM = bells
        elif period == 10:
            self.Friday_AM = bells
        elif period == 11:
            self.Friday_PM = bells
        elif period == 12:
            self.Saturday_AM = bells
        elif period == 13:
            self.Saturday_PM = bells
        else:
            raise ValueError("period doesn't exist")
        return True

    def createModel(self):
        """
        Creates the model form the object fields
        :return: turnips.meta.MetaModel
            turnip model
        """
        if self.Sunday_AM is not None:
            turnipModel = turnips.meta.MetaModel.blank(self.Sunday_AM)
        else:
            turnipModel = turnips.meta.MetaModel.blank()

        if self.Monday_AM is not None:
            turnipModel.fix_price(2, self.Monday_AM)
        if self.Monday_PM is not None:
            turnipModel.fix_price(3, self.Monday_PM)
        if self.Tuesday_AM is not None:
            turnipModel.fix_price(4, self.Tuesday_AM)
        if self.Tuesday_PM is not None:
            turnipModel.fix_price(5, self.Tuesday_PM)
        if self.Wednesday_AM is not None:
            turnipModel.fix_price(6, self.Wednesday_AM)
        if self.Wednesday_PM is not None:
            turnipModel.fix_price(7, self.Wednesday_PM)
        if self.Thursday_AM is not None:
            turnipModel.fix_price(8, self.Thursday_AM)
        if self.Thursday_PM is not None:
            turnipModel.fix_price(9, self.Thursday_PM)
        if self.Friday_AM is not None:
            turnipModel.fix_price(10, self.Friday_AM)
        if self.Friday_PM is not None:
            turnipModel.fix_price(11, self.Friday_PM)
        if self.Saturday_AM is not None:
            turnipModel.fix_price(12, self.Saturday_AM)
        if self.Saturday_PM is not None:
            turnipModel.fix_price(13, self.Saturday_PM)

        return turnipModel


def createTurnipModel(discordID, date):
    """
    Creates the turnip model for a user at a specified week
    :param discordID: str
        the User's Discord ID
    :param date: dateTime
        The date of the week you want to look for
    :return: turnip.model
        The turnip model for the specified date and user
    """
    date = date.date()
    beginningOfWeek = date - datetime.timedelta(days=date.weekday())

    response = table.query(
        KeyConditionExpression=Key('discordID').eq(str(discordID)) &
                               Key('weekBegining').eq(str(beginningOfWeek.strftime('%d/%m/%Y')))
    )

    if len(response['Items']) == 0:
        raise AttributeError("No data available to make model")
    elif len(response['Items']) > 1:
        raise LookupError("System Error, more than one response returned")

    # Create blank object to hold data
    turnipInstance = TurnipClass()

    i = response['Items'][0]
    for day in i['timeline']:
        turnipInstance.addPrice(numericalTimeSlot(str(day)), int(i['timeline'][day]))

    turnipModel = turnipInstance.createModel()
    return turnipModel


def addBuyPrice(discordID, date, bells):
    """
    Ass the buying of turnips price to DB
    :param discordID: str
        user's DiscordID
    :param date: datetime
        the date of when the turnips where bought
    :param bells: int
        The cost of the turnips
    :return: boolean
        if successful
    """
    # Works out the date for the beginning of the week
    if date.strftime('%A') == 'Sunday':
        date = date + datetime.timedelta(days=2)
    date = date.date()
    beginningOfWeek = date - datetime.timedelta(days=date.weekday())
    day = 'Sunday_AM'

    # Check is if an entry is already available for the user
    response = table.query(
        KeyConditionExpression=Key('discordID').eq(str(discordID)) &
                               Key('weekBegining').eq(str(beginningOfWeek.strftime('%d/%m/%Y')))
    )
    # If there isn't we create a new base entry to work from
    if len(response['Items']) == 0:
        table.put_item(
            Item={
                'discordID': str(discordID),
                'weekBegining': str(beginningOfWeek.strftime('%d/%m/%Y')),
                'timeline': {
                    'Sunday_AM': int(bells)
                }
            }
        )
        return True
    # Then we update the entry available on database with the new turnip data
    table.update_item(
        Key={
            'discordID': str(discordID),
            'weekBegining': str(beginningOfWeek.strftime('%d/%m/%Y'))
        },
        UpdateExpression="set timeline.{} = :b".format(day),
        ExpressionAttributeValues={
            ':b': int(bells)
        },
        ReturnValues="UPDATED_NEW"
    )
    return True


"""
Any thing belows this deals directly with commands from main.py
"""


def createCurrentSummary(discordID):
    """
    Creates the Turnip Summary for the last week
    :param discordID: str
        DiscordID for the person to check for
    :return: str
        The summary report
    """
    date = datetime.datetime.now()

    try:
        model = createTurnipModel(discordID, date)
        return model.summary()
    except AttributeError:
        raise Exception("No data available to make model")
    except LookupError:
        raise Exception("Internal Error, sorry >.< \n Issue has been reported to operator. \n (Too Many Responses)")


def addSpecifiedData(discordID, date, time, bells):
    """
    Allows for adding data on a specific date and time
    :param discordID: str
        User's discordID
    :param date: str
        Date to add the data for
    :param time: str
        Time to add the data for in either PM or AM
    :param bells: str
        The sale price
    :return:
        Success message
    """
    try:
        date = datetime.datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        raise Exception("Date format incorrect")
    time = time.upper()  # Turns the time given into Uppercase
    if not bells.isdigit():
        raise Exception("Bells must be given as a number! E.g 1-9")
    elif time == 'AM' or time == 'PM':
        try:
            if addData(discordID, date, time, bells):
                return "Added price of {} bells for {} at {}".format(bells,
                                                                     date.strftime('%d/%m/%Y'),
                                                                     time)
        except AttributeError:
            raise Exception("Time given to internal system was Invalid! \n"
                            "Has to be either `AM` or `PM`")
        except ValueError:
            raise Exception("You can't give me a time for Sunday!\n")
    else:
        raise Exception("Time isn't correct, has to be either `AM` or `PM`")


def addPurchasePrice(discordID, bells):
    """
    Add the turnip price to the DB
    :param discordID: str
        User's discordID
    :param bells: int
        The cost of turnips
    :return: boolean
        if successful
    """
    if not bells.isdigit():
        raise Exception("Bells must be given as a number! E.g 1-9")
    try:
        addBuyPrice(discordID, datetime.datetime.now(), bells)
        return "Added purchase price of {} bells from Daisy Mae".format(bells)
    except:
        raise Exception("Internal Error, sorry >.< \n Issue has been reported to operator. \n (Uncaught Exception)")

# model = createTurnipModel(113026708071821312, datetime.datetime.now())
# print(model.summary())
