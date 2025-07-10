import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
from disnake.ext import commands
import asyncio
from util.configuration import load_config_into_env, verify_config
from util.database import Database
from logger import logger
from kaggle.api.kaggle_api_extended import KaggleApi


class HotRoundBot(commands.InteractionBot):
    def __init__(self, **options):
        super().__init__(**options)
        self.database = Database(os.getenv('db_connection'))

    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')

async def main():
    bot_token = os.getenv("bot_token")
    bot = HotRoundBot()
    bot.load_extension('exts.ratings', package='exts')
    bot.load_extension('exts.status', package='exts')

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
    if len(sys.argv) == 2:
        config_file_path = sys.argv[1]
        load_config_into_env(config_file_path)
    verify_config([
        "bot_token",
        "db_path", 
        "db_file_name", 
        "db_connection", 
        "kaggle_dataset",
        "KAGGLE_USERNAME", 
        "KAGGLE_KEY",
    ])
    db_path = os.getenv("db_path")
    db_file_name = os.getenv("db_file_name")
    kaggle_dataset = os.getenv("kaggle_dataset")
    
    logger.info("Connecting to Kaggle...")
    api = KaggleApi()
    api.authenticate()
    # api.dataset_download_files(
    #     dataset=kaggle_dataset,
    #     path=db_path, 
    #     unzip=True)
    if not os.path.exists(db_path + db_file_name):
        raise ValueError("Failed to download Kaggle dataset.")
    logger.info("Downloaded Kaggle dataset.")
    
    asyncio.run(main())
