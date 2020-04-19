"""
turnipCalculator.py

Contains all the functions for adding a user's turnip pricing to
the turnip Database as well as calculating turnip price trends.
"""
import json
import boto3
import auth
import turnips
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
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
    # Check that the day generated isn't Sunday Morning
    if day == 'Sunday_AM':
        raise ValueError("Sunday AM isn't valid, Daisy Mae visits then!")
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

