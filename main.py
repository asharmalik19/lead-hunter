from scrape_website import fetch_url, get_fb_link, extract_info_from_website
from scrape_fb import extract_info_from_fb
from config_logger import create_logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
import logging
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ai import find_valid_address
import time

logger = create_logger()


def transform_info(info):
    """Transforms the data before it is stored."""
    if info['website_address_list']:
        info['website_address_list'] = find_valid_address(info['website_address_list'])
    else:
        info['website_address_list'] = None
    
    if 'facebook_address_list' in info:
        if not info['facebook_address_list']: 
            info['facebook_address_list'] = None
        else:
            info['facebook_address_list'] = info['facebook_address_list'][0]
    return info


def process_url(url, driver):
    """
    Process a single URL, scrape data from the website and its associated Facebook page.

    Args:
    url (str): The URL of the website to process.
    driver (webdriver.Chrome): Selenium WebDriver instance for web scraping.

    Returns:
    dict: A dictionary containing scraped information with the following structure:
        {
            'url': str,                     # The URL of the website being scraped
            'facebook_email': str,          # Email from Facebook page
            'facebook_phone': str,          # Phone number from Facebook page
            'facebook_address_list': str,   # Address from Facebook page (single string)
            'facebook_business_type': str,  # Business type from Facebook page
            'facebook_business_name': str,  # Business name from Facebook page
            'website_email': str,           # Email from website
            'website_phone': str,           # Phone number from website
            'website_address_list': str,    # A single valid address from website
            'website_business_name': str    # Business name from website
        }

    Note:
    - If the URL fails to fetch or process, an empty dictionary is returned.
    """

    logger.info(f"Processing {url}")

    content = fetch_url(url)
    if not content:
        logger.error(f"Failed to get content for {url}")
        return {}
    
    info = {'url': url}  # this contains the combined info from the website and fb
    
    fb_link = get_fb_link(content)
    if fb_link:
        info_from_fb = extract_info_from_fb(fb_link, driver)
        info.update(info_from_fb)
        logger.info(f"{url}: Extracted info from fb: {info_from_fb}")

    info_from_website = extract_info_from_website(content)
    logger.info(f"{url}: Extracted info_from_website from website: {info_from_website}")
    info.update(info_from_website)

    info = transform_info(info)
    return info


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(20)  # change the page load strategy or timout
    return driver


def save_data(data):
    file_name = 'extracted_info.csv'
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")


def main(urls):
    """Handles the flow of execution and starts/quits of the driver."""
    driver = get_driver()
    all_data = []

    for url in urls:
        info = process_url(url, driver)
        if info:
            all_data.append(info)
            print(f"Extracted info from {url}: {info}")
        else:
            logger.error(f"Failed to get info for {url}")

    save_data(all_data)
    driver.quit()


if __name__ == '__main__':
    start_time = time.time()
    
    urls = pd.read_excel('momence_websites.xlsx')["Momence Merchant URL's"].tolist()[:12]
    # urls = ['https://bikramyogaleicester.com/schedule-2-2/']
    main(urls)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    
  # urls = [
    #     'https://dottirhotyoga.squarespace.com/workshops',
    #     'https://downtoearthlondon.co.uk/workshops/',
    #     'https://downwarddog.com/class-schedule/',
    #     'https://drivefitnessstudio.com/bootcamp/',
    #     'https://pbn.haus/',
    #     'https://drogadomilosci.com/proces/',
    #     'https://dte-yoga.com/2023/01/07/explore-our-diverse-yoga-classes-at-dte-yoga-in-port-saint-lucie/',
    #     'https://earthworm-quillfish-g2gx.squarespace.com/events/yin-sound-july',
    #     'https://earthworm-saxophone-epza.squarespace.com/special-promotion',
    #     'https://earthyogastudio.com/schedule'
    # ]