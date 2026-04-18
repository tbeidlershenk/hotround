from logger import logger
from util.database import Database
from kaggle.api.kaggle_api_extended import KaggleApi
import os


def pull_from_kaggle():
    db_path = os.getenv("db_path")
    db_file_name = os.getenv("db_file_name")
    kaggle_dataset = os.getenv("kaggle_dataset")

    logger.info("Connecting to Kaggle...")
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset=kaggle_dataset, path=db_path, unzip=True)
    if not os.path.exists(db_path + db_file_name):
        raise ValueError("Failed to download Kaggle dataset.")
    logger.info(f"Downloaded Kaggle dataset to {db_path + db_file_name}")


def push_to_kaggle():
    db_path = os.getenv("db_path")
    db_file_name = os.getenv("db_file_name")
    kaggle_dataset = os.getenv("kaggle_dataset")

    logger.info("Connecting to Kaggle...")
    api = KaggleApi()
    api.authenticate()
    api.dataset_create_version(
        folder=db_path,
        version_notes="",
        convert_to_csv=False,
    )
    logger.info(f"Uploaded Kaggle dataset from {db_path + db_file_name}")
