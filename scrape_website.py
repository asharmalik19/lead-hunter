import requests
from utils import extract_info
from bs4 import BeautifulSoup
import re


def fetch_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def get_fb_link(content):
    fb_link_selector = 'a[href*="facebook.com"]'
    soup = BeautifulSoup(content, 'html.parser')
    fb_link_tag = soup.select_one(fb_link_selector)
    if fb_link_tag:
        fb_link = fb_link_tag.get('href')
        return fb_link
    return None

def get_company_name(content):
    soup = BeautifulSoup(content, 'html.parser') 
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text().strip()
        
        # Assuming the company name is a part of the title, extract it
        # Example: "Company Name - Some other information"
        company_name = re.split(r'\s[–—-]\s', title_text)[0]
        
        return company_name
    
    return None

def extract_info_from_website(content):
    """
    Extracts information from a website.

    Args:
        content (str): The content of the website.

    Returns:
        dict: A dictionary containing the extracted information with the following keys:
            - website_email (str): The email address.
            - website_phone (str): The phone number.
            - website_address_list (str): The address.
            - website_business_name (str): The name of the business.
    """

    info = extract_info(content)   
    company = get_company_name(content)
    info['business_name'] = company
    
    info = {f'website_{key}': value for key, value in info.items()}
    return info



if __name__ == '__main__':
    url = 'https://heightsites.com/event/fort-tryon-park-walk-thru/'
    content = fetch_url(url)
    if content:
        info = extract_info_from_website(content)  
        print(info)
        # fb_link = get_fb_link(content)


        # info = extract_info_from_webpage(content)
        # print(info)

    # valid = verify_address('805 Woodland St., Ste. 314')

