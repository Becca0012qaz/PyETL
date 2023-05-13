# 簡介
用selenium的方式將蝦皮賣場的競品資料進行爬取,並存進MySQL資料庫中,未來將結合linux中cronjob來持續更新資料
為避免被蝦皮擋,故每次執行一個動作會停留較久時間

## 導入相關套件
```python
import requests
import json
import pandas as pd
import time
import re
import random
import zlib
from seleniumwire import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime

from connect_to_db import SQLcommand
```

## 建立Chrome Webdriver
```python
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, chrome_options=options)
time.sleep(random.randint(10, 20))
```

## 爬蟲完直接存入MySQL中
```python
#搜尋目標賣場
for i in range(len(keyword)):
    driver.get('https://shopee.tw/search?keyword='+keyword[i])
    time.sleep(random.randint(25, 35))
    ....
    ...
    # 迭代列表並存入資料庫
    for i in range(len(product_count)):
        values = (product_count[i], rating[i], rating_Count[i])
        SQLcommand().modify('INSERT INTO offical_data (product_count, rating, rating_count) VALUES (%s, %s, %s)',values)

print(f'已於{date}完成競品賣場的資料更新！','競品總數量' + str(len(keyword)))
```
## 結合Cronjob--TBC


