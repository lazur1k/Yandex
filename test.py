from openpyxl import load_workbook
import pandas as pd
import os

from main import main


main_db = pd.read_excel('K:/Сектор мониторинга РН/Аналитика/1. СБОР ИНФОРМАЦИИ/Выгрузка - Яндекс/01.05.2022/Дома, дачи, котеджы/Дома, дачи, котеджы(2582).xlsx').iloc[:, 1:]
scans = main_db['id'].values.tolist()

row_for_delete = []
imgs = os.listdir('K:/Сектор мониторинга РН/Аналитика/1. СБОР ИНФОРМАЦИИ/Выгрузка - Яндекс/01.05.2022/Дома, дачи, котеджы/screenshots')
for scan in scans:
    # if f'{scan}.png' not in imgs:
    if scans.count(scan) >1 :
        print(scan)
#         row_for_delete.append(scan)
