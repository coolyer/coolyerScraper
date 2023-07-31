from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
def scrape_product_prices(product_name):
    retailers = {
        'Tesco': 'https://www.tesco.com/groceries/en-GB/search?query=',
        'Asda': 'https://groceries.asda.com/search/',
        'B&M': 'https://www.bmstores.co.uk/search?q=',
        'Sainsburys': 'https://www.sainsburys.co.uk/gol-ui/SearchResults/',
    }

    product_prices = {}
    item_names = {}
    ########################################################################################################################
    ''' #<-remove this
    # If you want to use Firefox
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless=new')  # Run the browser in headless mode (without opening a visible browser window)

    # Update the path to the GeckoDriver executable based on your system configuration
    geckodriver_path = 'path/to/geckodriver'

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    #driver.implicitly_wait(10)
    ''' #<-remove this
    ########################################################################################################################
    
    
   ########################################################################################################################
    #For Chrome
    options = webdriver.ChromeOptions()
    
    #--headless=new works with loading websites DO NOT change to just --headless
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    ########################################################################################################################
    
    for retailer, url in retailers.items():
        search_url = url + product_name
        driver.get(search_url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(f"Scraping: {retailer}")   

        if retailer == 'Tesco':
            try:
                clubcard_price_element = driver.find_element(By.CLASS_NAME, 'offer-text')
                clubcard_price = clubcard_price_element.get_attribute('innerHTML').strip()
                # Find the price element on the Tesco website
                price_element = WebDriverWait(driver, webWaitTime).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'beans-price__text'))
                )
                # Find the item name element on the Tesco website
                item_name_element = WebDriverWait(driver, webWaitTime).until(
                    EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "styled__Text-sc-1xbujuz-1")][contains(@class, "beans-link__text")][not(text()="Skip to main content" or text()="Skip to search" or text()="Skip to basket" or text()="Register" or text()="Sign in" or text()="Contact us" or text()= "Help" or text()="Feedback")]')))
            except:
                print(f"{retailer}" + " error/Item not found")
                continue
                
            # Extract the product name from the product name element
            name_html = item_name_element.get_attribute('outerHTML')
            soup = BeautifulSoup(name_html, 'html.parser')
            name = soup.get_text(strip=True)
            item_names[retailer] = name
            
            price_html = price_element.get_attribute('innerHTML')
            soup = BeautifulSoup(price_html, 'html.parser')
            price = soup.get_text(strip=True)
            product_prices[retailer] = price
            if clubcard_price:
                product_prices[retailer] = f"Regular Price: {price}, Clubcard Price: {clubcard_price}, (Occasionally, the program may fetch an incorrect clubcard price)"
            
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
            item_names[retailer] = name

            # Extract the price from the price element
            price_html = price_element.get_attribute('innerHTML')
            soup = BeautifulSoup(price_html, 'html.parser')
            price = soup.get_text(strip=True).replace('now', '')
            product_prices[retailer] = price
            
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
            item_names[retailer] = name

            # Extract the price from the price element
            price_html = price_element.get_attribute('innerHTML')
            soup = BeautifulSoup(price_html, 'html.parser')
            price = soup.get_text(strip=True).replace('now', '')
            product_prices[retailer] = price      
            
        elif retailer == "Sainsburys":
            try:
                  # Check if the Nectar price exists on the page
                nectar_price_element = driver.find_element(By.CLASS_NAME, 'pt__cost--price')
                nectar_price = nectar_price_element.get_attribute('innerHTML').strip()
                # Find the price element on the Sainsburys website
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
            item_names[retailer] = name
            price_html = price_element.get_attribute('innerHTML')
            soup = BeautifulSoup(price_html, 'html.parser')
            price = soup.get_text(strip=True).replace('now', '')
            product_prices[retailer] = price  
            if nectar_price:
                product_prices[retailer] = f"Regular Price: {price}, Nectar Price: {nectar_price}, (Occasionally, the program may fetch an incorrect nectar offer or Price Lock)"    
    
    driver.quit()

    return product_prices, item_names

product_name = input("Enter the product name: ")
webWaitTime = input("Enter your estimated website loading time based on your connection speed: ")
results = scrape_product_prices(product_name)
prices = results[0]
items = results[1]

# Display the scraped prices and item names
for retailer, price in prices.items():
    item_name = items.get(retailer, "N/A")  # Retrieve item name from the dictionary, defaulting to "N/A" if not found
    print(f'{retailer}: {item_name} - {price} ')