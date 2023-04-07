import json
import re
import os
from datetime import datetime

# Search for date patterns in the article string
date_pattern = re.compile(r'\b(\d{1,2})[.](\d{1,2})[.](\d{2}(?:\d{2})?)\b|\b(\d{1,2})[/](\d{2})\b')

def parse_mhd_date(article: str):
    match = date_pattern.search(article)

    if match:
        if match.group(1):
            # dd.mm.yy or dd.mm.YYYY format
            day, month, year = match.group(1), match.group(2), match.group(3)

            # Convert 2-digit years to 4-digit years
            if len(year) == 2:
                year = '20' + year

            # Parse the date
            date = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y").date()
        else:
            # mm/yy format
            month, year = match.group(4), match.group(5)
            year = '20' + year
            date = datetime.strptime(f"01-{month}-{year}", "%d-%m-%Y").date()

        return date
    else:
        return None


# Function to clean article name
def clean_article_name(article_name):
    article_name = re.sub(date_pattern, '', article_name)  # Remove MHD date
    article_name = re.sub(r'abgelaufen!+', '', article_name, flags=re.IGNORECASE)  # Remove "abgelaufen" and exclamation marks
    article_name = re.sub(r'Naehrsinn', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'nachbestellen', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'Verpackung :', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'Beutel', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'GT\d+', '', article_name, flags=re.IGNORECASE)    
    article_name = re.sub(r'MHD', '', article_name, flags=re.IGNORECASE)  # Remove "MHD"
    article_name = re.sub(r'[“”"„!]', '', article_name)  # Remove quote characters
    return article_name.strip()

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory to construct the file path
file_path = os.path.join(script_dir, 'inventory.json')

# Load JSON data from file or API response
with open(file_path, 'r', encoding="utf-8") as f:
    inventory_data = json.load(f)

# Iterate over each inventory item and extract article data
for item in inventory_data[0]['inventar']:
    if item["stueck"] == 0:
        continue
    article = item['artikel']
    if not article.strip():
        continue
    date = parse_mhd_date(article)
    cleaned_article_name = clean_article_name(article)
    print(cleaned_article_name, ",", date, ",", item["stueck"])
