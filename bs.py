import requests
import csv
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

def crawl(cars, link, page_source, highlight):
    if highlight:
        url_car = 'https://www.olx.co.id' + link.get('href')
    else:
        url_car = 'https://www.olx.co.id' + link.a.get('href')
    req = requests.get(url_car, headers)
    bs = BeautifulSoup(req.content, 'html.parser')
    bs = BeautifulSoup(page_source, 'html.parser')

    list_params = bs.find_all("span", class_="_25oXN")
    list_items = bs.find_all("span", class_="_2vNpt")
    list_added_features = bs.find_all("span", class_="_30Ijq")
    price = bs.find("span", class_="_2xKfz").text
    year_buy = bs.find("span", class_="_18gRm").text
    item_location = bs.find("div", class_="_1uzVV").text
    car_sold = bs.find("div", class_="_2DGqt").text
    seller_name = bs.find("div", class_="_3oOe9").text

    dict_items = dict(zip(list_params, list_items))
    if len(list_added_features) != 0:
        dict_items['Fitur_Tambahan'] = list_added_features
    
    dict_items['Tahun_Beli_Mobil'] = year_buy
    dict_items['Lokasi'] = item_location
    dict_items['Waktu_Penjualan'] = car_sold
    dict_items['Nama_Penjual'] = seller_name
    dict_items['Dihighlight'] = highlight
    dict_items['Harga'] = price

    cars.append(dict_items)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get('https://www.olx.co.id/mobil-bekas_c198')
more_buttons = driver.find_elements_by_class_name("JbJAl")
while more_buttons[0].is_displayed():
    driver.execute_script("arguments[0].click();", more_buttons[0])
    time.sleep(1)
    more_buttons = driver.find_elements_by_class_name("JbJAl")
page_source = driver.page_source

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
#Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:11.0) Gecko/20100101 Firefox/11.0

#url = 'https://www.olx.co.id/mobil-bekas_c198'
#req = requests.get(url, headers)
#soup = BeautifulSoup(req.content, 'html.parser')
soup = BeautifulSoup(page_source, 'html.parser')
cars = []

highlighted_cars = soup.find_all(class_="fhlkh")
nonhighlighted_cars = soup.find_all(class_="EIR5N")

for link in highlighted_cars:
    crawl(cars, link, page_source, True)

print(len(cars))

for link in nonhighlighted_cars:
    crawl(cars, link, page_source, False)

print(len(cars))

with open("car.json", "w") as file:
    json.dump(cars, file)