import requests
import re
import phonenumbers
import pyap
from phonenumbers.phonenumberutil import NumberParseException
from geopy.geocoders import Nominatim


def verify_address(address):
    geolocator = Nominatim(user_agent="my app")
    address = geolocator.geocode(address)
    if address:
        return True
    else:
        return False

def extract_info(content):
    info = {}
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    # Extract the first email
    email_match = email_pattern.search(content)
    if email_match:
        info['Email'] = email_match.group().strip()

    # Extract the phone number
    regions = ['US', 'GB', 'CA', 'AU']
    found = False

    for region in regions:
        numbers = phonenumbers.PhoneNumberMatcher(content, region)
        for number in numbers:
            print(f'number matched: {number.raw_string}')
            try:
                parsed_number = phonenumbers.parse(number.raw_string, region)
                found = True
                info['Phone'] = number.raw_string
                break
            except NumberParseException:
                print(f'error parsing number: {number.raw_string}')
        if found:
            break

    # Extract the address
    found_addresses = set()
    supported_regions_for_addresses = ['US', 'GB', 'CA']
    for region in supported_regions_for_addresses:
        addresses = pyap.parse(content, country=region)
        for address in addresses:
            found_addresses.add(str(address))
    for address in found_addresses:
        print(f'address matched: {address}')
        if verify_address(address):
            info['Address'] = address
            break           
    return info