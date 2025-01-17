import os
import asyncio
import json
import sys
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
