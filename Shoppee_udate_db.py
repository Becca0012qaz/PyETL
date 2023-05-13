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


User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
my_headers = {
    'user-agent': User_Agent,
    'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhEYD7joAAAjHAcEAAAAAAAAAAOYyhFB7rjob26/8rq6jA0F3J6Kfg5aGEX+GYncix7fIyPghAefe3JS894jq/3nC9cJjpEn32HTqasIUhFkInWzoCOj1uSC5kl6LU06aSrm61kX/Ny1L5jzxFjDrS1IzPHwt9muZUbatRPTf42k24UXHBZsir4fwWxQLVKw5gDu5CyybpSVWFCd7OLsY30Hj1OjSKZvDNTpkAhYqvdOyLCTGr41kHyFGV3ZaoQ01NX1u6R9AnBG6X9s1ynZK6vnTBgzBIOKTNFS4j1VT8sOl1BEtObri8ZUW3OTOHeCO4vGDCq4gRJFmvwSm1BNdccjxAekgEx3xwroP6ZL6LO5bh9QSxuKGYkUmR84CcHLB6dmMPnXDUGkagca9MFiK8RmRsrN2vcLDNTpkAhYqvdOyLCTGr41kKUmjTinalW5/ctjHa7Lte+06J5ekdC078Iv4wrMjrvbzUjYNqi2Hdu8tLPGrNL/jmEfixe8rpESf8+9J+WOK8kusILDBjMDq/xa+8hI9GWbdxIdVmB5payUD+EtCC4BUkWOzjLDykZY2dhCO2aemlpFjs4yw8pGWNnYQjtmnppZDbeO6witi5K5LrYrVnhWzWCX7lKDZYje5tgIJeETgYw==',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-API-SOURCE': 'pc',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': 'IDq3287GJnXS5JJj5c2p5NfuvByGNpst',
    'sz-token': 'Ra/NJSFhMbpYXlWXB/kMKw==|tbtAeRuQraLaHXP0PPLER62V4RREUxTHlM0sHpOnYMwbMMQeM9+qLgkomlUGpUVkjby5btMmGHCl9DFdTYOavUNJ3LuXv0sobg==|oZGZsgOMDe5oaMrE|06|3',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Cookie': 'REC_T_ID=99d3d94f-5df0-11ed-b735-2cea7fa8daa9; SPC_F=w4AfWBkq1JrakV2jppFicIhTClRLblU7; SPC_R_T_ID=UXubTQvc/YPsM6xl+teVYis0dA2qLMfX6XkESPWMhmcIFaEi8LrMjdy7JotmJURfc8VtNc6ecvjQ5h0QxzshCQkSOwSRbEYbPzopwt27ggZispI0Ud4iKQQFka+NykFRJH0vM8M04lQUpSa5SxdHmdirR2k7laqgj3MTGLHCqTQ=; SPC_R_T_IV=R0Y1N1IwUUFYa1VqTjJRTw==; SPC_SI=m5xjYwAAAABKQ2FmemF6RlFAiQAAAAAARjNNa3hrdEw=; SPC_T_ID=UXubTQvc/YPsM6xl+teVYis0dA2qLMfX6XkESPWMhmcIFaEi8LrMjdy7JotmJURfc8VtNc6ecvjQ5h0QxzshCQkSOwSRbEYbPzopwt27ggZispI0Ud4iKQQFka+NykFRJH0vM8M04lQUpSa5SxdHmdirR2k7laqgj3MTGLHCqTQ=; SPC_T_IV=R0Y1N1IwUUFYa1VqTjJRTw==',
    'if-none-match-': '55b03-87240b139c68bb9237a3de8ffd8e8795'
}

page=[]
href=[]
keyword = ['競品名稱']
date = datetime.now().date()


#建立 Chrome WebDriver 服務
service = ChromeService(executable_path=ChromeDriverManager().install())
# service = ChromeService(executable_path='./chromedriver.exe')

#設定Chrome選項-啟動headless模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')

#建立Chrome Webdriver
driver = webdriver.Chrome(service=service, chrome_options=options)
time.sleep(random.randint(10, 20))

