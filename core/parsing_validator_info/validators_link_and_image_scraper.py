import os
import re
import httpx
import pandas as pd
from icecream import ic

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from core.parsing_validator_info import ValidatorInfoScraper


class ValidatorLinkAndImageScraper(ValidatorInfoScraper):
    def __init__(self, urls):
        super().__init__(urls)
        self.data = {}

    def scrape_validator_links_and_images(self):
        ic("Starting to scrape validator links and images...")

        for url in self.urls:
            ic(f"Processing URL: {url}")
            chain_name = url.split('/')[-1]
            ic(f"Chain name: {chain_name}")

            self.data[chain_name] = []

            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 30).until(
                    ec.presence_of_element_located((By.CLASS_NAME, "el-DataListRow"))
                )

                rows = self.driver.find_elements(By.CLASS_NAME, "el-DataListRow")
                ic(f"Found {len(rows)} validators for {chain_name}")

                for i, row in enumerate(rows):
                    ic(f"Processing validator {i + 1} of {len(rows)}")

                    try:
                        validator_link = row.find_element(By.TAG_NAME, "a").get_attribute("href")
                        ic(f"Validator page link: {validator_link}")

                        validator_name = row.find_element(By.CLASS_NAME, "el-NameText").text.strip()
                        ic(f"Validator name: {validator_name}")

                        img_src = row.find_element(By.TAG_NAME, "img").get_attribute("src")
                        ic(f"Image source: {img_src}")

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

        for chain_name, validators in self.data.items():
            ic(f"Processing chain: {chain_name}")
            os.makedirs(chain_name, exist_ok=True)

            for item in validators:
                img_filename = self.get_valid_filename(item['validator_name']) + ".png"
                img_path = os.path.join(chain_name, img_filename)

                ic(f"Downloading image for {item['validator_name']}")
                response = httpx.get(item['img_src'])
                with open(img_path, 'wb') as f:
                    f.write(response.content)

                item['img_filename'] = img_filename
                ic(f"Saved image: {img_filename}")

            df = pd.DataFrame(validators)
            csv_path = os.path.join(chain_name, f"{chain_name}_validators.csv")
            df.to_csv(csv_path, index=False)
            ic(f"Created CSV file: {csv_path}")

    @staticmethod
    def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)
