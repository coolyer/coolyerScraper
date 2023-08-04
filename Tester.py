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

    num_tiles_to_search = get_integer_input("Enter the number of tiles to search for: ")
    
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
                    tiles = driver.find_elements(By.XPATH, '//li[@class="product-list--list-item"]')[:num_tiles_to_search]
                    product_data[retailer] = ''
                    for index, tile in enumerate(tiles):
                        try:
                            price_element = WebDriverWait(tile, webWaitTime).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, 'beans-price__text'))
                            )

                            item_name_element = WebDriverWait(tile, webWaitTime).until(
                            EC.visibility_of_element_located((
                                            By.XPATH,
                                            './/span[@class= "styled__Text-sc-1xbujuz-1 ldbwMG beans-link__text"]')))

                            try:
                                clubcard_price_element = tile.find_element(By.XPATH, './/span[contains(@class, "offer-text")]')
                                clubcard_price = clubcard_price_element.text.strip()
                            except NoSuchElementException:
                                clubcard_price = None

                            name_html = item_name_element.get_attribute('outerHTML')
                            soup = BeautifulSoup(name_html, 'html.parser')
                            name = soup.get_text(strip=True)

                            # Extract the regular price from the price element
                            price_html = price_element.get_attribute('innerHTML')
                            soup = BeautifulSoup(price_html, 'html.parser')
                            price = soup.get_text(strip=True)
                            if clubcard_price is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{clubcard_price}\n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                            # Add an error handler or continue based on your needs
                    
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")

            elif retailer == 'Asda':
                try:
                    tiles = driver.find_elements(By.XPATH, '//li[@class=" co-item co-item--rest-in-shelf "]')[:num_tiles_to_search]
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            price_element = WebDriverWait(tile, webWaitTime).until(
                            EC.visibility_of_element_located((By.XPATH, './/strong[contains(@class,"co-product__price")]'))
                            )
                            

                            item_name_element = tile.find_element(By.XPATH, './/h3[@class="co-product__title"]/a[@class="co-product__anchor"]')
                            
                            try:
                                Asdalitres_element = tile.find_element(By.XPATH, './/span[@class="co-product__volume co-item__volume"]')
                                Asdalitres = Asdalitres_element.text.strip()
                                
                            except NoSuchElementException:
                                Asdalitres = None
                            try:
                                deal_element = tile.find_element(By.XPATH, '//a[@data-auto-id="linkPromoDetail"]')
                                deal_text = deal_element.find_element(By.CLASS_NAME, 'link-save-banner-large__config--font-normal').text
                                deal_price = deal_element.find_element(By.CLASS_NAME, 'link-save-banner-large__config--font-huge').text
                                deal_info = f"{deal_text} {deal_price}"
                            except NoSuchElementException:
                                deal_info =""
                            name = item_name_element.text.strip()
                            price_html = price_element.get_attribute('innerHTML')
                            soup = BeautifulSoup(price_html, 'html.parser')
                            price = soup.get_text(strip=True).replace("now", "")
                            
                            
                            
                            
                            if Asdalitres is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {Asdalitres}, Price: {price}|{deal_info}\n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{deal_info}\n")
                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                            # Add an error handler or continue based on your needs
                    
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")
                
                
            elif retailer == 'B&M':
                try:
                    tiles = driver.find_elements(By.XPATH, '//li[@class="col-6 col-landscape-4 mt-3 pt-lg-3 px-lg-3"]')[:num_tiles_to_search]
                    product_data[retailer] = ''
                    for index, tile in enumerate(tiles):
                        try:
                            price_element = WebDriverWait(tile, webWaitTime).until(
                                EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "d-block h5 mb-0 text-secondary bm-line-compact")][contains(@class, "bm-line-compact")]'))
                            )

                            item_name_element = WebDriverWait(tile, webWaitTime).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, 'bm-product-stretch-link')))

                            try:
                                bmdeals_element = tile.find_element(By.XPATH, './/span[contains(@class, "offer-text")]')
                                bmdeals = bmdeals_element.text.strip()
                            except NoSuchElementException:
                                bmdeals = None
                            try:
                                bmoffer_element = tile.find_element(By.XPATH, './/span[contains(@class, "badge badge-primary text-wrap")]')
                                bmoffer = bmoffer_element.text.strip()
                            except NoSuchElementException:
                                bmoffer =None
                                

                            name_html = item_name_element.get_attribute('outerHTML')
                            soup = BeautifulSoup(name_html, 'html.parser')
                            name = soup.get_text(strip=True)

                            # Extract the regular price from the price element
                            price_html = price_element.get_attribute('innerHTML')
                            soup = BeautifulSoup(price_html, 'html.parser')
                            price = soup.get_text(strip=True)
                            if bmdeals is not None and bmoffer is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}| Deals: {bmdeals}, Offers: {bmoffer}|\n")
                            elif bmdeals is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}| Deals: {bmdeals}|\n")
                            elif bmoffer is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}| Offers: {bmoffer}|\n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n") 

                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
                    # Add an error handler or continue based on your needs

                except Exception as e:
                        print(f"{retailer} error: {str(e)}")
         
            elif retailer == 'Sainsburys':
                try:
                    tiles1 = driver.find_elements(By.XPATH, '//li[@class= "pt-grid-item ln-o-grid__item ln-u-1/2@xs ln-u-1/3@sm ln-u-1/4@md ln-u-1/5@xl"]')[:num_tiles_to_search]
                    tiles2 = driver.find_elements(By.XPATH, '//li[@class="gridItem"]')[:num_tiles_to_search]
                    tiles = tiles1 + tiles2
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            price_element1 = tile.find_elements(By.XPATH, './/p[contains(@class, "pricePerUnit")]')
                            price_element2 = tile.find_elements(By.XPATH, './/span[contains(@class, "pt__cost__retail-price")]')

                            # Extract the price based on whichever element is found
                            price = ""
                            if price_element1:
                                price = price_element1[0].text.strip()
                            elif price_element2:
                                price = price_element2[0].text.strip()

                            name_element1 = tile.find_elements(By.XPATH, './/a[contains(@class, "pt__link")]')
                            name_element2 = tile.find_elements(By.XPATH, './/div[contains(@class, "productNameAndPromotions")]/h3/a')

                            # Extract the product name based on whichever element is found
                            name = ""
                            if name_element1:
                                name = name_element1[0].text.strip()
                            elif name_element2:
                                name = name_element2[0].text.strip()
                            try:
                                nectar_price_element1 = tile.find_elements(By.XPATH, './/p[contains(@class, "pricePerUnit nectarPrice")]')
                                nectar_price_element2 = tile.find_elements(By.XPATH, './/span[contains(@class, "pt__cost--price")]')
                                # Extract the nectar price based on whichever element is found
                                nectar_price = ""
                                if nectar_price_element1:
                                    nectar_price = "Nectar price: " + nectar_price_element1[0].text.strip()
                                elif nectar_price_element2:
                                    nectar_price = "Nectar price: " + nectar_price_element2[0].text.strip()
                            except NoSuchElementException:
                                 nectar_price = ''

                           

                            # Extract the regular price from the price element
                            
                            product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{nectar_price}\n")
                           
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
                except Exception as e:
                        print(f"{retailer} error: {str(e)}")
                    
                
                
        # Close the browser window
        driver.quit()

        # Return the dictionary with the scraped data
        return product_data

    results = scrape_product_prices(product_name)
    
    # Display the results in a markdown table
    print(f"## Price comparison for {product_name}")
    for retailer, data in results.items():
        # Print the retailer and then the data.
        print(f"{retailer}:\n{data}")
        
    # Ask the user if they want to search for another product
    #print("Occasionally, the program may fetch an incorrect clubcard/Nectar prices")
    another_search = input("Do you want to search for another product? (yes/no): ").lower()
    if another_search != "yes":
        break # Exit the loop if the user says no

# End of loop, exit the program
print("Thank you for using CoolyerScraper. Please consider improving via code inputs or ideas or donating(Not needed but will be apprecited),\nGoodbye! ")


