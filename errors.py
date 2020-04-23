"""
This file contains errors thrown by Turnip Bot internally
"""


class EndPointValidation(Exception):
    """
    Raised when an invalid API endpoint is given
    """
    pass


class InvalidAPICall(Exception):
    """
    Raised when an invalid API returns something other than 200
    """
    pass


class FileNotCreated(Exception):
    """
    Raised when a requested file to upload hasn't been created
    """
    pass


class AWSError(Exception):
    """
    For catching AWS error like S3 and dynamoDB
    """
    pass


class InvalidDateTime(Exception):
    """
    For catching invalid date/time
    """
    pass


class InvalidPeriod(Exception):
    """
    Raised when an invalid period is given
    """
    pass


class InvalidDateFormat(Exception):
    """
    Raised when an invalid date format is given
    """
    pass

class BellsOutOfRange(Exception):
    """
    Raised when the value in bells is out of range
    """
    pass

class NoData(Exception):
    """
    Raised when there's no data to work with
    """
    pass

