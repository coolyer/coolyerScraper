from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver(browser_choice):
    if browser_choice == 1:
        # Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('-host=127.0.0.1')
        options.headless = True
        # Start the Firefox browser with the provided options
        print("Starting Firefox")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_choice == 2:
        # Chrome
        options = webdriver.ChromeOptions()    
        options.add_argument('--headless=new') # Run the browser in headless mode (without opening a visible browser window)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    else:
        print("Invalid browser choice. Exiting...")
        exit(1) # Exit the program if the user enters an invalid choice   
    return driver