from datetime import datetime
import sys
import os
from time import sleep, time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread
from adparser import YandexParser
import design
from processing import processing


class Worker(QObject):
    def __init__(self, streamParsing, infoParser, parserType, previewDirectory, dateEdit):
        super().__init__()
        streamParsing.clear()
        self.streamParsing = streamParsing
        self.infoParser = infoParser
        self.parserType = parserType
        self.previewDirectory = previewDirectory
        self.dateEdit = dateEdit
        self._adParser = None
        self._page_remember = None

        
    def run(self):
        try:
            os.listdir(self.previewDirectory.currentItem().text())
        except:
            self.update_info_parsing('Выберите дирректорию для сохранения файлов')
            return
        self.change_info_title('Началась работа программы')
        self.__create_parser()
        self._count_ads = 1
        self._count_new_ads = 0
        self._urls = self._adParser.urls_generator()
        for url in self._urls:
            self._url = url
            page_nums = self._adParser.generate_pages(self._url)
            sleep(2)
            if page_nums != 'ERORR':
                for page_num in range(1, page_nums + 1):
                    self._page_num = page_num
                    try:
                        self.__parsing()                     
                    except Exception as e:
                        print(e)
                        self._count_ads += 1
                        sleep(10)
                        self.__create_parser()
                        next
            else:
                continue
        self.change_info_title('Парсинг закончен')
            

    def __create_parser(self):
        self.stop()
        self._adParser = YandexParser( self.parserType.currentText(), self.previewDirectory.currentItem().text(), self.dateEdit.date().getDate()[1:])
        self._stopFlag = False
    
    def __parsing(self):
        ads_on_main_page = self._adParser.get_ads(self._url + f'{self._page_num}')
        for ad in ads_on_main_page:
            if self._stopFlag == False:
                result = self._adParser.scrap_ad(ad)
                self.update_info_parsing(f'Получено {self._count_ads} объявление')
                if type(result) == str:
                    self._count_ads += 1
                    self.update_info_parsing(result)
                    continue
                else:
                    self._adParser.save_to_excel(result)
                    self.update_info_parsing(f'Объявление {result["url"].split("/")[-2]} сохранено\n{40*"-"}')
                    self._count_new_ads += 1 
                    self.change_info_title(f'Собрано: {self._count_new_ads} объявлений')
                    self._count_ads += 1
                
                sleep(2)
            else:
                sleep(2)
                return

    def change_info_title(self, text):
        self.infoParser.clear()
        text = QtWidgets.QListWidgetItem(text)
        self.infoParser.addItem(text)
        # QtWidgets.QApplication.processEvents()
        # sleep(0.1)

        
    def update_info_parsing(self, text):
        # text = QtWidgets.QListWidgetItem(text)
        self.streamParsing.append(text)
        sleep(0.01)
        self.streamParsing.verticalScrollBar().setValue(self.streamParsing.verticalScrollBar().maximum())            
    
    def stop(self):
        if self._adParser != None:
            self._stopFlag = True
            self._adParser.stop()
            self._adParser = None
            self.change_info_title('Парсинг остановлен')


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.chooseParser.addItems(['Квартиры','Коммерческая недвижимость','Земельные участки','Гаражи', 'Дома, дачи, коттеджи', 'Новостройки'])
        self.previewDirectory.addItem('Выберите папку для сохранения результатов')        
        self.qthread = QThread()
        self.qthread.setStackSize(1)
        self.worker = Worker(self.streamParsing, self.infoParser, self.chooseParser, self.previewDirectory, self.dateEdit)
        self.worker.moveToThread(self.qthread)
        
        self.btnDirectory.clicked.connect(self.browse_folder)
        self.btnStart.clicked.connect(self.click_start)
        self.btnStart.clicked.connect(self.worker.run)
        self.btnStop.clicked.connect(self.click_stop)
        self.processingResults.clicked.connect(self.process)
        
    def browse_folder(self):
        self.previewDirectory.clear()
        directory = QtWidgets.QListWidgetItem(QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку"))
        if directory:
            self.previewDirectory.addItem(directory)
            self.previewDirectory.setCurrentItem(directory)    
    
    def click_start(self):
        self.qthread.start()
        
    def click_stop(self): 
        if self.qthread.isRunning():
            self.qthread.terminate()
            self.worker.stop()
            self.streamParsing.clear()
    
    def process(self):
        if self.qthread.isRunning():
            self.infoParser.clear()
            text = QtWidgets.QListWidgetItem('Остановите парсинг')
            self.infoParser.addItem(text)
        else:   
            self.infoParser.clear()
            text = QtWidgets.QListWidgetItem('Обрабатываются собранные данные')
            self.infoParser.addItem(text)
            try:
                processing(self.chooseParser.currentText(), self.previewDirectory.currentItem().text()) 
                self.infoParser.clear()
                text = QtWidgets.QListWidgetItem('Данные готовы')
                self.infoParser.addItem(text)       
            except Exception as e:
                print(e)
                self.infoParser.clear()
                text = QtWidgets.QListWidgetItem('Проверьте правильноть выбранного пути')
                print('Что-то пошло не так. Проверьте правильноть выбранного пути')
                self.infoParser.addItem(text)
                                            
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec()
    
if __name__ == '__main__':
    main()