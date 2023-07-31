# Import the required libraries
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Define a function to get an integer input from the user and validate it
def get_integer_input(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("Invalid input. Please enter a number.")

# Start of loop
while True:
    # Get the browser choice, web wait time, and product name from the user
    browser_choice = get_integer_input("Choose a browser: \n1. Firefox\n2. Chrome\n Please choose a number only: ")
    webWaitTime = get_integer_input("Enter your estimated website loading time based on your connection speed: ")
    product_name = input("Enter the product name: ")

    # Define a function to scrape the product prices and names from different retailers
    def scrape_product_prices(product_name):
        # Define a dictionary of retailers and their search URLs
        retailers = {
            'Tesco': 'https://www.tesco.com/groceries/en-GB/search?query=',
            'Asda': 'https://groceries.asda.com/search/',
            'B&M': 'https://www.bmstores.co.uk/search?q=',
            'Sainsburys': 'https://www.sainsburys.co.uk/gol-ui/SearchResults/',
        }
        # Define an empty dictionary to store the product prices and names
        product_data = {}

        # Choose the browser based on the user's input
        if browser_choice == 1:
            # Firefox
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless=new') # Run the browser in headless mode (without opening a visible browser window)
            options.log.level = "OFF" # Turn off logging messages
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif browser_choice == 2:
            # Chrome
            options = webdriver.ChromeOptions()    
            options.add_argument('--headless=new') # Run the browser in headless mode (without opening a visible browser window)
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        else:
            print("Invalid browser choice. Exiting...")
            exit(1) # Exit the program if the user enters an invalid choice
        
        # Loop through each retailer and their search URL
        for retailer, url in retailers.items():
            # Construct the full search URL by appending the product name to the base URL
            search_url = url + product_name
            # Open the search URL using the chosen browser
            driver.get(search_url)
            # Wait for some time for the web page to load
            time.sleep(webWaitTime)
            # Parse the HTML source of the web page using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            print(f"Scraping: {retailer}")   
            
            # Scrape the data for each retailer using different CSS selectors or XPath expressions
            
            if retailer == 'Tesco':
                try:
                    # Find the element that contains the clubcard price, if any, and extract its text
                    clubcard_price_element = driver.find_element(By.CLASS_NAME, 'offer-text')
                    clubcard_price = clubcard_price_element.get_attribute('innerHTML').strip()
                    # Find the element that contains the regular price and wait for it to be visible
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'beans-price__text'))
                    )
                    # Find the element that contains the product name and wait for it to be visible, excluding some unwanted elements by their text content
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "styled__Text-sc-1xbujuz-1")][contains(@class, "beans-link__text")][not(text()="Skip to main content" or text()="Skip to search" or text()="Skip to basket" or text()="Register" or text()="Sign in" or text()="Contact us" or text()= "Help" or text()="Feedback")]')))
                except:
                    # Handle any errors that might occur during the scraping process and skip this retailer
                    print(f"{retailer}" + " error/Item not found")
                    continue
                
                # Extract the product name and price from the elements
                name_html = item_name_element.get_attribute('outerHTML')
                soup = BeautifulSoup(name_html, 'html.parser')
                name = soup.get_text(strip=True)
                
                price_html = price_element.get_attribute('innerHTML')
                soup = BeautifulSoup(price_html, 'html.parser')
                price = soup.get_text(strip=True)
                
                # Store the product name, price, and clubcard price (if any) in the dictionary
                product_data[retailer] = (name, price, clubcard_price)
            
            elif retailer == "Asda":
                try:
                    # Find the price element on the Asda website
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'co-product__price'))
                    )
                    # Find the item name element on the Asda website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'co-product__anchor')))
                except:
                    print(f"{retailer}" + " error/Item not found")
                    continue
                 
                # Extract the product name from the product name element
                name_html = item_name_element.get_attribute('outerHTML')
                soup = BeautifulSoup(name_html, 'html.parser')
                name = soup.get_text(strip=True)
                
                # Extract the price from the price element
                price_html = price_element.get_attribute('innerHTML')
                soup = BeautifulSoup(price_html, 'html.parser')
                price = soup.get_text(strip=True).replace('now', '')
                
                # Store the product name and price in the dictionary
                product_data[retailer] = (name, price)
            
            elif retailer == "B&M":
                try:
                    # Find the price element on the B&M website
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "d-block h5 mb-0 text-secondary bm-line-compact")][contains(@class, "bm-line-compact")]'))
                    )
                    # Find the item name element on the B&M website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'bm-product-stretch-link')))
                except:
                    print(f"{retailer}" + " error/Item not found")
                    continue
                
                # Extract the product name from the product name element
                name_html = item_name_element.get_attribute('outerHTML')
                soup = BeautifulSoup(name_html, 'html.parser')
                name = soup.get_text(strip=True)
                
                # Extract the price from the price element
                price_html = price_element.get_attribute('innerHTML')
                soup = BeautifulSoup(price_html, 'html.parser')
                price = soup.get_text(strip=True).replace('now', '')
                
                # Store the product name and price in the dictionary
                product_data[retailer] = (name, price)      
            
            elif retailer == "Sainsburys":
                try:
                      # Check if the Nectar price exists on the page
                    nectar_price_element = driver.find_element(By.CLASS_NAME, 'pt__cost--price')
                    nectar_price = nectar_price_element.get_attribute('innerHTML').strip()
                    # Find the regular price element on the Sainsburys website
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'pt__cost__retail-price'))
                        )
                    # Find the item name element on the Sainsburys website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                             EC.visibility_of_element_located((By.XPATH, '//a[contains(@class, "pt__link")]'))
                    )
                except:
                    print(f"{retailer}" + " error/Item not found")
                    continue
                
                # Extract the product name from the product name element
                name_html = item_name_element.get_attribute('outerHTML')
                soup = BeautifulSoup(name_html, 'html.parser')
                name = soup.get_text(strip=True)
                
                # Extract the regular price from the regular price element
                price_html = price_element.get_attribute('innerHTML')
                soup = BeautifulSoup(price_html, 'html.parser')
                price = soup.get_text(strip=True)
                
                 # Store the product name, regular price, and Nectar price (if any) in the dictionary
                product_data[retailer] = (name, price, "Nectar Price:", nectar_price)
        # Close the browser window
        driver.quit()

        # Return the dictionary with the scraped data
        return product_data

    # Call the scrape_product_prices function and get the results
    results = scrape_product_prices(product_name)

    # Display the results in a markdown table
    print(f"## Price comparison for {product_name}")
    for retailer, data in results.items():
        # Use a default value of None for the third and fourth elements if they do not exist
        name, price, clubcard_price, nectar_price = data + ("",) * (4 - len(data))
        print(f"| {retailer}, {name}: Regular Price: {price}| {clubcard_price} {nectar_price}") # Use currency symbol and clubcard price and nectar price

    # Ask the user if they want to search for another product
    another_search = input("Do you want to search for another product? (yes/no): ").lower()
    if another_search != "yes":
        break # Exit the loop if the user says no

# End of loop, exit the program
print("Thank you for using the product scraper. Goodbye!")

