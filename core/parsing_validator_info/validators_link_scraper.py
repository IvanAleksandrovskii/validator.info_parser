import os
import glob

from icecream import ic

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

import pandas as pd

from core.parsing_validator_info import ValidatorInfoScraper
from core import logger, settings


class ValidatorExternalLinksScraper(ValidatorInfoScraper):
    def __init__(self):
        super().__init__(urls=[])
        self.config = settings.validator_info_scraper_save_path
        self.base_dir = self.config.link_and_image_dir

    def process_csv_file(self, file_path):
        ic(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        external_links = []

        for index, row in df.iterrows():
            validator_name = row['validator_name']
            validator_link = row['link']
            logger.debug(f"Processing validator: {validator_name}")
            logger.debug(f"Validator link: {validator_link}")

            try:
                self.driver.get(validator_link)
                ic(f"Loaded page for validator: {validator_name}")

                WebDriverWait(self.driver, 30).until(
                    ec.presence_of_element_located((By.TAG_NAME, "a"))
                )

                try:
                    link_element = self.driver.find_element(By.CLASS_NAME, "el-BlockchainAgentExternalLink")
                    external_link = link_element.get_attribute("href")
                    logger.debug(f"External link found: {external_link}")
                except:
                    external_link = ''
                    logger.debug(f"No external link found for validator: {validator_name}")

                external_links.append(external_link)

            except TimeoutException:
                logger.exception(f"Timeout waiting for page to load for validator: {validator_name}")
                external_links.append('')
            except Exception as e:
                logger.exception(f"Error processing validator {validator_name}: {str(e)}")
                external_links.append('')

        df['external_link'] = external_links
        df.to_csv(file_path, index=False)
        ic(f"Updated and saved file: {file_path}")

    def scrape_external_links(self):
        ic("Starting to scrape external links...")
        csv_files = glob.glob(os.path.join(self.base_dir, "*", "*_validators.csv"))

        for file_path in csv_files:
            self.process_csv_file(file_path)

        ic("Finished scraping external links for all files.")
