import re
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from core import settings


class ValidatorInfoScraper:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.driver = self._get_chrome_driver()

    def _get_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(settings.chrome.path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    @staticmethod
    def _clean_validator_name(name):
        name = re.sub(r'^[+-]?\d+\s*', '', name)
        name = re.sub(r'\bNEW\s*', '', name)
        name = re.sub(r'^\d+\s*', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    @staticmethod
    def _clean_numeric_value(value, column_name):
        value = value.split('\n')[0] if '\n' in value else value

        if column_name == "Votes":
            value = re.sub(r'[^0-9/\s]', '', value)
        else:
            value = re.sub(r'[^0-9.,%]', '', value)

        return value.strip()
