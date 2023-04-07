# create inventory.json via https://app.parsio.io/642fc366382d30000e4af4ba/parsed
# import table data into https://drive.google.com/drive/folders/1RyDaxeqhiSQOQSQte2NKvpw3-sOQ3kJv sheet
#
import os
from datetime import datetime

article_data = [
    {"cleaned_article_name": "KETO Coffee 5er", "VariationId": "1677", "VariationName": "KETO-COFFEE-BOX"},
    {"cleaned_article_name": "KETO-CREAMER-CLASSIC", "VariationId": "1267", "VariationName": "KETO CREAMER CLASSIC"},
    {"cleaned_article_name": "KETO-CREAMER-VANILLA", "VariationId": "1266", "VariationName": "KETO CREAMER VANILLE"},
    {"cleaned_article_name": "MCT- POWDER", "VariationId": "1711", "VariationName": "KETO MCT POWDER 200g"},
    {"cleaned_article_name": "KG-KAKAO", "VariationId": "1244", "VariationName": "KGR-KAKAO-250g"},
    {"cleaned_article_name": "KG-NUSS", "VariationId": "1241", "VariationName": "KGR-NUSS-250g"},
    {"cleaned_article_name": "KG-HIMBEER", "VariationId": "1437", "VariationName": "KGR-HIMBEER-CHOCO-250g"},
    {"cleaned_article_name": "Brownie Chrisp Riegel (Vanille) violette", "VariationId": "1441", "VariationName": "MCT-BAR-BROWNIE"},
    {"cleaned_article_name": "Peanut Butter Riegel orange", "VariationId": "1443", "VariationName": "MCT-BAR-PEANUT"},
    {"cleaned_article_name": "TASSE-SUPERPOWER", "VariationId": "1366", "VariationName": "Tasse Einhorn Superpower"},
    {"cleaned_article_name": "TASSE-KEEPCALM in Schwarz", "VariationId": "1367", "VariationName": "Tasse Keep Calm"},
    {"cleaned_article_name": "KAKAO-DRINK", "VariationId": "1668", "VariationName": "KAKAO-DRINK"},
    {"cleaned_article_name": "MCT-Oil Classic C8/C10 500ml", "VariationId": "1736", "VariationName": "MCT ÖL Classic 1x500ml"},
    {"cleaned_article_name": "MCT-Oil Classic C8/C10 100ml", "VariationId": "1805", "VariationName": "MCT ÖL Classic 1x100ml"},
    {"cleaned_article_name": "MCT-Oil Premium C8 500ml", "VariationId": "1803", "VariationName": "MCT ÖL Premium 1x500ml"},
    {"cleaned_article_name": "MCT-Oil Premium C8 100ml", "VariationId": "1804", "VariationName": "MCT ÖL Premium 1x100ml"},
    {"cleaned_article_name": "Rasberry Lime Flavour 300g", "VariationId": "1830", "VariationName": "EAA Pulver Himbeere Limette 1x300g"},
    {"cleaned_article_name": "Sweet Orange Flavour 300g", "VariationId": "1831", "VariationName": "EAA Pulver Sweet Orange 1x300g"},
    {"cleaned_article_name": "KETO-KOMPASS", "VariationId": "1251", "VariationName": "BUCH KETO-KOMPASS"},
    {"cleaned_article_name": "Cocktail Buch", "VariationId": "1431", "VariationName": "BUCH COCKTAIL"},
    {"cleaned_article_name": "KETO-Alles, was sie wissen müssen BUCH", "VariationId": "1782", "VariationName": "KETO-ALLES-BUCH"},
    {"cleaned_article_name": "TRINKMAHLZEIT Schoko", "VariationId": "1384", "VariationName": "TMZ-SCHOKO"},
    {"cleaned_article_name": "Ketonella Haselnuss Creme", "VariationId": "1075", "VariationName": "HASELNUSS-CREME"},
    {"cleaned_article_name": "KG-NUSS Portions", "VariationId": "1429", "VariationName": "PORTIONSBEUTEL-NUSS-40g"},
    {"cleaned_article_name": "Theken Display NUSS Trays", "VariationId": "", "VariationName": ""},
    {"cleaned_article_name": "BITES-COCOA", "VariationId": "", "VariationName": ""},
    {"cleaned_article_name": "BITES-COCONUT", "VariationId": "", "VariationName": ""},
    {"cleaned_article_name": "BITES-HIMBEERE", "VariationId": "", "VariationName": ""},
    {"cleaned_article_name": "TRINKMAHLZEIT Vanille&Zimt", "VariationId": "1385", "VariationName": "KETO TRINKMAHLZEIT VANILLE ZIMT 650g"},
]

def find_variation(article_data, cleaned_article_name):
    for item in article_data:
        if item["cleaned_article_name"] == cleaned_article_name:
            return item["VariationId"], item["VariationName"]
    return None, None

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
    article_name = re.sub(r'Verpackung', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'Retoure', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'Beutel', '', article_name, flags=re.IGNORECASE)
    article_name = re.sub(r'GT\d+', '', article_name, flags=re.IGNORECASE)    
    article_name = re.sub(r'MHD', '', article_name, flags=re.IGNORECASE)  # Remove "MHD"
    article_name = re.sub(r'[“”"„!\:]', '', article_name)  # Remove quote characters
    return article_name.strip()

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory to construct the file path
file_path = os.path.join(script_dir, 'inventory.json')

# Load JSON data from file or API response
with open(file_path, 'r', encoding="utf-8") as f:
    inventory_data = json.load(f)

print("VariationId,VariationName,CleanedName,BBD,count")
# Iterate over each inventory item and extract article data
for item in inventory_data[0]['inventar']:
    if item["stueck"] == "0":
        continue
    if not item["stueck"].isdigit():
        continue
    article = item['artikel']
    if not article.strip():
        continue
    if "BITES" in article:
        continue
    date = parse_mhd_date(article)
    cleaned_article_name = clean_article_name(article)
    variation_id, variation_name = find_variation(article_data, cleaned_article_name)
    print(variation_id, ",", variation_name, ",", cleaned_article_name, ",", date, ",", item["stueck"])