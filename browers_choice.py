from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def initialize_driver(browser_choice):
    if browser_choice == 1:
        # Firefox
        options = webdriver.FirefoxOptions()
        options.headless = True
        print("Starting Firefox")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_choice == 2:
        # Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_choice == 3:
        # Microsoft Edge
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_argument ("headless")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        print ("Starting Edge\nCurrently undergoing improvements, including resolving errors and enhancing compatibility with certain websites.")
    return driver
