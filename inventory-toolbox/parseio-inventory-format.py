import json
import re
import os
import datetime

# Regular expression pattern to match MHD date
mhd_pattern = r'MHD\s+(\d{2}\.\d{2}\.\d{2}|\d{2}\.\d{4}|\d{2}\/\d{2}|\d{2}\.\d{2}\.\d{4})'

# Function to parse MHD date from article name
def parse_mhd_date(article_name):
    match = re.search(mhd_pattern, article_name)
    if match:
        date_str = match.group(1)
        if len(date_str) == 8:
            date = datetime.datetime.strptime(date_str, '%d.%m.%y').strftime('%Y-%m-%d')
        elif len(date_str) == 5:
            date = datetime.datetime.strptime(date_str, '%m/%y').strftime('%Y-%m-%d')
        elif len(date_str) == 7:
            date = datetime.datetime.strptime(date_str, '%d.%Y').strftime('%Y-%m-%d')
        else:
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y').strftime('%Y-%m-%d')
        return date
    else:
        return None

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory to construct the file path
file_path = os.path.join(script_dir, 'inventory.json')

# Load JSON data from file or API response
with open(file_path, 'r') as f:
    inventory_data = json.load(f)

# Iterate over each inventory item and extract article data
for item in inventory_data[0]['inventar']:
    article = item['artikel']
    # Your code to split and extract article name and BBD date goes here
    # ...
    m = re.match(r"(.+?)\s*(?:MHD:?|Haltbar bis:?|Best before:?|BB:?)?\s*([\d./]{5,10})(?:\s|\w|$)", article)
    if m:
        name = m.group(1).strip()
        date = parse_mhd_date(article)
        print(name)
        print(date)
