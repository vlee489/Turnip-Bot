"""
Deals with allowing suers to set their timezone
for date dependent
"""
import datetime
import boto3
import pendulum
from boto3.dynamodb.conditions import Key
import csv
import errors

session = boto3.Session(profile_name='default')


class Timezoner:
    def __init__(self, dbName: str):
        self.validList = []
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(dbName)
        with open("zone.csv", 'r') as zoneFile:
            reader = csv.DictReader(zoneFile)
            for row in reader:
                self.validList.append(row["Zone-Name"])

    def addTimezone(self, discordID: str, timezone: str) -> bool:
        """
        Add a user's timezone to the database
        :param discordID: str
            User's Discord ID
        :param timezone: str
            A valid time zone
        :return: bool
            True is added successfully, else false
        """
        timezone = timezone.title()
        if timezone in self.validList:
            try:
                response = self.table.query(
                    KeyConditionExpression=Key('discordID').eq(str(discordID))
                )
                if len(response['Items']) == 0:
                    self.table.put_item(
                        Item={
                            'discordID': str(discordID),
                            'tz': str(timezone)
                        }
                    )
                    return True
                self.table.update_item(
                    Key={
                        'discordID': str(discordID),
                    },
                    UpdateExpression="set tz = :b",
                    ExpressionAttributeValues={
                        ':b': str(timezone)
                    },
                    ReturnValues="UPDATED_NEW"
                )
                return True
            except Exception as e:
                raise errors.AWSError(e)
        else:
            return False

    def getCurrentDatetime(self, discordID: str) -> datetime:
        try:
            response = self.table.query(
                KeyConditionExpression=Key('discordID').eq(str(discordID))
            )
            if len(response['Items']) > 0:
                i = response['Items'][0]
                if "tz" in i:
                    return pendulum.now(i["tz"])
            return pendulum.now("Europe/London")
        except Exception as e:
            raise errors.AWSError(e)
