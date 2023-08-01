# Coolyer Scraper(Product Price Scraper)
Coolyer Scraper is a Python script that allows you to scrape product prices from various retailers. It uses Selenium and BeautifulSoup to extract product information from popular grocery retailers' websites.

## Prerequisites

- Python 3.x
- Firefox or Chrome browser (depending on your choice)
- GeckoDriver for Firefox or ChromeDriver for Chrome (automatically installed via `webdriver_manager`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/coolyer/coolyerScraper
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Python script:

   ```bash
   python main.py
   ```

2. You will be prompted to choose a browser (1 for Firefox or 2 for Chrome).

3. Enter your estimated website loading time based on your connection speed.

4. Provide the product name you want to search for.

5. The script will display the scraped prices and item names from various retailers in a markdown table.

6. After displaying the results, you will be asked if you want to search for another product. Enter 'yes' to continue searching or 'no' to exit the program.

## Supported Retailers

The script supports the following retailers:

- Tesco
- Asda
- B&M
- Sainsburys

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

Please note that web scraping might be against the terms of service of some websites. Use this script responsibly and make sure to review the terms of service of the websites you are scraping data from.

## Acknowledgments

The script uses Selenium for browser automation and BeautifulSoup for web scraping. Special thanks to the developers of these excellent libraries.

## Product Scraper - Features to Add

This project aims to be a versatile and efficient product scraper, capable of retrieving prices and product names from various online retailers. While the current version provides a solid foundation, there are several exciting features planned for future updates:

* Expanded Browser Support: In upcoming versions, we plan to add support for more web browsers, including Brave, Opera, and Bing. This will give users greater flexibility in choosing their preferred browser for the scraping process.

* Code Optimization: My commitment to excellence means continually refining and optimizing the codebase. Future updates will focus on enhancing performance and streamlining the scraping process for improved efficiency.

 * Increased Retailer Coverage: I understand the importance of having access to a wide range of retailers. As such, I aim to expand the list of supported websites, adding more options for users to scrape prices and product names from your favorite online stores.

 * Customized Website Selection: To provide users with even more control, a feature to select specific websites for scraping will be implemented. This option allows users to target their preferred retailers, ensuring a more personalized and relevant scraping experience.

**I am dedicated to maintaining and enhancing this product scraper to meet the evolving needs of our users. Your feedback and suggestions are valuable to me, so feel free to share your ideas for additional features or improvements. Together, we can make this tool even more powerful and user-friendly. Thank you for using our product scraper!**

## The Team
**|Main Programer: Josh|**

# Bugs 
* Sometimes error with Sainsburys not showing products prices or not scalping correctly. (Set to 3 seconds when asked in the code)
