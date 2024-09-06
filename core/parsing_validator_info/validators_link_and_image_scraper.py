from icecream import ic
import httpx
import os
import re

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd

from core.parsing_validator_info import ValidatorInfoScraper
from core import logger, settings


class ValidatorLinkAndImageScraper(ValidatorInfoScraper):
    def __init__(self, urls):
        super().__init__(urls)
        self.data = {}

    def scrape_validator_links_and_images(self):
        ic("Starting to scrape validator links and images...")

        for url in self.urls:
            logger.debug(f"Processing URL: {url}")
            chain_name = url.split('/')[-1]
            logger.debug(f"Chain name: {chain_name}")

            self.data[chain_name] = []

            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 30).until(
                    ec.presence_of_element_located((By.CLASS_NAME, "el-DataListRow"))
                )

                rows = self.driver.find_elements(By.CLASS_NAME, "el-DataListRow")
                ic(f"Found {len(rows)} validators for {chain_name}")

                for i, row in enumerate(rows):
                    logger.debug(f"Processing validator {i + 1} of {len(rows)}")

                    try:
                        validator_link = row.find_element(By.TAG_NAME, "a").get_attribute("href")
                        logger.debug(f"Validator page link: {validator_link}")

                        validator_name = row.find_element(By.CLASS_NAME, "el-NameText").text.strip()
                        logger.debug(f"Validator name: {validator_name}")

                        img_src = row.find_element(By.TAG_NAME, "img").get_attribute("src")
                        logger.debug(f"Image source: {img_src}")

                        self.data[chain_name].append({
                            "validator_name": validator_name,
                            "img_src": img_src,
                            "link": validator_link
                        })
                        ic(f"Added data for {validator_name}")

                    except Exception as e:
                        ic(f"Error processing validator {i + 1}: {str(e)}")

            except Exception as e:
                ic(f"Error processing chain {chain_name}: {str(e)}")

        ic("Finished scraping all validators")
        self.save_images_and_create_csv()

    def save_images_and_create_csv(self):
        ic("Starting to save images and create CSV files...")
        config = settings.validator_info_scraper_save_path

        for chain_name, validators in self.data.items():
            chain_dir = os.path.join(config.media_dir, chain_name)
            config.ensure_dir(chain_dir)

            for item in validators:
                img_filename = self.get_valid_filename(item['validator_name']) + ".png"
                img_path = config.get_image_path(chain_name, img_filename)

                logger.debug(f"Downloading image for {item['validator_name']}")
                response = httpx.get(item['img_src'])
                with open(img_path, 'wb') as f:
                    f.write(response.content)

                item['img_filename'] = img_filename
                logger.debug(f"Saved image: {img_filename}")

            df = pd.DataFrame(validators)
            csv_path = config.get_file_path(config.link_and_image_dir, f"{chain_name}_validators.csv")
            config.ensure_dir(os.path.dirname(csv_path))
            df.to_csv(csv_path, index=False)
            ic(f"Created CSV file: {csv_path}")

    @staticmethod
    def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)
