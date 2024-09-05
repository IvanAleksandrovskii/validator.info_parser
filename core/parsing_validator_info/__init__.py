__all__ = ["ValidatorExternalLinksScraper", "ValidatorInfoScraper", "ValidatorLinkAndImageScraper",
           "ValidatorDataScraper", "MainPageScraper"]

from base_scraper import ValidatorInfoScraper
from main_page_scraper import MainPageScraper
from validators_link_and_image_scraper import ValidatorLinkAndImageScraper
from validators_link_scraper import ValidatorExternalLinksScraper
from validators_page_scraper import ValidatorDataScraper
