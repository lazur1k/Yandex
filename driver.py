from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from subprocess import CREATE_NO_WINDOW
from bs4 import BeautifulSoup
from time import sleep

class Driver():
   
    def __init__(self):
        
        self._options = webdriver.ChromeOptions()
        self._options.add_argument("--headless")
        self._options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
        self._options.add_argument("--log-level=3")
        self._options.add_argument("--disable-blink-features=AutomationControlled")
        self._caps = DesiredCapabilities.CHROME
        self._caps["goog:loggingPrefs"] = {"performance": "ALL"}
        self._caps["pageLoadStrategy"] = "eager"
        self._service = Service(chromedriver_autoinstaller.install())
        self._service.creationflags = CREATE_NO_WINDOW
        self._driver = webdriver.Chrome(service= self._service, options = self._options, desired_capabilities = self._caps)

    def get_ads(self, url):
        self._driver.get(url)
        ads = self.__get_ads_on_page()
        return ads
    
    def generate_pages(self, url):
        self._driver.get(url)
        try:
            ads = self._driver.find_element(by=By.CLASS_NAME, value= 'FiltersFormField__counter-submit').text.split(' ')[1:-1]
            ads = int(''.join(ads))
            pages = ads//20 + 1
            return int(pages)
        except:
            return 'ERORR'
       
    def stop(self):
        self._driver.quit()
            
    def __get_ads_on_page(self):
        container = self._driver.find_element(by=By.CLASS_NAME, value='OffersSerp__list')
        ads = container.find_elements(by=By.CLASS_NAME, value= 'OffersSerp__list-item_type_offer')
        ads_on_page =[]
        for ad in ads:
            ad_html = BeautifulSoup(ad.get_attribute('innerHTML'), 'lxml')
            ad_element = ad.find_element(by=By.CSS_SELECTOR, value = 'a')
            ad_id = ad_html.find('a').get('href').split('/')[-2]
            ad_date = ad_html.find('div', {'class': 'OffersSerpItem__publish-date'}).text.replace('\xa0', ' ')
            ad_object = {'id': ad_id, 'element': ad_element, 'date': ad_date}
            ads_on_page.append(ad_object)
        return ads_on_page
      
if __name__ == "__main__":
    driver = Driver()
    dr = driver._driver
    driver._driver.get('https://realty.yandex.ru/offer/5636510418058913817/')
    html = BeautifulSoup(dr.page_source, 'lxml')
    print(html.find_all(class_ ='PriceHistory__item'))
    
    driver.stop()