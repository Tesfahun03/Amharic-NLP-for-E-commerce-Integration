import os
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
channel_username = '@ZemenExpress'

client = TelegramClient('session_name', api_id, api_hash)


async def main():
    await client.start()
    logger.info('client connected successfully ')

    # Fetch message from the channels above
    messages = []
    logger.info(f'fetching data from {channel_username}...')
    async for msg in client.iter_messages(channel_username, limit=100):
        if msg:
            messages.append({
                'text': msg.text,
                'sender': msg.sender_id,
                # 'date': msg.date,
                'media': msg.photo
            })
            # logger.info(
            #     f"Message Fetched ftom {msg.sender_id} message ")

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

    # def download_photo(message, file_path):
    #     if message.photo:
    #         message.download_media(file=file_path)
    #         print(f"Photo downloaded to {file_path}")

    # await download_photo(msg, media_file)
    # saving fetched data into pandas dataframe
    df = pd.DataFrame(messages)
    df.to_csv(output_file, index=False)
    logger.info(f"messages saved to {output_file}")

    logger.info(
        f"Message Fetched ftom {msg.sender_id} message {messages[0]['media']}")


async def fetch_data():
    async with client:
        await main()
