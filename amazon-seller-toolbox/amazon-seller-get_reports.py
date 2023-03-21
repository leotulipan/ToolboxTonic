# To get started, you need to install the Selenium package and Microsoft Edge WebDriver:

# Install Selenium:
# pip install selenium
# or
# conda install selenium
#
# Download the appropriate Microsoft Edge WebDriver from the following link: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Make sure you download the WebDriver version that matches your installed version of Microsoft Edge.

# Set the PATH environment variable to include the directory where you downloaded the Edge WebDriver.


from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

# Path to the Edge WebDriver executable
driver_path = r"C:\Users\leo\Downloads\edgedriver\msedgedriver.exe"

# Create a new Edge browser instance and start it
browser = webdriver.Edge(executable_path=driver_path)

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

# Close the browser
browser.quit()