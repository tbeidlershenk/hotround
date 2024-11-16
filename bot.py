import logging
from disnake.ext import commands
import dotenv
import os
import asyncio
from server import run_server
from util.database import Database
import json
import threading
from tendo import singleton
import sys

try:
    instance = singleton.SingleInstance() 
except singleton.SingleInstanceException:
    exit()

class CaddieBot(commands.InteractionBot):
    def __init__(self, **options):
        super().__init__(**options)
        self.database = Database(os.getenv('db_connection'))
        self.logger = logging.getLogger('disnake')

    async def on_ready(self):
        self.logger.info(f'PID: {os.getpid()}')
        self.logger.info(f'Logged in as {self.user}')

async def main():
    bot_token = os.getenv("bot_token")
    log_path = os.getenv('log_file')
    log_dir = os.path.dirname(log_path)
    log_file = os.path.basename(log_path)
    home_dir = os.path.expanduser("~")
    log_dir = os.path.join(home_dir, log_dir)
    log_path = os.path.join(log_dir, log_file)
    os.makedirs(log_dir, exist_ok=True)

    bot_logger = logging.getLogger('disnake')
    bot_logger.setLevel(logging.INFO)
    log_file_handler = logging.FileHandler(log_path, mode='a')
    log_file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
    bot_logger.addHandler(log_file_handler)
    
    bot = CaddieBot() 
    bot.load_extensions("exts")

    try:
        await bot.start(bot_token)
    except InterruptedError:
        pass
    except BaseException:
        pass
    finally:
        bot.logger.info('Logging out of session...')
        await bot.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 bot.py <config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    with open(config_file_path) as config_file:
        config: dict = json.load(config_file)
    for key, value in config.items():
        if value is None:
            continue
        os.environ[key] = str(value)
    
    threading.Thread(target=run_server).start()
    asyncio.run(main())
