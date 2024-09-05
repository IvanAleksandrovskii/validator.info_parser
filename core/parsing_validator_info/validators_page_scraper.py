from icecream import ic
import time

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd

from core.parsing_validator_info import ValidatorInfoScraper
from core import logger


class ValidatorDataScraper(ValidatorInfoScraper):
    def scrape_validator_data(self, url):
        self.driver.get(url)
        time.sleep(10)

        WebDriverWait(self.driver, 20).until(
            ec.presence_of_element_located((By.CLASS_NAME, "el-DataListRow"))
        )

        rows = self.driver.find_elements(By.CLASS_NAME, "el-DataListRow")

        data = []

        for row in rows:
            cols = row.find_elements(By.CLASS_NAME, "el-DataListRowCell")
            row_data = [col.text.strip() for col in cols]
            data.append(row_data)

        count_of_columns = len(data[0])

        excluded_urls = ["https://validator.info/polygon"]

        if count_of_columns == 9 and url not in excluded_urls:
            headers = ["Validator", "Total staked", "Voting power", "Delegators", "Votes", "Fee", "APR", "Blocks", ""]

        elif count_of_columns == 10 and url not in excluded_urls:
            headers = ["Validator", "Total staked", "Voting power", "Delegators", "Votes", "Fee", "APR", "Blocks",
                       "Oracle", ""]

        elif url == "https://validator.info/polygon":
            headers = ["Validator", "Total staked", "Delegators", "Fee", "APR", "Checkpoints", "Heimdall", "Bar", ""]

        else:
            headers = []

        df = pd.DataFrame(data, columns=headers)

        for col in df.columns:
            if col == "Validator" or col == "Operator":
                df[col] = df[col].apply(self._clean_validator_name)
            else:
                df[col] = df[col].apply(lambda x: self._clean_numeric_value(x, col))

        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        df = df[df.iloc[:, 0].astype(bool)]
        df = df.loc[:, (df != '').any(axis=0)]

        ic(f"Scraped data from: {url}")
        ic(f"DataFrame shape: {df.shape}")
        ic(f"Columns: {df.columns.tolist()}")

        return df

    def save_to_csv(self, df, url):
        filename = url.split('/')[-1] + '.csv'
        filename = 'validator_info_tables/' + ''.join(c for c in filename if c.isalnum() or c in ('_', '.'))

        logger.debug("Columns in DataFrame:")
        for i, col in enumerate(df.columns):
            logger.debug(f"{i}: {col}")

        df.to_csv(filename, index=False)
        ic(f"Data saved to file: {filename}")
