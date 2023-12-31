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

while True:
    # Web wait time
    webWaitTime = 4
    
    # Product name from the user
    product_name = input("Enter the product name: ")

    # Not Needed anymore. Can be readadded by doing [:num_tiles_to_search] on each retailers tiles search html.
    # Added to Json File.
    #num_tiles_to_search = get_integer_input("Enter the number of tiles to search for: ")

    # Get browser the user chooses.
    #browser_choice = get_integer_input("Choose a browser:\n1. Firefox\n2. Chrome\n3. Edge\nPlease choose a number only: ")
    while True:
            try:
                browser_choice = get_integer_input("Choose a browser:\n1. Firefox\n2. Chrome\n3. Edge\nPlease choose a number only: ")
                if browser_choice in (1, 2, 3):
                    driver = initialize_driver(browser_choice)
                    break  # Valid choice, exit the loop
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            # Initialize the driver based on the browser choice using the function from browser_handler.py
            

    # Define a function to scrape the product prices and names from different retailers
    def scrape_product_prices(product_name):
        # Define a dictionary of retailers and their search URLs grabbing from the retailersSites.py
        retailers = retailersFile()

        # Define an empty dictionary to store the product prices and names
        product_data = {}
        # Loop through each retailer and their search URL
        for retailer, url in retailers.items():
            retailers = retailersFile()
            # Construct the full search URL by appending the product name to the base URL
            search_url = retailers[retailer]['url'] + product_name
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
                    tiles = driver.find_elements(By.XPATH, '//li[@class="product-list--list-item"]')[:retailers[retailer]['num_tiles_to_search']]
                    product_data[retailer] = ''
                    for index, tile in enumerate(tiles):
                        try:
                            price_element = WebDriverWait(tile, webWaitTime).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, 'beans-price__text'))
                            )

                            item_name_element = WebDriverWait(tile, webWaitTime).until(
                            EC.visibility_of_element_located((
                                            By.XPATH,
                                            './/span[@class= "styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text"]')))

                            pricePerMil_element = WebDriverWait(tile, webWaitTime).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, '.styled__StyledFootnote-sc-119w3hf-7.icrlVF.styled__Subtext-sc-8qlq5b-2.bNJmdc.beans-price__subtext')))
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
                            pricePerMil = pricePerMil_element.text.strip()
                            if clubcard_price is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} {pricePerMil}|{clubcard_price}\n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} {pricePerMil}|\n")
                        except Exception as e:
                                pass
                            # Add an error handler or continue based on your needs
                    
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")

            elif retailer == 'Asda':
                try:
                    tiles = driver.find_elements(By.XPATH, '//li[@class=" co-item co-item--rest-in-shelf "]')[:retailers[retailer]['num_tiles_to_search']]
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
                    tiles = driver.find_elements(By.XPATH, '//li[@class="col-6 col-landscape-4 mt-3 pt-lg-3 px-lg-3"]')[:retailers[retailer]['num_tiles_to_search']]
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
                    tiles1 = driver.find_elements(By.XPATH, '//li[@class= "pt-grid-item ln-o-grid__item ln-u-1/2@xs ln-u-1/3@sm ln-u-1/4@md ln-u-1/5@xl"]')[:retailers[retailer]['num_tiles_to_search']]
                    tiles2 = driver.find_elements(By.XPATH, '//li[@class="gridItem"]')[:retailers[retailer]['num_tiles_to_search']]
                    tiles = tiles1 + tiles2
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            price_element1 = tile.find_elements(By.XPATH, './/div[@class = "pricing"]/p[@class = "pricePerUnit"]')
                            price_element2 = tile.find_elements(By.XPATH, './/span[contains(@class, "pt__cost__retail-price pt__cost__retail-price--with-nectar-not-associated")]')
                            price_element3 = tile.find_elements(By.CLASS_NAME, 'pt__cost__retail-price')
                            # Extract the price based on whichever element is found
                            price = ""
                            if price_element1:
                                price = price_element1[0].text.strip()
                            elif price_element2:
                                price = price_element2[0].text.strip()
                            elif price_element3:
                                price = price_element3[0].text.strip()
                                
                            name_element1 = tile.find_elements(By.XPATH, './/a[contains(@class, "pt__link")]')
                            name_element2 = tile.find_elements(By.XPATH, './/div[contains(@class, "productNameAndPromotions")]/h3/a')

                            # Extract the product name based on whichever element is found
                            name = ""
                            if name_element1:
                                name = name_element1[0].text.strip()
                            elif name_element2:
                                name = name_element2[0].text.strip()
                            try:
                                nectar_price_element1 = tile.find_elements(By.XPATH, './/div[@class = "pricing"]/p[@class = "pricePerUnit nectarPrice"]')
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
                    
            elif retailer == 'Iceland':
                try:
                    tiles = driver.find_elements(By.CLASS_NAME, 'grid-tile ')[:retailers[retailer]['num_tiles_to_search']]
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            price_elements = tile.find_elements(By.XPATH, './/span[@class="product-sales-price"]/span')
                            price = price_elements[0].text.strip()
                            

                            item_name_element = tile.find_element(By.CLASS_NAME, 'name-link')
                            
                            try:
                                iceLandOffers_element = tile.find_element(By.CLASS_NAME, 'price')
                                iceLandOffers = iceLandOffers_element.text.strip()
                                
                            except NoSuchElementException:
                                iceLandOffers = None
                            
                            name = item_name_element.text.strip()
                            
                            
                            if iceLandOffers is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|Multibuy Price: {iceLandOffers} each \n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                        except Exception as e:
                                pass # There is a list index out of range error but shows all the correct prices and products so no idea.
                
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")
                    
            elif retailer == 'Poundshop':
                try:
                    tiles = driver.find_elements(By.XPATH, '//li[@class= "rrp item product product-item"]')[:retailers[retailer]['num_tiles_to_search']]
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            price_element = WebDriverWait(driver, webWaitTime).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, 'price'))
                            )
                            

                            item_name_element = tile.find_element(By.CLASS_NAME, 'product-item-link')
                            
                            try:
                                poundShopOffersStart_element = tile.find_element(By.CLASS_NAME, 'price')
                                poundShopOffersStart = poundShopOffersStart_element.text.strip()
                                poundShopOffersExtra_element = tile.find_element(By.CLASS_NAME, 'qty-label')
                                poundShopOffersExtra = poundShopOffersExtra_element.text.strip()
                                poundShopOffers = (f" {poundShopOffersStart} {poundShopOffersExtra}")
                            except NoSuchElementException:
                                poundShopOffers = None
                            
                            name = item_name_element.text.strip()
                            price_html = price_element.get_attribute('innerHTML')
                            soup = BeautifulSoup(price_html, 'html.parser')
                            price = soup.get_text(strip=True).replace("now", "")
                            
                            if poundShopOffers is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: £{price}|{poundShopOffers}\n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: £{price}|\n")
                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                            # Add an error handler or continue based on your needs
                    
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")    

            elif retailer == 'Poundland':
                try:
                    tiles = driver.find_elements(By.XPATH, '//li[@class= " item product product-item c-product c-product__item"]')[:retailers[retailer]['num_tiles_to_search']]
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            price_element = tile.find_elements(By.CLASS_NAME, 'c-product__price')
                            price = price_element[0].text.strip()
                            item_name_element = tile.find_element(By.CLASS_NAME, 'c-product__title')
                            
                            try:
                                poundLandOffers_element = tile.find_element(By.CLASS_NAME, 'c-product__promo')
                                poundLandOffers = poundLandOffers_element.text.strip()
                                
                            except NoSuchElementException:
                                poundLandOffers = None
                            
                            name = item_name_element.text.strip()
                            
                            if poundLandOffers is not None:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{poundLandOffers} each \n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                            # Add an error handler or continue based on your needs
                    
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")  
            elif retailer == 'Aldi':
                try:
                    tiles = driver.find_elements(By.XPATH, '//div[@data-qa="search-result"]')[:retailers[retailer]['num_tiles_to_search']]
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                            try:
                                name_element = tile.find_element(By.XPATH, './/a[@data-qa="search-product-title"]')
                                price_element = tile.find_element(By.XPATH, './/span[@class="h4"]/span')

                                # Extract the product name and price
                                name = name_element.text.strip()
                                price = price_element.text.strip()

                                # Add the extracted data to product_data
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                            except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                except Exception as e:
                    print(f"{retailer} error: {str(e)}")
                    
            elif retailer == 'Morrisons':
                try:
                    tiles = driver.find_elements(By.XPATH, '//li[contains(@class, "fops-item") and contains(@class, "fops-item--on_offer") or contains (@class, "fops-item fops-item--cluster")]')[:retailers[retailer]['num_tiles_to_search']]
                    product_data[retailer] = ""
                    for index, tile in enumerate(tiles):
                        try:
                            name_element = tile.find_element(By.XPATH, './/div[@class ="fop-description"]/h4[@class="fop-title"]')
                            price_element = tile.find_elements(By.XPATH, './/div[@class = "price-group-wrapper"]/span[@class="fop-price"]')
                            price_element1 = tile.find_elements(By.XPATH, './/div[@class = "price-group-wrapper"]/span[@class ="fop-price price-offer"]')
                            price = ""
                            if price_element:
                                price = price_element[0].text.strip()
                            
                            elif price_element1:
                                price = price_element1[0].text.strip()
                            # Extract the product name and price
                            name = name_element.text.strip()
                            try:
                            # Check if there's a promotional offer
                                promo_element = tile.find_element(By.XPATH, './/a[@class="fop-row-promo promotion-offer"]/span')
                                promo = promo_element.text.strip()
                            except NoSuchElementException:
                                promo = None
                            try:
                                weight_element = tile.find_element(By.XPATH, './/span[@class="fop-catch-weight"]')
                                weight = weight_element.text.strip()
                            except NoSuchElementException:
                                weight = None
                            # Add the extracted data to product_data
                            if promo:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {weight}, Price: {price}|{promo}\n")
                            else:
                                product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {weight}, Price: {price}|\n")
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
        
    print("If the retailer shows no product its either error, the product as taken it to the exact product page which the code cant read or maybe a error.\nBefore reporting do check the website for the product.")    
    another_search = input("Do you want to search for another product? (yes/no): ").lower()
    if another_search != "yes":
        break # Exit the loop if the user says no

# End of loop, exit the program
print("Thank you for using CoolyerScraper. Please consider improving via code inputs or ideas or donating(Not needed but will be apprecited),\nGoodbye! ")
exit(0)


