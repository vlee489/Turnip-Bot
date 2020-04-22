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