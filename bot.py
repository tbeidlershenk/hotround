from disnake.ext import commands
import dotenv
import os
import asyncio
from logger import logger
from util.database import Database
import json

class CaddieBot(commands.Bot):
    def __init__(self, config: dict, **options):
        super().__init__(**options)
        self.database = Database(config['db_connection'])
        self.debug: bool = config['debug']

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

async def main():
    dotenv.load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    with open('config.json') as config_file:
        config: dict = json.load(config_file)
    bot = CaddieBot(config)  # Ensure to pass a command prefix or other required options
    bot.load_extensions("exts")

    # This starts the bot in much the same way as `bot.run` does, except in
    # an async context.
    await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())