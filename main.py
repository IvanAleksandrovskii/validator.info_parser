from icecream import ic

from core.parsing_validator_info import (
    ValidatorExternalLinksScraper,
    ValidatorLinkAndImageScraper,
    ValidatorDataScraper,
    MainPageScraper,
)


def main():
    main_page_scraper = MainPageScraper(["https://validator.info"])
    validators_page_scraper = ValidatorDataScraper([
        "https://validator.info/lava",
        # "https://validator.info/dydx",
        # "https://validator.info/cronos-pos",
        # "https://validator.info/celestia",
        # "https://validator.info/terra-classic",
        # "https://validator.info/dymension",
        # "https://validator.info/saga",
        # "https://validator.info/haqq",
        # "https://validator.info/coreum",
        # "https://validator.info/nolus",
        # "https://validator.info/polygon",
    ])

    link_and_image_scraper = ValidatorLinkAndImageScraper(validators_page_scraper.urls)
    external_link_scraper = ValidatorExternalLinksScraper("lava/lava_validators.csv")

    # main_page_scraper.scrape_main_page()
    try:
        main_page_content = main_page_scraper.scrape_main_page()
        data = main_page_scraper.extract_data_from_main_page(main_page_content)
        main_page_scraper.create_csv_from_main_page(data)
    except Exception as e:
        ic(f"Error scraping main page: {str(e)}")

    # validators_page_scraper.scrape_validator_data()
    for url in validators_page_scraper.urls:
        try:
            df = validators_page_scraper.scrape_validator_data(url)
            validators_page_scraper.save_to_csv(df, url)
        except Exception as e:
            ic(f"Error scraping {url}: {str(e)}")

    # link_and_image_scraper.scrape_validator_links_and_images()
    try:
        ic("Starting the scraping process...")
        link_and_image_scraper.scrape_validator_links_and_images()
        ic("Scraping process completed successfully.")
    except Exception as e:
        ic(f"Critical error during scraping: {str(e)}")
    finally:
        if hasattr(link_and_image_scraper, 'driver'):
            link_and_image_scraper.driver.quit()

    # external_link_scraper.scrape_external_links()
    try:
        ic("Starting the external links scraping process...")
        external_link_scraper.scrape_external_links()
        ic("External links scraping process completed successfully.")
    except Exception as e:
        ic(f"Critical error during scraping: {str(e)}")
    finally:
        if hasattr(external_link_scraper, 'driver'):
            external_link_scraper.driver.quit()


if __name__ == "__main__":
    ic("Script started")
    main()
    ic("Script ended")
