import pandas as pd
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# import the main function
from src.main import main


urls = pd.read_csv('cleaned_momence_websites.csv')['domain'].iloc[:20].tolist()

main(urls)