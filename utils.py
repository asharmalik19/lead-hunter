import requests
import re
import phonenumbers
import pyap
from phonenumbers.phonenumberutil import NumberParseException
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup


USA_ADDRESS_PATTERN = (
    r'(\d+\s[A-Za-z0-9\-\.\s]+,\s[A-Za-z\s]+,\s[A-Z]{2},?\s[A-Za-z\s]+(?:,\s[A-Za-z\s]+)?'  # Street, city, state, country, optional state again
    r'|[A-Za-z0-9\-\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}'                                    # Street, city, state, ZIP
    r'|\d+\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}'                                                  # Numbered street, state, ZIP
    r'|\d+\s[A-Za-z0-9\-\.\s]+(?:,\s(?:Apt|Unit|Suite|#)\s?\d+[A-Za-z]?\.?)?,\s[A-Za-z\s]+(?:,\s[A-Z]{2}\s\d{5})?'  # Street, Apt/Unit/Suite, city, state, ZIP
    r'|[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}'                                                       # City, state, ZIP
    r'|\d+\s[A-Za-z0-9\-\.\s]+,\s[A-Za-z\s]+)'                                              # Street and city only
)
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def extract_email(content):
    email_match = EMAIL_PATTERN.search(content)
    if email_match:
        return email_match.group().strip()
    return None

 
def extract_phone_number(content):
    regions = ['US', 'GB', 'CA', 'AU']

    for region in regions:
        numbers = phonenumbers.PhoneNumberMatcher(content, region)
        for number in numbers:
            print(f'number matched: {number.raw_string}')
            try:
                parsed_number = phonenumbers.parse(number.raw_string, region)
                return number.raw_string
            except NumberParseException:
                print(f'error parsing number: {number.raw_string}')
    return None

    
def extract_addresses(content):
    potential_addresses = []
    matches = re.findall(USA_ADDRESS_PATTERN, content)
    potential_addresses.extend(matches)

    potential_addresses = list(set(potential_addresses))  # Remove duplicates (if any)
    return potential_addresses


def extract_info(content):
    info = {
        'email': None,
        'phone': None,
        'address_list': None
    }
    info['email'] = extract_email(content)
    info['phone'] = extract_phone_number(content)

    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(strip=True)
    info['address_list'] = extract_addresses(text)          
    return info