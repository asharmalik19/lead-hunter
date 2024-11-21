import re
from bs4 import BeautifulSoup

with open("content.txt", "r", encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, "html.parser")
text = soup.get_text(strip=True)

usa_address_pattern = (
    r'(\d+\s[A-Za-z0-9\-\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}(?:\s\d{5})?(?:,\s[A-Za-z\s]+)?'  # Street, city, state, ZIP with optional country
    r'|[A-Za-z0-9\-\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}'                              # Street, city, state, ZIP
    r'|\d+\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}'                                            # Numbered street, state, ZIP
    r'|\d+\s[A-Za-z0-9\-\s]+(?:,\s(?:Apt|Unit|Suite|#)\s?\d+[A-Za-z]?\.?)?,\s[A-Za-z\s]+(?:,\s[A-Z]{2}\s\d{5})?'  # Street, Apt/Unit/Suite, city, state, ZIP
    r'|[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}'                                                 # City, state, ZIP
    r'|\d+\s[A-Za-z0-9\-\s]+,\s[A-Za-z\s]+)'                                          # Street and city only
)

# Extract potential addresses
potential_addresses = []
# for pattern in patterns:
#     matches = re.findall(pattern, text)
#     potential_addresses.extend(matches)
matches = re.findall(usa_address_pattern, text)
potential_addresses.extend(matches)

# Remove duplicates (if any)
potential_addresses = list(set(potential_addresses))

# Print all found potential addresses
for address in potential_addresses:
    print("Potential address found:", address)
