import logging
from disnake.ext import commands
import dotenv
import os
import asyncio
from util.database import Database
import json

class CaddieBot(commands.InteractionBot):
    def __init__(self, config: dict, **options):
        super().__init__(**options)
        self.database = Database(config['db_connection'])
        self.debug: bool = config['debug']

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')

async def main():
    dotenv.load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    with open('bot_config.json') as config_file:
        config: dict = json.load(config_file)

    log_path = config['log_file']
    log_dir = os.path.dirname(log_path)
    log_file = os.path.basename(log_path)
    os.mkdir(log_dir, exist_ok=True)
    bot_logger = logging.getLogger('disnake')
    bot_logger.setLevel(logging.WARNING)
    log_file_handler = logging.FileHandler(log_file)
    bot_logger.addHandler(log_file_handler)
    
    bot = CaddieBot(config) 
    bot.load_extensions("exts")

    # This starts the bot in much the same way as `bot.run` does, except in
    # an async context.
    await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())