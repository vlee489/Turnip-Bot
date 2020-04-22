"""
This python script is responsible for creating images for
a user's Turnip Summary and then uploading to AWS S3.
"""
from PIL import Image, ImageDraw, ImageFont
import auth
import boto3
import botocore.config as bcc
from boto3.s3.transfer import S3Transfer
import botocore.exceptions as be
import datetime
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import errors

# Initiate session
# Config to limit retry attempts
boto3Config = bcc.Config(connect_timeout=5, read_timeout=60, retries={'max_attempts': 1})
session = boto3.session.Session()
client = session.client('s3', region_name=auth.aws_region_name, endpoint_url=auth.endpoint_url,
                        aws_access_key_id=auth.aws_access_key_id, aws_secret_access_key=auth.aws_secret_access_key,
                        config=boto3Config)
transfer = S3Transfer(client)

# Colour and Font constants
font = ImageFont.truetype("files/RobotoRegular.ttf", size=20)
subHeadingFont = ImageFont.truetype("files/RobotoRegular.ttf", size=20)
headingFont = ImageFont.truetype("files/RobotoBold.ttf", size=24)
percentFont = ImageFont.truetype("files/RobotoRegular.ttf", size=18)
colour = '#99AAB5'
headingColour = '#FFFFFF'
subHeadingColour = '#CCD5DA'
# Constants for turnip Summary X locations
x = 21
x2 = 150
x3 = 330
# Configure constants for matplotlib
# Tells matplotlib to use different graphic engine, as we don't have a Xorg instance for it to use
matplotlib.use('Agg')
# Set colours
matplotlib.rcParams['text.color'] = colour
matplotlib.rcParams['axes.labelcolor'] = colour
matplotlib.rcParams['xtick.color'] = subHeadingColour
matplotlib.rcParams['ytick.color'] = subHeadingColour
# set font from ttf
prop = fm.FontProperties(fname="files/RobotoRegular.ttf")
matplotlib.rc('axes', edgecolor=headingColour)
basewidth = 658  # Location of where the &ages line up on the graph image


