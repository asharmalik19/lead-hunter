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

"""
Both the scrape_fb and scrape_website module uses the same function for scraping the main required info. If additional info is available on the fb page which is not in the website, it can be added here in the fb module or if the approach needs for scraping the fb needs to be changed, it can be done here.
"""

# def scrape_info_section(fb_content):
#     soup = BeautifulSoup(fb_content, 'html.parser')
#     intro_ul = soup.select_one(By.CSS_SELECTOR, 'div.xieb3on ul')
#     info_divs = intro_ul.find_all('div')

#     for div in info_divs:
#         text = div.text
#         if '@' in text:
#             info['business_email'] = text
#         elif 'www.' in text or '.com' in text:
#             info['business_website'] = text
#         elif text.startswith('+') or '-' in text:       #any(char.isdigit() for char in text)
#             info['phone_number'] = text
#         elif text.endswith('Street') or text.endswith('Avenue') or text.endswith('Road') or any(c.isdigit() for c in text):
#             info['business_address'] = text
#         elif 'Page' in text:
#             info['business_type'] = text.split(' ')[1]

def get_business_type(intro_section):
    business_type = intro_section.find_all('div')[0].text.strip()
    return business_type.split(' ')[2]

def get_business_name(soup):
    business_name = soup.select_one('h1.html-h1').text
    return business_name.replace('\xa0', '')


def extract_info_from_fb(fb_link, driver):

    driver.get(fb_link)
    cancel_xpath = '//div[@aria-label="Close"]'
    try:
        cancel_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, cancel_xpath)))
    except TimeoutException:
        print('cancel button did not appear')
        driver.save_screenshot('cancel_button.png')
        return None
    cancel_button.click()

    fb_page_source = driver.page_source
    soup = BeautifulSoup(fb_page_source, 'html.parser')
    intro_section = soup.select_one('div.xieb3on ul')  # narrow down to the intro section in the fb page
    info = extract_info(intro_section.get_text(separator='\n'))  # extract the info from the intro_section

    info['business_type'] = get_business_type(intro_section)
    info['business_name'] = get_business_name(soup)

    return info


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("--lang=en")
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(20)  # change the page load strategy or timout
    return driver


if __name__=='__main__':
    fb_link = 'https://www.facebook.com/chevylaurent'
    driver = get_driver()
    info = extract_info_from_fb(fb_link, driver)
    print(info)

    driver.quit()


