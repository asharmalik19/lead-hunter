from scrape_website import fetch_url, get_fb_link, extract_info_from_website
from scrape_fb import extract_info_from_fb
from config_logger import create_logger
# from utils import extract_info_from_website
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


def check_info_completion(info, logger):
    """
    Required fields:
        Website, Company, Address, Phone, Email, Business Type, BO Name, Current Vendor
    """

    return


def process_url(url, logger, driver):
    logger.info(f"Processing {url}")

    content = fetch_url(url)
    if not content:
        logger.error(f"Failed to get content for {url}")
        return None
    
    fb_link = get_fb_link(content)
    if fb_link:
        info = extract_info_from_fb(fb_link, driver)
        logger.info(f"{url}: Extracted info from fb: {info}")
    else:   # if the content of the page doesn't have the fb link then extract the info from the web page
        info = extract_info_from_website(content)
        logger.info(f"{url}: Extracted info from website: {info}")
    # check_info_completion(info, logger)
    
    return info


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("--lang=en")
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(20)  # change the page load strategy or timout
    return driver

def main(urls):
    driver = get_driver()
    logger = create_logger()
    for url in urls:
        info = process_url(url, logger, driver)
        if info:
            print(f"Extracted info from {url}: {info}")

    driver.quit()   
    return

if __name__ == '__main__':
    urls = [
        'https://dottirhotyoga.squarespace.com/workshops',
        'https://downtoearthlondon.co.uk/workshops/',
        'https://downwarddog.com/class-schedule/',
        'https://drivefitnessstudio.com/bootcamp/',
        'https://pbn.haus/',
        'https://drogadomilosci.com/proces/',
        'https://dte-yoga.com/2023/01/07/explore-our-diverse-yoga-classes-at-dte-yoga-in-port-saint-lucie/',
        'https://earthworm-quillfish-g2gx.squarespace.com/events/yin-sound-july',
        'https://earthworm-saxophone-epza.squarespace.com/special-promotion',
        'https://earthyogastudio.com/schedule'
    ]
    main(urls)

    

