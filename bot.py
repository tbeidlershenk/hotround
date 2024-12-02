import logging
from disnake.ext import commands
import os
import asyncio
from util.configuration import load_config_into_env
from util.database import Database
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
    bot_logger = logging.getLogger('disnake')
    bot_logger.setLevel(logging.INFO)
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
    load_config_into_env(config_file_path)
    asyncio.run(main())
