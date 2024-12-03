from scrape_website import fetch_url, get_fb_link, extract_info_from_website
from scrape_fb import extract_info_from_fb
from config_logger import create_logger
from selenium import webdriver
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
    
    if 'facebook_address_list' in info:  # check if at least any info has been got from fb i.e when the link is valid
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
    driver = webdriver.Chrome(options=options)
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
        if info:        # todo: if info contains no values for keys, then navigate to the content page to get info
            all_data.append(info)
            print(f"Extracted info from {url}: {info}")
        else:
            all_data.append({'url': url})
            logger.error(f"Failed to fetch the {url}")

    save_data(all_data)
    driver.quit()


if __name__ == '__main__':
    start_time = time.time()
    
    urls = pd.read_csv('cleaned_momence_websites.csv')['domain'].iloc[:20].tolist()
    main(urls)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


# todo: 
# 1. the bot currently checks for the required info on the given page of the website (and fb). Navigation to relevant pages 
# should also be done.
# 2. the bot should parse the domains from the urls and extract the info from them. If the info can't be found on the main page
# (domain), then the bot should try to find the contact page and find info there.
# 3. Addresses and phone numbers for other supported countries need to be added.
# 4. Try the html_text library from zyte to check if we get any better text from web pages.

