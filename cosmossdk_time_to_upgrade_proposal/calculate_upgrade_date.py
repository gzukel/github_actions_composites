import logging  # Import the logging module for logging purposes
import os  # Import the os module for interacting with the operating system
import sys  # Import the sys module for system-specific parameters and functions
import time  # Import the time module for sleep function and time calculations
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


def convert_nanoseconds_to_seconds(nanoseconds):
    """
    Function to convert nanoseconds to seconds.

    Parameters:
    nanoseconds (int): The time in nanoseconds.

    Returns:
    float: The time in seconds.
    """
    return nanoseconds / 1000000000


# Make a request to get the genesis data
web_request = requests_get_call(f"{os.environ['RPC_URL']}/genesis")

# Make a request to get the current block height
current_height = int(requests_get_call(f"{os.environ['RPC_URL']}/status")["result"]["sync_info"]["latest_block_height"])

# Get the upgrade height and average block time from environment variables
upgrade_height = int(os.environ["UPGRADE_HEIGHT"])
average_block_time = float(os.environ["AVERAGE_BLOCK_TIME"])

if web_request:
    logger.log.info("Web Request: Success")

    # Convert the voting period from nanoseconds to seconds
    voting_period = convert_nanoseconds_to_seconds(int(os.environ["VOTING_PERIOD"]))

    # Calculate the total number of blocks between the current height and the upgrade height
    total_number_of_blocks_for_upgrade = upgrade_height - current_height

    # Calculate the total seconds for the upgrade based on the average block time
    total_seconds_for_upgrade = float(total_number_of_blocks_for_upgrade) * average_block_time

    # Log various information for debugging purposes
    logger.log.info(f"VOTING PERIOD: {voting_period}")
    logger.log.info(f"UPGRADE_HEIGHT: {upgrade_height}")
    logger.log.info(f"CURRENT_HEIGHT: {current_height}")
    logger.log.info(f"AVERAGE BLOCK TIME: {average_block_time}")
    logger.log.info(f"BLOCKS BETWEEN CURRENT BLOCK AND UPGRADE BLOCK: {total_number_of_blocks_for_upgrade}")
    logger.log.info(f"TOTAL SECONDS FOR UPGRADE: {total_seconds_for_upgrade}")

    # Check if the total seconds for upgrade is beyond the voting period
    if total_seconds_for_upgrade > voting_period:
        logger.log.info("UPGRADE HEIGHT BEYOND VOTING PERIOD CHECK: PASS")
    else:
        logger.log.info("UPGRADE HEIGHT BEYOND VOTING PERIOD CHECK: FAILURE")
        sys.exit(2)  # Exit the script with a status code of 2 if the check fails

    # Calculate the end time for the upgrade in UTC
    current_time = time.time()
    end_time = current_time + total_seconds_for_upgrade
    end_time_object = datetime.datetime.fromtimestamp(end_time)
    utc_dt = end_time_object.astimezone(pytz.UTC)

    # Log the calculated upgrade time in UTC
    logger.log.info(f"UPGRADE WILL HAPPEN UTC: {str(utc_dt)}")
else:
    logger.log.critical("FAILED:TO:GET:GENESIS")
    sys.exit(2)  # Exit the script with a status code of 2 if the genesis request fails

# Write the calculated upgrade date to the GitHub environment file
GITHUB_ENV = open(os.environ["GITHUB_ENV"], "a+")
GITHUB_ENV.write(f"UPGRADE_DATE={utc_dt}")
GITHUB_ENV.close()
