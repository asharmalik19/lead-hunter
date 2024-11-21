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

logger = create_logger()


def transform_info(info):
    if info['website_address_list']:
        info['website_address_list'] = find_valid_address(info['website_address_list'])
    else:
        info['website_address_list'] = None
    
    if 'facebook_address_list' in info and not info['facebook_address_list']:  # if the address list is empty, set it to None instead of square brackets
        info['facebook_address_list'] = None
    return info



def process_url(url, driver):
    """The function drops the urls which are not fetched and they are not stored in the output file.

    Output Schema:
    {
        'url': The URL of the website being scraped,
        'facebook_email': The email of the business from Facebook,
        'facebook_phone': The phone number of the business from Facebook,
        'facebook_address_list': The address of the business from Facebook,
        'facebook_business_type': The business type of the business from Facebook,
        'facebook_business_name': The name of the business from Facebook,
        'website_email': The email of the business from the website,
        'website_phone': The phone number of the business from the website,
        'website_address_list': The address of the business from the website,
        'website_business_name': The name of the business from the website
    }
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

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main(urls):
    driver = get_driver()
    all_data = []

    for url in urls:
        info = process_url(url, driver)
        if info:
            all_data.append(info)
            print(f"Extracted info from {url}: {info}")

    save_to_excel(all_data, 'extracted_info.xlsx')
    driver.quit()


if __name__ == '__main__':
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

    urls = pd.read_excel('momence_websites.xlsx')["Momence Merchant URL's"].tolist()[:21]
    main(urls)

    
