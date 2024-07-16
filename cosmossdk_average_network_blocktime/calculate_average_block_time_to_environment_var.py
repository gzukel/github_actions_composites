import logging  # Import the logging module for logging purposes
import os  # Import the os module for interacting with the operating system
import statistics  # Import the statistics module for calculating the mean
import sys  # Import the sys module for system-specific parameters and functions
import time  # Import the time module for sleep function

import requests  # Import the requests module for making HTTP requests
from dateutil.parser import parse  # Import the parse function from dateutil.parser for parsing dates


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


# Log the start of the average block time calculation process
logger.log.info("START CALCULATING AVERAGE BLOCK TIME")

# List to store the date objects for each block
date_objects = []

# Make a request to get the latest block status
web_request = requests_get_call(f"{os.environ['RPC_URL']}/status")
if web_request:
    logger.log.info("Web Request: Success")
    # Get the latest block height from the response
    LATEST_BLOCK_HEIGHT = int(web_request["result"]["sync_info"]["latest_block_height"])
    # Calculate the starting block height for sampling
    STARTING_SAMPLE_BLOCK_HEIGHT = LATEST_BLOCK_HEIGHT - int(os.environ["AVG_TIME_SAMPLE_SIZE"])

    # Loop through the range of block heights to get block data
    for block_height in range(STARTING_SAMPLE_BLOCK_HEIGHT, LATEST_BLOCK_HEIGHT):
        logger.log.info(f"LOOKING UP HEIGHT: {block_height}")
        # Make a request to get the block data for the current block height
        web_request = requests_get_call(f"{os.environ['RPC_URL']}/block?height={block_height}")
        if web_request:
            logger.log.info("BLOCK WEB REQUEST: SUCCESS")
            # Parse the block time and add it to the date_objects list
            date_object = parse(web_request["result"]["block"]["header"]["time"])
            date_objects.append(date_object)
        else:
            logger.log.critical("WEB REQUEST: FAILED")
            sys.exit(2)  # Exit the script with a status code of 2 if the request fails
        time.sleep(.3)  # Sleep for 0.3 seconds between requests to avoid overwhelming the server
else:
    logger.log.critical("Web Request: Failed")
    sys.exit(2)  # Exit the script with a status code of 2 if the initial status request fails

# Initialize variables for calculating time differences between blocks
first = True
last_date_object = None
time_differences_between_block = []

# Calculate the time differences between consecutive blocks
for date_object in date_objects:
    if first:
        last_date_object = date_object
        first = False
        continue
    else:
        # Calculate the time difference between the current and last block
        time_difference = date_object - last_date_object
        last_date_object = date_object
        time_difference_between_block = time_difference.total_seconds()
        logger.log.info(f"Difference in seconds: {time_difference_between_block}")
        time_differences_between_block.append(time_difference_between_block)

# Calculate the average block time
average_block_time = statistics.mean(time_differences_between_block)
logger.log.info(f"AVERAGE_BLOCK_TIME: {average_block_time}")

# Write the average block time to the GitHub environment file
GITHUB_ENV = open(os.environ["GITHUB_ENV"], "a+")
GITHUB_ENV.write(f"AVERAGE_BLOCK_TIME={average_block_time}")
GITHUB_ENV.close()
