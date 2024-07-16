import logging  # Import the logging module for logging purposes
import os  # Import the os module for interacting with the operating system
import sys  # Import the sys module for system-specific parameters and functions
import datetime  # Import the datetime module for working with dates and times
import requests  # Import the requests module for making HTTP requests
import pytz  # Import the pytz module for working with time zones


class Logger:
    """
    Logger class for setting up logging configuration.
    """

    def __init__(self):
        # Initialize the logger
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.handler = logging.StreamHandler(sys.stdout)  # Set up the stream handler to output to stdout
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Define the log format
        self.handler.setFormatter(self.formatter)
        self.log.addHandler(self.handler)  # Add the handler to the logger


# Instantiate the Logger class
logger = Logger()


def requests_get_call(url):
    """
    Function to make a GET request and return the JSON response.
    Logs an error if the request fails.

    Parameters:
    url (str): The URL to make the GET request to.

    Returns:
    dict: The JSON response from the GET request, or None if the request fails.
    """
    try:
        web_request = requests.get(url).json()  # Make a GET request and parse the JSON response
    except Exception as e:
        logger.log.error(str(e))  # Log any exceptions that occur
        web_request = None
    return web_request


# Parse the upgrade date from the environment variable
upgrade_date_object = datetime.datetime.strptime(os.environ["UPGRADE_DATE"], "%m/%d/%Y %H:%M")

# Get the current date and time
now = datetime.datetime.now()

# Convert the current date and time to UTC
utc_now = now.astimezone(pytz.UTC)

# Convert the upgrade date to UTC
utc_future = upgrade_date_object.astimezone(pytz.UTC)

# Calculate the difference between the future upgrade date and now
difference = utc_future - utc_now

# Calculate the difference in seconds
seconds_difference = difference.total_seconds()

# Calculate the number of blocks that can fit within the available seconds
blocks_within_available_seconds = float(seconds_difference) / float(os.environ["AVERAGE_BLOCK_TIME"])

# Make a request to get the current block height
current_height = int(requests_get_call(f"{os.environ['RPC_URL']}/status")["result"]["sync_info"]["latest_block_height"])

# Calculate the upgrade height by adding the blocks within the available seconds to the current height
upgrade_height = current_height + int(blocks_within_available_seconds)

# Log the calculated upgrade height
logger.log.info(f"UPGRADE_HEIGHT_CALCULATED: {upgrade_height}")

# Write the calculated upgrade height to the GitHub environment file
GITHUB_ENV = open(os.environ["GITHUB_ENV"], "a+")
GITHUB_ENV.write(f"UPGRADE_HEIGHT={upgrade_height}")
GITHUB_ENV.close()
