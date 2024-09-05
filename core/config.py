import os
from pydantic_settings import BaseSettings


class ChromeConfig:
    path: str = os.path.abspath("/usr/local/bin/chromedriver")


# class WebConfig:
#     height_text_area = 500


class Settings(BaseSettings):
    chrome: ChromeConfig = ChromeConfig()


settings = Settings()