class SummaryImage:
    """
    Function for creating a summary Image
    """
    turnip_data = None
    discordID = None
    created = False
    graphCreated = False

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
        y = 55  # Y Location
        # Load in image and create draw function on image
        image = Image.open('files/Template.png')
        draw = ImageDraw.Draw(image)

        for periods in self.turnip_data:
            # for all the data we add in the dict it to the image
            period = periods.replace("_", " ", 1)  # remove the dash, so it looks nicer
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

    def createGraph(self) -> None:
        """
        Creates Graph from dict
        :return: None
            Nothing is returned
        """
        # This creates the lists with all the data to form the graph.
        priceLower = []
        priceUpper = []
        likelyLower = []
        likelyUpper = []
        xAxisLabels = []
        for periods in self.turnip_data:
            # break up the price
            if " - " in self.turnip_data[periods]['price']:
                elements = (self.turnip_data[periods]['price']).split(" - ", 1)
                priceLower.append(int(elements[0]))
                priceUpper.append(int(elements[1]))
            else:  # Some done have - as they so in this case we just add the one number to both lists
                priceLower.append(int(self.turnip_data[periods]['price']))
                priceUpper.append(int(self.turnip_data[periods]['price']))
            # Do the same again but for the likely price
            if " - " in self.turnip_data[periods]['likely']:
                elements = (self.turnip_data[periods]['likely']).split(" - ", 1)
                likelyLower.append(int(elements[0]))
                likelyUpper.append(int(elements[1]))
            else:
                likelyLower.append(int(self.turnip_data[periods]['likely']))
                likelyUpper.append(int(self.turnip_data[periods]['likely']))
            xAxisLabels.append(periods.replace("_", " ", 1))  # Add each period to a list to be used as Label for xAxis
        # Matplotlib graph functions
        pricePatch = mpatches.Patch(color="#CF70D3", label='Price Range')
        likelyPatch = mpatches.Patch(color="#32CD32", label='Likely Price Range')
        plt.subplots(facecolor='lightslategray')
        plt.xticks(range(len(xAxisLabels)), xAxisLabels,  rotation='vertical', fontproperties=prop)
        plt.yticks(fontproperties=prop)
        plt.plot(xAxisLabels, priceLower, color="#CF70D3", label='Lower Price')
        plt.plot(xAxisLabels, priceUpper, color="#CF70D3", label='Upper Price')
        plt.fill_between(xAxisLabels, priceLower, priceUpper, color='#CF70D3')
        plt.plot(xAxisLabels, likelyLower, color="#32CD32", label='Lower Likely')
        plt.plot(xAxisLabels, likelyUpper, color="#32CD32", label='Upper Likely')
        plt.fill_between(xAxisLabels, likelyLower, likelyUpper, color="#32CD32")
        plt.ylabel("Amount: Bells", fontproperties=prop)
        plt.xlabel("Day", fontproperties=prop)
        plt.legend(handles=[pricePatch, likelyPatch], bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, mode="expand", borderaxespad=0., framealpha=0, prop=prop)
        # Save image to temp location
        plt.savefig("tempHolding/graph/{}".format(self.fileName), transparent=True, bbox_inches='tight')

        # Uses Pillow to form final image with boarder
        templateImage = Image.open('files/graphTemplate.png')
        # We load in the graph image and resize it to make it fit into the middle of the template
        graphImage = Image.open("tempHolding/graph/{}".format(self.fileName))
        widthPercent = (basewidth / float(graphImage.size[0]))
        heightSize = int((float(graphImage.size[1]) * float(widthPercent)))
        graphImage = graphImage.resize((basewidth, heightSize), Image.ANTIALIAS)
        newImage = templateImage.copy()
        # paste graph onto template with transparency
        newImage.paste(graphImage, (x, 55), graphImage)
        # Add in %ages
        draw = ImageDraw.Draw(newImage)
        y = 31
        draw.text((714, y), "Chance(%)", fill=headingColour, font=headingFont)
        y = y + 34
        for periods in self.turnip_data:  # For each of the periods in the dict
            period = periods.replace("_", " ", 1)  # remove the dash, so it looks nicer
            draw.text((714, y), period, fill=subHeadingColour, font=percentFont)
            y = y + 23
            # Add the actual %age in
            draw.text((714, y), "   {}".format(self.turnip_data[periods]['chance']), fill=colour, font=percentFont)
            y = y + 27
        newImage.save("tempHolding/Graph{}".format(self.fileName))  # Save image to temp location
        self.graphCreated = True
        os.remove("tempHolding/graph/{}".format(self.fileName))  # Remove the temp image from matplotlib

    def uploadImage(self) -> str:
        """
        Uploads image to S3 bucket
        :return: str
            Link to the uploaded image
        """
        if not self.created:
            raise errors.FileNotCreated("File Not created")
        try:
            # Upload files to S3
            client.upload_file("tempHolding/{}".format(self.fileName),
                           auth.aws_bucket,
                           "TurnipBot/predictions/{}".format(self.fileName),
                           ExtraArgs={'ACL': 'public-read'})
            os.remove("tempHolding/{}".format(self.fileName))  # remove temp file
            return "{}/TurnipBot/predictions/{}".format(auth.CDNLink, self.fileName)
        except be.ClientError as e:
            os.remove("tempHolding/Graph{}".format(self.fileName))
            raise errors.AWSError(e)
        except Exception as e:
            os.remove("tempHolding/Graph{}".format(self.fileName))
            raise errors.AWSError(e)

    def uploadGraphImage(self) -> str:
        """
        Uploads Graph image to S3 bucket
        :return: str
            Link to the uploaded image
        """
        if not self.graphCreated:
            raise errors.FileNotCreated("File Not created")
        try:
            # Upload files to S3
            client.upload_file("tempHolding/Graph{}".format(self.fileName),
                               auth.aws_bucket,
                               "TurnipBot/predictions/Graph{}".format(self.fileName),
                               ExtraArgs={'ACL': 'public-read'})
            os.remove("tempHolding/Graph{}".format(self.fileName))  # remove temp file
            return "{}/TurnipBot/predictions/Graph{}".format(auth.CDNLink, self.fileName)
        except be.ClientError as e:
            os.remove("tempHolding/Graph{}".format(self.fileName))
            raise errors.AWSError(e)
        except Exception as e:
            os.remove("tempHolding/Graph{}".format(self.fileName))
            raise errors.AWSError(e)
