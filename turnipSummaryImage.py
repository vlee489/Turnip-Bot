"""
This python script is reponsible for creating images for
a user's Turnip Summary and then uploading to AWS S3.
"""
from PIL import Image, ImageDraw, ImageFont
import auth
import boto3
from boto3.s3.transfer import S3Transfer
import datetime
import os

# Initiate session
session = boto3.session.Session()
client = session.client('s3', region_name=auth.aws_region_name, endpoint_url=auth.endpoint_url,
                        aws_access_key_id=auth.aws_access_key_id, aws_secret_access_key=auth.aws_secret_access_key)
transfer = S3Transfer(client)

font = ImageFont.truetype("files/Roboto-Regular.ttf", size=20)
subHeadingFont = ImageFont.truetype("files/Roboto-Regular.ttf", size=20)
headingFont = ImageFont.truetype("files/Roboto-Bold.ttf", size=24)
colour = '#99AAB5'
headingColour = '#FFFFFF'
subHeadingColour = '#CCD5DA'
x = 21
x2 = 150
x3 = 330


class SummaryImage:
    """
    Function for creating a summary Image
    """
    turnip_data = None
    discordID = None
    created = False

    def __init__(self, TurnipData, discordID) -> None:
        """
        Constructor
        :param TurnipData: dict
            The turnip data
        :param discordID: str
            the user's Discord ID
        """
        self.turnip_data = TurnipData
        self.discordID = discordID
        self.fileName = "{}-{}.png".format(discordID, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    def createImage(self) -> None:
        """
        Creates the image and saves it to temp location
        :return: None
            returns nothing
        """
        y = 55
        image = Image.open('files/Template.png')
        draw = ImageDraw.Draw(image)

        for periods in self.turnip_data:
            period = periods.replace("_", " ", 1)
            draw.text((x, y), period, fill=headingColour, font=headingFont)
            y = y + 25
            draw.text((x, y), "Price(Bells)", fill=subHeadingColour, font=subHeadingFont)
            draw.text((x2, y), "Likely Price(Bells)", fill=subHeadingColour, font=subHeadingFont)
            draw.text((x3, y), "Chance(%)", fill=subHeadingColour, font=subHeadingFont)
            y = y + 25
            draw.text((x, y), self.turnip_data[periods]['price'], fill=colour, font=font)
            draw.text((x2, y), self.turnip_data[periods]['likely'], fill=colour, font=font)
            draw.text((x3, y), self.turnip_data[periods]['chance'], fill=colour, font=font)

            y = y + 29

        image.save("tempHolding/{}".format(self.fileName), optimize=True, quality=20)
        self.created = True

    def uploadImage(self) -> str:
        """
        Uploads image to S3 bucket
        :return: str
            Link to the uploaded image
        """
        if not self.created:
            raise AttributeError("FIle Not created")
        client.upload_file("tempHolding/{}".format(self.fileName),
                           auth.aws_bucket,
                           "TurnipBot/predictions/{}".format(self.fileName),
                           ExtraArgs={'ACL': 'public-read'})
        os.remove("tempHolding/{}".format(self.fileName))
        return "{}/TurnipBot/predictions/{}".format(auth.CDNLink, self.fileName)
