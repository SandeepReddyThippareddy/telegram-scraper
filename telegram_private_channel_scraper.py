from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from datetime import datetime, timezone
import os
import sys

# Telegram API credentials
api_id = '21637603'  
api_hash = '083076909d9d86fcacae0959d7e06e13'  

# Channel name and date range
channel_username = "@GetBankLog" 
from_date = datetime(2024, 10, 1, tzinfo=timezone.utc)  
to_date = datetime(2024, 10, 31, tzinfo=timezone.utc)  

download_folder = channel_username[1:] 
os.makedirs(download_folder, exist_ok=True)  

async def download_images_by_date(channel_username, from_date, to_date):
    """
    Downloads images from a specified Telegram channel within a date range.
    Images are saved in a folder named after the channel.
    """
    try:
        async with TelegramClient('unique_session_name', api_id, api_hash, timeout=60) as client:
            print(f"Connected to Telegram. Downloading images from {channel_username} within date range {from_date} to {to_date}...")
            
            async for message in client.iter_messages(channel_username, offset_date=from_date, reverse=True):
                if message.date < from_date:
                    break
                if message.date > to_date:
                    continue
                
                if message.media and (isinstance(message.media, MessageMediaPhoto) or isinstance(message.media, MessageMediaDocument)):
                    try:
                        sender = await message.get_sender()
                        sender_username = sender.username if sender.username else f"user_{sender.id}"
                        
                        local_message_date = message.date.astimezone()  # Defaults to local timezone

                        message_date_str = local_message_date.strftime('%Y-%m-%d_%H-%M-%S')
                        
                        filename = f"{sender_username}_{message_date_str}.jpg"
                        
                        file_path = await client.download_media(message, file=os.path.join(download_folder, filename))
                        print(f"Downloaded image: {file_path}")
                    except Exception as e:
                        print(f"Failed to download image from message ID {message.id}: {e}")
    except ValueError as ve:
        print(f"ValueError: {ve} - Please ensure the channel exists and is accessible.")
    except ConnectionError:
        print("Failed to connect to Telegram. Check your internet connection and API credentials.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Image download process completed.")

if __name__ == "__main__":
    try:
        with TelegramClient('session_name', api_id, api_hash) as client:
            client.loop.run_until_complete(download_images_by_date(channel_username, from_date, to_date))
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"An error occurred during client session initialization: {e}")
        sys.exit(1)
    finally:
        print("Script execution finished. All processes closed.")