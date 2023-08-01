# Import the required libraries
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
#Use to clean the code
from retailers_links import retailersFile
from input_validation import get_integer_input
from browers_choice import initialize_driver
import version_checker

#Version checker will never force it to auto install.
if __name__ == "__main__":
    # Replace this with your current software version
    current_version = "1.0.0"

    # Replace this URL with the GitHub API endpoint for your repository
    repo_url = "https://api.github.com/repos/coolyer/coolyerScraper/releases/latest"

    latest_version = version_checker.get_latest_version(repo_url)
    if latest_version:
        if current_version == latest_version:
            print(f"Your software is up-to-date. Current version: {current_version}")
        else:
            print(f"Your software is outdated. Current version: {current_version}. Latest version: {latest_version}")


while True:
    # Get the browser choice 
    browser_choice = get_integer_input("Choose a browser:\n1. Firefox\n2. Chrome\nPlease choose a number only: ")
    
    # Web wait time
    webWaitTime = get_integer_input("Enter your estimated website loading time based on your connection speed: ")
    
    # Product name from the user
    product_name = input("Enter the product name: ")
    
    # Initialize the driver based on the browser choice using the function from browser_handler.py
    driver = initialize_driver(browser_choice)
    
    # Define a function to scrape the product prices and names from different retailers
    def scrape_product_prices(product_name):
        # Define a dictionary of retailers and their search URLs grabbing from the retailersSites.py
        retailers = retailersFile()

        # Define an empty dictionary to store the product prices and names
        product_data = {}
        
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
                    first_tile = driver.find_element(By.XPATH, '(//li[@class="product-list--list-item first"])[1]')

                        # Check if the first tile contains the offer text element
                    try:
                            clubcard_price_element = first_tile.find_element(By.XPATH, './/span[contains(@class, "offer-text")]')
                            # Retrieve the clubcard price element if it exists
                            clubcard_price = clubcard_price_element.text.strip()
                    except NoSuchElementException:
                            # If no clubcard price element is found, set the clubcard_price to an empty string
                            clubcard_price = ''
                    # Find the element that contains the clubcard price, if any, and extract its text
                    
                    # Find the element that contains the regular price and wait for it to be visible
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'beans-price__text'))
                    )
                    # Find the element that contains the product name and wait for it to be visible, excluding some unwanted elements by their text content
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "styled__Text-sc-1xbujuz-1")][contains(@class, "beans-link__text")][not(text()="Skip to main content" or text()="Skip to search" or text()="Skip to basket" or text()="Register" or text()="Sign in" or text()="Contact us" or text()= "Help" or text()="Feedback")]')))
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")
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
              
            elif retailer == "B&M":
                try:
                    
                    first_tile = driver.find_element(By.XPATH, '(//li[@class="col-6 col-landscape-4 mt-3 pt-lg-3 px-lg-3"])[1]')

                        # Check if the first tile contains the offer text element
                    try:
                            bmdeals_elements = first_tile.find_element(By.XPATH, './/span[contains(@class, "badge badge-primary text-wrap")]')
                            # Retrieve the clubcard price element if it exists
                            bmdeals = bmdeals_elements.text.strip()
                    except NoSuchElementException:
                            # If no clubcard price element is found, set the clubcard_price to an empty string
                            bmdeals = ''
                    # Find the element that contains the clubcard price, if any, and extract its text
                    # Find the price element on the B&M website
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "d-block h5 mb-0 text-secondary bm-line-compact")][contains(@class, "bm-line-compact")]'))
                    )
                    # Find the item name element on the B&M website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'bm-product-stretch-link')))
                except:
                    print(f"{retailer} error: {str(Exception)}")
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
                product_data[retailer] = (name, price, bmdeals)      
            
            elif retailer == "Sainsburys":
                try:
                    first_tile = driver.find_element(By.XPATH, '(//li[@class="pt-grid-item ln-o-grid__item ln-u-1/2@xs ln-u-1/3@sm ln-u-1/4@md ln-u-1/5@xl"])[1]')

                    # Check if the first tile contains the nectar price element
                    try:
                        nectar_price_element = first_tile.find_element(By.XPATH, './/span[contains(@class, "pt__cost--price")]')
                        # Retrieve the nectar price element if it exists
                        nectar_price = "Nectar price:" + nectar_price_element.text.strip() 
                    except NoSuchElementException:
                        # If no nectar price element is found, set the nectar_price to an empty string
                        nectar_price = ''

                    # Find the element that contains the regular price and wait for it to be visible
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'pt__cost__retail-price'))
                    )
                    # Find the item name element on the Sainsburys website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.XPATH, '//a[contains(@class, "pt__link")]'))
                    )

                    # Extract the product name from the item name element
                    name_html = item_name_element.get_attribute('outerHTML')
                    soup = BeautifulSoup(name_html, 'html.parser')
                    name = soup.get_text(strip=True)

                    # Extract the regular price from the price element
                    price_html = price_element.get_attribute('innerHTML')
                    soup = BeautifulSoup(price_html, 'html.parser')
                    price = soup.get_text(strip=True)

                    # Store the product name, regular price, and nectar price (if any) in the dictionary
                    product_data[retailer] = (name, price, "Nectar Price:", nectar_price)
                except Exception as e:
                    print(f"{retailer} Item not found/error: {str(e)}")
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
                product_data[retailer] = (name, price, nectar_price)
            
            elif retailer == "Iceland":
                try:
                    # Find the price element on the B&M website
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'product-sales-price'))
                    )
                    # Find the item name element on the B&M website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'name-link')))
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
                  
            elif retailer == "Poundland":
                try:
                    # Find the price element on the B&M website
                    price_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'price'))
                    )
                    # Find the item name element on the B&M website
                    item_name_element = WebDriverWait(driver, webWaitTime).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'product-item-link')))
                except Exception as e:
                    print(f"{retailer} Item not found/error: {str(e)}")
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
        name, price, clubcard_price, nectar_price, bmdeals = data + ("",) * (5 - len(data))
        print(f"| {retailer}: {name}| Regular Price: {price}| {clubcard_price} {nectar_price} {bmdeals}") # Use currency symbol and clubcard price and nectar price

    # Ask the user if they want to search for another product
    print("Occasionally, the program may fetch an incorrect clubcard/Nectar prices")
    another_search = input("Do you want to search for another product? (yes/no): ").lower()
    if another_search != "yes":
        break # Exit the loop if the user says no

# End of loop, exit the program
print("Thank you for using the CoolyerScraper. Please consider improving via code inputs or ideas or donating(Not needed but will be apprecited). Goodbye! ")

