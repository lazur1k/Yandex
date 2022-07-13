types = {
    'Квартиры': {
        'urls': [

            'https://realty.yandex.ru/tyumen/kupit/kvartira/tryohkomnatnaya/?newFlat=NO&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/tryohkomnatnaya/?newFlat=NO&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/4-i-bolee/?newFlat=NO&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/4-i-bolee/?newFlat=NO&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/studiya/?newFlat=NO&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/studiya/?newFlat=NO&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/odnokomnatnaya/?newFlat=NO&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/odnokomnatnaya/?newFlat=NO&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/dvuhkomnatnaya/?newFlat=NO&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/dvuhkomnatnaya/?newFlat=NO&areaMin=200&page=' ,
        ],
        'sqr_range' : range(10,200, 5)
    },
    'Новостройки': {
        'urls': [

            'https://realty.yandex.ru/tyumen/kupit/kvartira/tryohkomnatnaya/?newFlat=YES&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/tryohkomnatnaya/?newFlat=YES&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/4-i-bolee/?newFlat=YES&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/4-i-bolee/?newFlat=YES&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/studiya/?newFlat=YES&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/studiya/?newFlat=YES&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/odnokomnatnaya/?newFlat=YES&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/odnokomnatnaya/?newFlat=YES&areaMin=200&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/dvuhkomnatnaya/?newFlat=YES&areaMin={sqr}&areaMax={sqr}&page=' ,
            'https://realty.yandex.ru/tyumen/kupit/kvartira/dvuhkomnatnaya/?newFlat=YES&areaMin=200&page=' ,
        ],
        'sqr_range' : range(10,200, 5)
    },
   
    'Дома, дачи, коттеджи': {
        'urls':[
            'https://realty.yandex.ru/tyumen/kupit/dom/?houseType=HOUSE&areaMin={sqr}&areaMax={sqr}&page=',
            'https://realty.yandex.ru/tyumen/kupit/dom/?lotAreaMin=100&houseType=HOUSE&areaMin=350',
            'https://realty.yandex.ru/tyumen/kupit/dom/?houseType=TOWNHOUSE&houseType=DUPLEX&houseType=PARTHOUSE&page=', 
         ],
        'sqr_range': range(1,350, 3)
    },
    
    'Земельные участки': {
        'urls': [
            'https://realty.yandex.ru/tyumen/kupit/uchastok/?lotAreaMin={sqr}&lotAreaMax={sqr}&page=',
            'https://realty.yandex.ru/tyumen/kupit/uchastok/?lotAreaMin=100&page=',
        ],
        'sqr_range': range(1, 100, 2)
    },
    
    'Гаражи': {
        'urls': [
            'https://realty.yandex.ru/tyumen/kupit/garazh/?garageType=BOX&garageType=GARAGE&page=',
            'https://realty.yandex.ru/tyumen/kupit/garazh/?garageType=PARKING_PLACE&page=',
        ]
    },
    'Коммерческая недвижимость': {
        'urls': [
            'https://realty.yandex.ru/tyumen/kupit/kommercheskaya-nedvizhimost/?areaMin={sqr}&areaMax={sqr}&page=',
            'https://realty.yandex.ru/tyumen/kupit/kommercheskaya-nedvizhimost/?areaMin=301',
        ],
        'sqr_range': range(1, 300, 3)
    }
}
