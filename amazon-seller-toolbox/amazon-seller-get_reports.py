# To get started, you need to install the Selenium package and Microsoft Edge WebDriver:

# Install Selenium:
#  pip install selenium==4.4.3

# Download the appropriate Microsoft Edge WebDriver from the following link: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Make sure you download the WebDriver version that matches your installed version of Microsoft Edge.

# Set the PATH environment variable to include the directory where you downloaded the Edge WebDriver.

from selenium import webdriver
from selenium.webdriver.edge import service
import os

# Path to the Edge WebDriver executable (in users Downloads Folder)
driver_path = os.path.join("C:\\", "Users", os.environ['USERNAME'], "Downloads", "edgedriver", "msedgedriver.exe")

# Set the path to the user data directory 
local_app_data = os.environ['LOCALAPPDATA']
user_data_dir = os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data')

# Initialize Edge options
# edge_options = Options()
# edge_options.arguments.append(f'--user-data-dir={user_data_dir}')

edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
edge_options.arguments.append(f'--user-data-dir={user_data_dir}')

# Initialize the WebDriver with the custom profile
browser = webdriver.Edge(executable_path=driver_path, options=edge_options)

# Navigate to a specific URL
browser.get("https://duckduckgo.com")

# Locate the input element and send the desired text
search_input = browser.find_element_by_id("search_form_input_homepage")
search_input.send_keys("Python Selenium with Edge examples")

# Option 1: Submit the form by calling the submit method on the input element
search_input.submit()

# Option 2: Locate the search button and click it to submit the form
# search_button = browser.find_element(By.ID, "search_button_homepage")
# search_button.click()

# Wait for the user to press Enter to close the browser
input("Press Enter to close the browser...")

# next step: https://sellercentral.amazon.de/payments/past-settlements?ref_=xx_settle_ttab_dash

# Close the browser
browser.quit()