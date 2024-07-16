import logging
import os
import sys
import discord

class Logger:
    def __init__(self):
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.log.addHandler(self.handler)
logger = Logger()

intents = discord.Intents.default()  # creates a new Intents object with all flags enabled
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.log.info('We have logged in as {0.user}'.format(client))
    channel_id = os.environ["DISCORD_CHANNEL_ID"]
    channel = client.get_channel(int(channel_id))
    await channel.send(os.environ["DISCORD_MESSAGE"])
    await client.close()

client.run(os.environ["DISCORD_TOKEN"])
