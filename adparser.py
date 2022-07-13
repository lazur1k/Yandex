from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
import config
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import datetime
import os


class YandexParser(Driver):
    def __init__(self, ads_type, directory, date):
        super().__init__()
        
        self._need_date = date
        self._ads_type = ads_type
        self._directory = f'{directory}/{ads_type}'
        self._directory_screenshots = f'{directory}/{ads_type}/screenshots'
        self._directory_excel = f'{directory}/{ads_type}/excel'
        
        if self._ads_type not in os.listdir(directory):
            os.makedirs(self._directory)
            
        if 'screenshots' not in os.listdir(self._directory):
            os.makedirs(self._directory_screenshots)
        
        self._existing_ads = os.listdir(self._directory_screenshots)          

        if 'excel' not in os.listdir(self._directory):
            os.makedirs(self._directory_excel)         
 
    def urls_generator(self):
        options = config.types[self._ads_type]
        urls = []
        for url in options['urls']:
            if self._ads_type == 'Гаражи':
                urls.append(url)
            else:
                for i in options['sqr_range']:
                    urls.append(url.format(sqr = i))
        
        return urls
    
    def scrap_ad(self, ad):
        k=0
        try:
            self.__close_ad_page()
            ad_element = ad['element']
            ad_id = ad['id']
            ad_date = ad['date']
            if f'{ad_id}.png' in self._existing_ads:
                return f'Объявление {ad_id} уже собрано\n{40*"-"}'
            
            date_publication = self.__change_format_of_date(ad_date)    
            if self.__date_publication_check(date_publication) == False:
                self.__close_ad_page()
                return f'Объявление {ad_id} слишком старое\n{40*"-"}'
            
            else:
                try:
                    ad_element.click()
                    WebDriverWait(self._driver, 10).until(EC.number_of_windows_to_be(2))
                    self._driver.switch_to.window(self._driver.window_handles[1])
                    sleep(1)
                except:
                    self.__close_ad_page()
                    return f'Объявление {ad_id} не открывается \n{40*"-"}'
            html = BeautifulSoup(self._driver.page_source, 'lxml')
                
            data = {
                        '_id': f"{datetime.datetime.today().strftime('%y%m')}_{len(self._existing_ads)}",
                        'id': 'Запустите обработку результатов, чтобы отобразить id объявления',
                        'url': str(self._driver.current_url)
                    }        
            try:     
                data['Дата публикации'] = date_publication           
                try:
                    self.__expand_descriptions()
                except Exception as e:
                    print(e)
                
                html = BeautifulSoup(self._driver.page_source, 'lxml')
                try:                   
                    data['Заголовок'] = html.find('div', class_ = 'OfferCardSummaryInfo__description--1eQMI').text.replace('\xa0', ' ')
                except:
                    data['Заголовок'] = 'Ошибка'
                try:
                    data['Описание'] = html.find('p', class_='OfferCardTextDescription__text--3na1F').text.replace('\xa0', '').replace('\n', ' ')
                except:
                    data['Описание'] = 'Отсутствует описание'
                try:
                    data['Цена'] = html.find('span', class_ = 'OfferCardSummaryInfo__price--3WinQ OfferCardSummaryInfo__priceWithLeftMargin--dZLTe').text.replace('\xa0', '')[:-2]  
                except:
                    data['Цена'] = 'Ошибка'
                
                try:    
                    full_adress = html.find('div', class_ ='GeoLinks__addressContainer--2MSWu').text  
                    data['Адрес'] = full_adress 
                except:
                    data['Адрес'] = 'Ошибка'          
                # try:    
                #     data['Этаж/Этажность'] = data['Этаж']
                #     data['Этаж'] = data['Этаж/Этажность'].split('/')[0].strip()
                #     data['Этажность'] = data['Этаж/Этажность'].split('/')[1].strip()
                # except:
                
                params_of_flat =  html.find_all(class_ = 'OfferCardFeature__root--1uCzg')
                for param in params_of_flat:
                    try:
                        attribute = param.find('svg').get('class')[1].replace('IconSvg_', '').replace('-48', '').replace('-outline', '')
                        attribute_data = param.text.replace('\xa0', '')
                        if attribute != 'm2':
                            data[attribute] = attribute_data
                    except Exception as e:
                        print(param)
                        print(e)

                price_history_element = self._driver.find_element(by=By.CLASS_NAME, value = 'OfferCardSummaryInfo__price--3WinQ')
                ActionChains(self._driver).move_to_element(price_history_element).perform()
                sleep(0.1)
                html = BeautifulSoup(self._driver.page_source, 'lxml')
                prices = html.find_all(class_ ='PriceHistory__item')
                if prices:
                    price_history = {}
                    price_history['url'] = self._driver.current_url
                    for i in range(len(prices)):
                        try:
                            date = prices[i].find(class_ = 'PriceHistory__item-col_date').text.replace('\xa0', ' ')
                            date = self.__change_format_of_date(date)
                            price = prices[i].find(class_ = 'PriceHistory__item-col_price').text.replace('\xa0', ' ')
                            price_history[f'Дата изменения цены_{i}'] = date
                            price_history[f'Цена_{i}'] = price     
                        except Exception as e:
                            print(e)
                            print(prices)           
                    self.__price_history_excel(price_history)
                
            except Exception as e :
                print(e)
                sleep(20)
                return f'Страница объявления {ad_id} не прогрузилась\n{40*"-"}'
            
            self._existing_ads.append(f'{ad_id}.png')
            self.__take_screen()
            self.__close_ad_page()
            return data
            
        except Exception as e:
            print(e)
            return
    
    def save_to_excel(self, ad_info):
        try:
            pd.set_option('display.precision', 20)
            self.__DB_checking()
            excel_path = f'{self._directory_excel}/{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx'
            db = pd.read_excel(excel_path).iloc[:, 1:]
            new_ad = pd.DataFrame(ad_info, index= [0])
            new_db = pd.concat([db,new_ad], ignore_index= True)
            new_db.to_excel(excel_path)
        except Exception as e:
            print(e)
    
    def __price_history_excel(self, price_history):
        self.__DB_checking()
        try:
            price_path = f'{self._directory}/excel/priceHistory.xlsx'
            price_db = pd.read_excel(price_path).iloc[:, 1:]
            price_history = pd.DataFrame(price_history, index = [len(price_db)])
            new_price = pd.concat([price_db, price_history])
            new_price.to_excel(price_path)
        except Exception as e:
            print(e)
        
    def __take_screen(self):
        try:
            if f'screenshots' in os.listdir(self._directory):
                try:
                    S = lambda X: self._driver.execute_script('return document.body.parentNode.scroll'+X)
                    self._driver.set_window_size(S('Width'),S('Height'))
                    self._driver.find_element_by_tag_name('body').screenshot(f"{self._directory}/screenshots/{self._driver.current_url.split('/')[-2]}.png")
                except Exception as e:
                    print(e)
            else:
                os.makedirs(self._directory_screenshots)
                self._existing_ads = list(map(lambda x: x[:-4], os.listdir(f'{self._directory_screenshots}')))
                self.__take_screen()
        except Exception as e:
            print(e)
    
    def stop(self):
        self._driver.quit()             

    def __change_format_of_date(self, date):
        months = {
                'января': '01',
                'февраля': '02',
                'марта': '03',
                'апреля': '04',
                'мая': '05',
                'июня': '06',
                'июля': '07',
                'августа': '08',
                'сентября': '09',
                'октября': '10',
                'ноября': '11',
                'декабря': '12'
                }
        date = date.split(' ')
        if date[0].isdigit():
            if 'час' in date[1] or 'минут' in date[1] :
                return f'{datetime.datetime.today().strftime("%d.%m.%Y")}'
            else:
                return f"{date[0]}.{months[date[1].replace(',', '')]}.{datetime.datetime.today().year}"        
        
        elif 'вчера' in date[0]:
            today= datetime.datetime.today()
            yesterday = today - datetime.timedelta(days = 1)
            return  f'{yesterday.strftime("%d.%m.%Y")}'
        
        elif date[0] == 'сейчас':
            return f'{datetime.datetime.today().strftime("%d.%m.%Y")}'
    
    def __DB_checking(self):
        if not f'{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx' in os.listdir(self._directory_excel):
            df = pd.DataFrame()
            excel_name = f'{self._directory_excel}/{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx'
            df.to_excel(excel_name)
        if not 'priceHistory.xlsx' in  os.listdir(self._directory_excel):
            df = pd.DataFrame()
            excel_name = f'{self._directory_excel}/priceHistory.xlsx'
            df.to_excel(excel_name)
            
    def __date_publication_check(self, date):
        
        date = date.split(' ')[0].split('.') #[0: day, 1: month] all str
        if int(date[1]) > self._need_date[0]:
            return True
        elif int(date[1]) == self._need_date[0] and int(date[0]) >= self._need_date[1]:
            return True
        else: 
            return False
    
    def __expand_descriptions(self):
        S = lambda X: self._driver.execute_script('return document.body.parentNode.scroll'+X)
        self._driver.set_window_size(S('Width'),S('Height'))
        btns = self._driver.find_elements(by=By.CLASS_NAME, value= 'OfferCardExpandableData__root--3XbNs')
        for btn in btns:
            btn = btn.find_element(by=By.XPATH,  value= './/span')
            btn.click()
    
    def __close_ad_page(self):
        if len(self._driver.window_handles) > 1:
            self._driver.close()
            self._driver.switch_to.window(self._driver.window_handles[0])
    
if __name__ == "__main__":
    pass