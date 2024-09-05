from icecream import ic

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import pandas as pd

from core.parsing_validator_info import ValidatorInfoScraper


class ValidatorExternalLinksScraper(ValidatorInfoScraper):
    def __init__(self, csv_file_path):
        super().__init__(urls=[])
        self.csv_file_path = csv_file_path
        self.data = []

    def save_to_csv(self):
        df = pd.read_csv(self.csv_file_path)
        df['external_link'] = self.data
        df.to_csv(self.csv_file_path, index=False)
        ic("Data saved to file: " + self.csv_file_path)

    def scrape_external_links(self):
        ic("Starting to scrape external links...")
        df = pd.read_csv(self.csv_file_path)
        ic(f"Found {len(df)} validators in the CSV file")

        for index, row in df.iterrows():
            validator_name = row['validator_name']
            validator_link = row['link']
            ic(f"Processing validator: {validator_name}")
            ic(f"Validator link: {validator_link}")

            try:
                self.driver.get(validator_link)
                ic(f"Loaded page for validator: {validator_name}")

                WebDriverWait(self.driver, 30).until(
                    ec.presence_of_element_located((By.TAG_NAME, "a"))
                )

                try:
                    link_element = self.driver.find_element(By.CLASS_NAME, "el-BlockchainAgentExternalLink")
                    external_link = link_element.get_attribute("href")
                    ic(f"External link found: {external_link}")

                except:
                    ic(f"el-BlockchainAgentExternalLink not found, searching all <a> elements...")
                    external_link = ''
                    ic(f"No external link found for validator: {validator_name}")

                self.data.append(external_link)

            except TimeoutException:
                ic(f"Timeout waiting for page to load for validator: {validator_name}")
            except Exception as e:
                ic(f"Error processing validator {validator_name}: {str(e)}")

        self.save_to_csv()
