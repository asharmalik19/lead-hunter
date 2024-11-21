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
from utils import extract_info
import logging
from config_logger import create_logger

"""
Both the scrape_fb and scrape_website module uses the same function for scraping the main required info. If additional info is available on the fb page which is not in the website, it can be added here in the fb module or if the approach needs for scraping the fb needs to be changed, it can be done here.
"""


logger = create_logger('Lead_hunter_facebook')

def get_business_type(intro_section):
    business_type = intro_section.find_all('div')[0].text.strip()
    return business_type.split(' ')[2]

def get_business_name(soup):
    business_name = soup.select_one('h1.html-h1').text
    return business_name.replace('\xa0', '')

def close_popup(driver):
    popup_closed = False
    cancel_xpath = '//div[@aria-label="Close"]'
    try:
        cancel_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, cancel_xpath)))
        cancel_button.click()
        popup_closed = True
    except TimeoutException:
        return popup_closed
    return popup_closed

def extract_info_from_fb(fb_link, driver):
    """
    Extracts information from a Facebook page.

    Args:
        fb_link (str): The URL of the Facebook page.
        driver (webdriver.Chrome): The Selenium WebDriver instance.

    Returns:
        dict: A dictionary containing the extracted information with the following keys:
            - facebook_email (str): The email address.
            - facebook_phone (str): The phone number.
            - facebook_address_list (str): The address.
            - facebook_business_type (str): The type of business.
            - facebook_business_name (str): The name of the business.
    """

    driver.get(fb_link)

    if not close_popup(driver):
        logger.info(f'popup did not appear for {fb_link}')
        return {}
    logger.info(f'popup succesfully closed for {fb_link}')
    fb_page_source = driver.page_source
    soup = BeautifulSoup(fb_page_source, 'html.parser')
    intro_section = soup.select_one('div.xieb3on ul')  # narrow down to the intro section in the fb page
    if not intro_section:
        logger.warning(f'intro section not found for {fb_link}')
        return {}
    
    info = extract_info(intro_section.get_text(separator='\n'))  # the separator is essential for email to be correctly extracted
    info['business_type'] = get_business_type(intro_section)
    info['business_name'] = get_business_name(soup)

    info = {f'facebook_{key}': value for key, value in info.items()}
    return info


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'eager'
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)  # change the page load strategy or timout
    return driver


if __name__=='__main__':
    fb_link = 'https://www.facebook.com/6DegreeBurnFitness'
    driver = get_driver()
    info = extract_info_from_fb(fb_link, driver)
    print(info)

    driver.quit()



# write a function for adding two numbers

