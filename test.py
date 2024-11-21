import pandas as pd
from urllib.parse import urlparse

def get_domain_with_scheme(url):
    """Extracts the scheme and domain from a URL, adding 'http' if no scheme is provided."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Add a default scheme if missing
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Validate domain (basic check for at least one dot in the netloc)
    if '.' in parsed_url.netloc:
        return domain
    else:
        return None


# Read the file containing URLs
input_file = 'momence_websites.xlsx'  # Replace with your actual file name
output_file = 'cleaned_momence_websites.csv'

# Load the URLs into a pandas DataFrame
df = pd.read_excel(input_file)

# Apply the function to extract scheme and domain
df['domain'] = df["Momence Merchant URL's"].apply(get_domain_with_scheme)

# Write the results to a new file
df[['domain']].to_csv(output_file, index=False, header=False)

print(f"Domain parts saved to {output_file}")

