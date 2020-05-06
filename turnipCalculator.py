"""
turnipCalculator.py

Contains all the functions for adding a user's turnip pricing to
the turnip Database as well as calculating turnip price trends.
"""
import boto3
import turnips.meta
from boto3.dynamodb.conditions import Key
import datetime
import errors
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Starts the dynamoDB connection
session = boto3.Session(profile_name='default')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get("turnipDB_Table"))


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
        raise errors.InvalidDateTime('Invalid time operator')
    # Check that the day generated isn't Sunday
    if "Sunday" in day:
        raise errors.InvalidPeriod()
    try:
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
    except Exception:
        raise errors.AWSError("Unable to interface with backend")
    return True


def numericalTimeSlot(day) -> int:
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


def timeSlotToStr(timeSlot) -> str:
    """
    Returns the time slot str from a numerical time slot
    :param timeSlot: int
        Time slot between 1-13
    :return: str
        The string for the time slot it is
    """
    switch = {
        1: "Sunday_AM",
        2: "Monday_AM",
        3: "Monday_PM",
        4: "Tuesday_AM",
        5: "Tuesday_PM",
        6: "Wednesday_AM",
        7: "Wednesday_PM",
        8: "Thursday_AM",
        9: "Thursday_PM",
        10: "Friday_AM",
        11: "Friday_PM",
        12: "Saturday_AM",
        13: "Saturday_PM"
    }
    return switch.get(timeSlot, "Invalid")


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
        raise errors.NoData("No data available to make model")
    elif len(response['Items']) > 1:
        raise errors.AWSError("System Error, more than one response returned")
        # A lookup error should in theory never happen because discordID and weekBegining as tied together
        # as a dual pair key, so each set of data requires both attributes to exist and one the combo can only
        # exist in one entry together

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
    if date.strftime('%A') == 'Sunday':  # If it's a sunday we need to save the price for the next week actually
        date = date + datetime.timedelta(days=2)  # So we work out the next week.
    date = date.date()
    beginningOfWeek = date - datetime.timedelta(days=date.weekday())
    day = 'Sunday_AM'
    if int(bells) < 90 or int(bells) > 110:
        raise errors.BellsOutOfRange("Purchase price must be between 90-110 bells")
    try:
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
    except Exception as e:
        raise errors.AWSError(e)

    return True


def clearErrors(discordID, date) -> str:
    """
    Attempts to remove data causing errors from Database
    :param date: datetime
        The datetime to correct for
    :param discordID: str
        The user's Discord ID
    :return: str
        The list of day/times removes
    """
    # Work out the beginning of the week
    beginningOfWeek = date - datetime.timedelta(days=date.weekday())
    # We check if we actually need to fix errors by making sure data already present can't produce a report
    try:
        if bool((createTurnipModel(discordID, datetime.datetime.now()).summary())) is True:
            raise errors.DataCorrect("Nothing to correct")
    except AttributeError:
        raise errors.NoData("No data available to make model")
    except LookupError as e:
        raise errors.InternalError(e)
    # We query the DB for the current copy of the data
    response = table.query(
        KeyConditionExpression=Key('discordID').eq(str(discordID)) &
                               Key('weekBegining').eq(str(beginningOfWeek.strftime('%d/%m/%Y')))
    )
    if len(response['Items']) == 0:
        raise errors.NoData("No data available to make model")
    elif len(response['Items']) > 1:
        raise errors.InternalError("Too Many Responses")
    # we take the response and for each day we turn it into it's numerical id
    dates = []
    removedDates = []
    i = response['Items'][0]
    for day in i['timeline']:  # for each day in the response
        timeSlot = numericalTimeSlot(str(day))
        if timeSlot != 1:
            dates.append(timeSlot)
    dates.sort()  # Sort numerical dates out in order
    for x in range(len(dates)):  # for each date in the list
        lastDate = dates.pop()  # pop date
        removedDates.append(timeSlotToStr(lastDate).replace("_", " "))  # add it to the list of removed dates
        try:
            # We remove that date we popped from the the DB
            table.update_item(
                Key={
                    'discordID': str(discordID),
                    'weekBegining': str(beginningOfWeek.strftime('%d/%m/%Y'))
                },
                UpdateExpression="Remove timeline.{}".format(timeSlotToStr(lastDate)),
                ReturnValues="UPDATED_NEW"

            )
        except Exception as e:
            raise errors.AWSError(e)
        # We then check if we can then create a model.
        if bool((createTurnipModel(discordID, datetime.datetime.now()).summary())) is True:
            # if we can create a model, then we break
            break
        # if not the loop continues to remove dates in order till we can create a model
    # if we finish the loop, then we return all the dates removed.
    strReply = ""
    for date in removedDates:
        strReply = strReply + "{}, ".format(date)
    return strReply
    # We don't remove the Sunday_AM reference because we error check that value
    # before it's entered anyway so will always be within range being the first value


def deleteTurnipData(discordID: str) -> int:
    """
    Delete all turnip data from a given user
    :param discordID: str
        Discord ID of the User we want to delete turnip data for
    :return: bool
        If the operation was successful or not
    """
    deleteCount = 0
    try:
        # We query the DB for all the entries the user has made, so we can get the sort key needed to delete items
        response = table.query(
            KeyConditionExpression=Key('discordID').eq(str(discordID))
        )
        if response['Count'] <= 0:
            raise errors.NoData("No data in database")
        else:
            for entries in response['Items']:
                deleteResponse = table.delete_item(
                    Key={
                        'discordID': discordID,
                        'weekBegining': entries['weekBegining']
                    }
                )
                if deleteResponse["ResponseMetadata"]['HTTPStatusCode'] != 200:
                    raise errors.AWSError("Unable to delete entry")
                else:
                    deleteCount = deleteCount + 1
    except Exception as e:
        pass
    return deleteCount