# 登入蝦皮頁面
username = username
password = password
driver.get('https://shopee.tw/buyer/login?next=https%3A%2F%2Fshopee.tw%2F')
time.sleep(random.randint(10,15))
driver.find_element(By.CSS_SELECTOR, 'input[name="loginKey"]').send_keys(username)
time.sleep(random.randint(5,8))
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(random.randint(5,8))
driver.find_elements(By.CSS_SELECTOR, 'button')[2].click()
time.sleep(random.randint(25,30))


#商品數、粉絲數、評價數量
product_count=[]
fans_count =[]
rating_count =[]

#搜尋目標賣場
for i in range(len(keyword)):
    driver.get('https://shopee.tw/search?keyword='+keyword[i])
    time.sleep(random.randint(25, 35))

    #取得href
    hreff = driver.find_element(By.CLASS_NAME, 'shopee-search-user-item__username')
    href.append(hreff.text)
    time.sleep(random.randint(25, 35))
    
    #點進目標賣場
    driver.find_element(By.CSS_SELECTOR, '#main > div > div.dYFPlI > div > div > div.sdzgsX > div.shopee-search-user-brief > div > div.shopee-header-section__content > div > a.shopee-search-user-item__shop-info > div.shopee-search-user-item__nickname').click()
    time.sleep(random.randint(25, 35))

    #取得page總頁數
    pagee=driver.find_element(By.CLASS_NAME, 'shopee-mini-page-controller__total').text
    page.append(int(pagee))
    
    # 取得粉絲數
    g_fans_count = driver.find_element(by=By.CSS_SELECTOR, value="#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(2) > div.section-seller-overview__item-text > div.section-seller-overview__item-text-value").text
    if "萬" in g_fans_count:
        g_fans_count=int(float(g_fans_count.replace('萬',""))*10000)
        fans_count.append(g_fans_count)
    else:
        fans_count.append(int(g_fans_count))

    # 取得商品數
    g_product_count = driver.find_element(by=By.CSS_SELECTOR, value="#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(1) > div.section-seller-overview__item-text > div.section-seller-overview__item-text-value").text
    product_count.append(g_product_count)

    # 取得評價(數量)
    g_rating_count = driver.find_element(by=By.CSS_SELECTOR, value="#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(4) > div.section-seller-overview__item-text > div.section-seller-overview__item-text-value").text.replace('(', '').replace(')', '').split(' ')[1]
    if "萬" in g_rating_count:
        g_rating_count=int(float(g_rating_count.split('個評價')[0].replace('萬',""))*10000)
        rating_count.append(g_rating_count)
    else:
        rating_count.append(int(g_rating_count.split('個評價')[0]))

    # 迭代列表並存入資料庫
    for i in range(len(product_count)):
        values = (product_count[i], rating[i], rating_Count[i])
        SQLcommand().modify('INSERT INTO offical_data (product_count, rating, rating_count) VALUES (%s, %s, %s)',values)

print(f'已於{date}完成競品賣場的資料更新！','競品總數量' + str(len(keyword)))


