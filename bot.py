import sys
import os
from disnake.ext import commands
import asyncio
from util.configuration import load_config_into_env
from util.database import Database
from logger import logger

class CaddieBot(commands.InteractionBot):
    def __init__(self, **options):
        super().__init__(**options)
        self.database = Database(os.getenv('db_connection'))

    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')

async def main():
    bot_token = os.getenv("bot_token")
    bot = CaddieBot() 
    bot.load_extensions("exts")

    try:
        await bot.start(bot_token)
    except InterruptedError:
        pass
    except BaseException:
        pass
    finally:
        logger.info('Logging out of session...')
        await bot.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 bot.py <config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)
    asyncio.run(main())
