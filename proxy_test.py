from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import chromedriver_autoinstaller
from time import sleep

PROXY = "91.224.62.194:8080" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
service = Service(chromedriver_autoinstaller.install())

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.avito.ru/')
sleep(60)