# 商品已售出
for i in range(len(keyword)):
    itemid = []
    shopid =[]
    name = []
    price = []
    historical_sold = []
    link=[]
    shop_name=[]
    date=[]
    for k in range(int(page[i])):
        driver.get(f'https://shopee.tw/{href[i]}?page={str(k)}sortBy=pop') 
        time.sleep(random.randint(25,30))

        for scroll in range(20):
            driver.execute_script('window.scrollBy(0,1000)')
            time.sleep(random.randint(15, 25))
            
        for item, thename in zip (driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="link"]'),
                                  driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="name"]')):
                # Link/ItemID/shopID
                getID = item.get_attribute('href')
                theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
                theshopid = int(getID[ getID[:getID.rfind('.')].rfind('.')+1 :getID.rfind('.')]) 
                link.append(getID)
                itemid.append(theitemid)
                shopid.append(theshopid)
                shop_name.append(keyword[i])
                date.append(date)
                
                # 商品名稱
                getname = thename.text.split('\n')[0]
                name.append(getname)
                time.sleep(random.randint(10, 15))

                thecontent = item.text
                thecontent = thecontent[(thecontent.find(getname)) + len(getname):]
                thecut = thecontent.split('\n')
                   
                # 商品價格
                if len(thecut) >= 3:
                    if bool(re.search('市|區|縣|鄉|海外|中國大陸', thecontent)): #有時會沒有商品地點資料
                        if bool(re.search('已售出', thecontent)): #有時會沒銷售資料
                            if '出售' in thecut[-3][1:]:
                                theprice = thecut[-4][1:]
                            else:
                                theprice = thecut[-3][1:]
                        else:
                            theprice = thecut[-2][1:]
                    else:
                        if bool(re.search('已售出', thecontent)):
                            theprice = thecut[-2][1:]
                        else:
                            theprice = thecut[-1][1:]               
                elif re.search('已售出', thecontent):   #有時會沒銷售資料
                    if len(thecut) == 1:
                        theprice = thecut[0]
                    else:
                        theprice = thecut[-2][1:]
                elif len(thecut)==2:
                        theprice = thecut[-1]
                else:                               # 處理 thecut 列表不足 3 個元素的情況（例如將 theprice 設置為空字符串）
                    theprice = ''

                theprice = theprice.replace('$','')
                theprice = theprice.replace('已','')
                theprice = theprice.replace(',','')
                theprice = theprice.replace('售','')
                theprice = theprice.replace('出','')
                theprice = theprice.replace(' ','')
                if '萬' in theprice:
                    theprice=int(float(theprice.replace('萬',""))*10000)
                if ' - ' in theprice:
                    theprice = (int(theprice.split(' - ')[0]) +int(theprice.split(' - ')[1]))/2
                if '-' in theprice:
                    theprice = (int(theprice.split('-')[0]) +int(theprice.split('-')[1]))/2
                if theprice != '':
                    price.append(int(theprice))
                else:
                    price.append(0)
                    print(0)
        # 取得已售出
        get_historical_sold = driver.find_elements(By.CSS_SELECTOR, '.shop-search-result-view [class="rOgDNT lNPX0P"]')
        for element in get_historical_sold:
            content_historical_sold = element.text
            print(content_historical_sold)
            if content_historical_sold == "":
                historical_sold.append(0)
                print(0)
            else:
                historical_sold = historical_sold.replace("已售出", "").replace(",","")
                historical_sold_value = int(content_historical_sold)
                historical_sold.append(historical_sold_value)

    values = zip(date, itemid, name, shopid, shop_name, price, historical_sold)
    SQLcommand().modify('INSERT INTO products_info (date, product_id, product_name, shop_id, shop_name, price, historical_sales) VALUES (%s, %s, %s, %s, %s, %s, %s)',values)
              
print(f'已於{date}完成歷史銷售資料更新！','總銷售商品數' + str(len(itemid)))


#取得商品月銷量資訊
for i in range(len(keyword)):
    itemid = []
    mounthly_sales = []
    for k in range(int(page[i])):
        driver.get(f'https://shopee.tw/{href[i]}?page={str(k)}&sortBy=sales' )
        time.sleep(random.randint(20,30))

        # 滾動頁面
        for scroll in range(10):
            driver.execute_script('window.scrollBy(0,1000)')
            time.sleep(random.randint(20,30))
        #取得商品內容
        for item, thename in zip (driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="link"]'),
                                  driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="name"]')):
            getID = item.get_attribute('href')
            
            theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
            itemid.append(theitemid)

    # 取得月銷量
        get_mounthly_sales = driver.find_elements(By.CSS_SELECTOR, ".shop-search-result-view div.BUP03F.hynaVT")
        for element in get_mounthly_sales:
            content_monthly = element.text
            if content_monthly == "":
                mounthly_sales.append(0)
            else:
                content_monthly = content_monthly.replace("月銷量", "").replace(",","")
                mounthly_sales_value = int(content_monthly)
                mounthly_sales.append(mounthly_sales_value)

    for item, sales in zip(itemid, monthly_sales):
            values = (sales, item)

    SQLcommand().modify("UPDATE products_info SET monthly_sales = %s WHERE itemid = %s",values)           
    print(f'已於{date}完成月銷售資料更新！','總銷售商品數' + str(len(itemid)))      

driver.close() 

if __name__ == '__main__':
  username = os.environ.get('shoppee_username')
  password = os.environ.get('shoppee_password')


