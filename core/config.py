import os
from pydantic_settings import BaseSettings

# Base directories
BASE_DIR = "collected_data"
MEDIA_DIR = os.path.join(BASE_DIR, "media")

# Subdirectories for different scraper types
MAIN_PAGE_DIR = os.path.join(BASE_DIR, "main_page")
VALIDATOR_DATA_DIR = os.path.join(BASE_DIR, "validator_data")
LINK_AND_IMAGE_DIR = os.path.join(BASE_DIR, "link_and_image")


class ChromeConfig:
    path: str = os.path.abspath("/usr/local/bin/chromedriver")


class ValidatorInfoScraperSavePathConfig:
    base_dir: str = BASE_DIR
    media_dir: str = MEDIA_DIR

    main_page_dir: str = MAIN_PAGE_DIR
    validator_data_dir: str = VALIDATOR_DATA_DIR
    link_and_image_dir: str = LINK_AND_IMAGE_DIR

    @staticmethod
    def ensure_dir(directory):
        """Ensure that a directory exists, creating it if necessary."""
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def get_chain_name(url):
        """Extract the chain name from a URL."""
        return url.split('/')[-1]

    @staticmethod
    def get_file_path(base_dir, chain_name, filename):
        """Get the full file path for a given chain and filename."""
        return os.path.join(base_dir, chain_name, filename)

    @staticmethod
    def get_image_path(chain_name, filename):
        """Get the full image path for a given chain and filename."""
        return os.path.join(MEDIA_DIR, chain_name, filename)


class Settings(BaseSettings):
    chrome: ChromeConfig = ChromeConfig()
    validator_info_scraper_save_path: ValidatorInfoScraperSavePathConfig = ValidatorInfoScraperSavePathConfig()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure all necessary directories exist
        for directory in [BASE_DIR, MEDIA_DIR, MAIN_PAGE_DIR, VALIDATOR_DATA_DIR, LINK_AND_IMAGE_DIR]:
            self.validator_info_scraper_save_path.ensure_dir(directory)


settings = Settings()
