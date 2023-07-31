
# Coolyer Scraper (Product Price Scraper)

## Product Price Scraper

This Python script is designed to scrape product prices from various online retailers, It utilizes Selenium WebDriver and BeautifulSoup to extract prices and item names, providing users with up-to-date product pricing information from different websites.


## Installation and Setup

1. Clone this repository to your local machine.
2. Install the required Python packages using pip:

3. Ensure you have either ChromeDriver or GeckoDriver installed and added to your system PATH. You can use the following links for installation instructions:
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

## Usage

1. Run the `main.py` 
2. Will ask for Product you want to scrape for
3. webWaitTime How long to wait for webpage to load depending on your internet 

## Handling Inaccurate Prices

Please note that the program may occasionally fetch incorrect prices due to variations in website layouts or updates. To mitigate this, the script has implemented additional checks when scraping Clubcard prices from Tesco and Nectar prices from Sainsburys. If the Clubcard or Nectar price is found, the script will indicate that the prices might not be accurate in those cases.

## Working websites
* Tescos
* Asda
* B&M   
* Sainsburys
Will be adding more soon!

## Acknowledgments

- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

## To be added
* Browser choice, Chrome or Firefox.
* More accurate Nectar and Clubcard price for your product
