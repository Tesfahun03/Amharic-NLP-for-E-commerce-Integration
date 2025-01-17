
"""
This script fetches messages from specified Telegram channels and saves them to a CSV file.
Modules:
    os: Provides a way of using operating system dependent functionality.
    asyncio: Provides support for asynchronous programming.
    json: Provides methods for parsing JSON.
    sys: Provides access to some variables used or maintained by the interpreter.
    logging: Provides a way to configure and use loggers.
    pandas: Provides data structures and data analysis tools.
    telethon: Provides a Telegram client implementation.
    dotenv: Loads environment variables from a .env file.
Functions:
    fetch_messages(client, channel_username):
        Fetches the latest messages from a specified Telegram channel.
    main():
        Main function that initializes the Telegram client, fetches messages from channels, and saves them to a CSV file.
    fetch_data():
        Wrapper function to run the main function asynchronously.
Environment Variables:
    api_id: The API ID for the Telegram client.
    api_hash: The API hash for the Telegram client.
Usage:
    Run this script to fetch messages from the specified Telegram channels and save them to a CSV file.

    Fetches the latest messages from a specified Telegram channel.
    Args:
        client (TelegramClient): The Telegram client instance.
        channel_username (str): The username of the Telegram channel.
    Returns:
        list: A list of messages from the specified channel.
    
    Main function that initializes the Telegram client, fetches messages from channels, and saves them to a CSV file.
    This function connects to the Telegram client using the provided API ID and hash, fetches messages from the specified
    channels, and saves the messages to a CSV file. If the output file already exists, it prompts the user for confirmation
    before overwriting the file.
    
    Wrapper function to run the main function asynchronously.
    This function is used to initiate the asynchronous execution of the main function.
    """
import os
import sys
import asyncio
import json
import logging
import pandas as pd

from telethon import TelegramClient
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath('..'))

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
channel_usernames = ['@ZemenExpress', '@AwasMart',
                     '@modernshoppingcenter', '@Shewabrand', '@sinayelj']


async def fetch_messages(client, channel_username):
    messages = []
    async for message in client.iter_messages(channel_username, limit=100):
        messages.append(message.text)
    return messages


async def main():

    logger.info('client connected successfully ')

    # Fetch message from the channels above
    async with TelegramClient('session_name', api_id, api_hash) as client:
        tasks = [fetch_messages(client, username)
                 for username in channel_usernames]
        results = await asyncio.gather(*tasks)

        # Flatten the list of messages and process as needed
        all_messages = [msg for sublist in results for msg in sublist]

        logger.info(f"messgaes: {all_messages}")

    # save message in csv format
    output_file = '../data/telegram_messages.csv'
    media_file = '../data/media/'

    # check if a file name already existed or not
    if os.path.exists(output_file):
        print(
            f"File {output_file} already exists. Do you want to override it? (Y/N): ")
        choice = input().lower()
        if choice != 'y':
            print('opration cancelled')

    df = pd.DataFrame(all_messages, columns=['messages'])
    df.to_csv(output_file, index=False)
    logger.info(f"messages saved to {output_file}")


async def fetch_data():
    await main()
