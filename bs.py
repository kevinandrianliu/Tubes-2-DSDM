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
    bs = BeautifulSoup(page_source, 'html.parser')

    list_params = []
    array_params = bs.find_all("span", class_="_25oXN")
    for param in array_params:
        list_params.append(param.text)

    list_items = []
    array_items = bs.find_all("span", class_="_2vNpt")
    for item in array_items:
        list_items.append(item.text)

    list_added_features = []
    array_added_features = bs.find_all("span", class_="_30Ijq")
    if len(list_added_features) != 0:
        for feature in array_added_features:
            list_added_features.append(feature.text)

    price = bs.find("span", class_="_2xKfz").text
    year_buy = bs.find("span", class_="_18gRm").text
    item_location = bs.find("span", class_="_2FRXm").text
    car_sold = bs.find("div", class_="_2DGqt").find("span").text
    seller_name = bs.find("div", class_="_3oOe9").text
    seller_join = bs.find("div", class_="rui-3P6Ei rui-1-t_r rui-urkah rui-3Rldd").find("span").find("span").text

    dict_items = dict(zip(list_params, list_items))
    dict_items['Fitur_Tambahan'] = list_added_features
    dict_items['Tahun_Beli_Mobil'] = year_buy
    dict_items['Lokasi'] = item_location
    dict_items['Waktu_Penjualan'] = car_sold
    dict_items['Nama_Penjual'] = seller_name
    dict_items['Waktu_Penjual_Bergabung_ke_OLX'] = seller_join
    dict_items['Dihighlight'] = highlight
    dict_items['Harga'] = price

    cars.append(dict_items)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get('https://www.olx.co.id/mobil-bekas_c198')
more_buttons = driver.find_element_by_xpath('//button[contains(@class, "rui-3sH3b") and contains(@class, "rui-23TLR") and contains(@class, "rui-1zK8h")]')

highlighted_cars = len(driver.find_elements_by_class_name("fhlkh"))
nonhighlighted_cars = len(driver.find_elements_by_class_name("EIR5N"))
print(str(highlighted_cars+nonhighlighted_cars))
while more_buttons.is_displayed():
    driver.execute_script("arguments[0].click();", more_buttons)
    time.sleep(1)
    more_buttons = driver.find_element_by_xpath('//button[contains(@class, "rui-3sH3b") and contains(@class, "rui-23TLR") and contains(@class, "rui-1zK8h")]')
    highlighted_cars = len(driver.find_elements_by_class_name("fhlkh"))
    nonhighlighted_cars = len(driver.find_elements_by_class_name("EIR5N"))
    print(str(highlighted_cars+nonhighlighted_cars))
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')
cars = []

highlighted_cars = soup.find_all(class_="fhlkh")
nonhighlighted_cars = soup.find_all(class_="EIR5N")

for link in highlighted_cars:
    crawl(cars, link, page_source, True)

print(len(cars))

for link in nonhighlighted_cars:
    crawl(cars, link, page_source, True)

print(len(cars))

with open("car.json", "w") as file:
    json.dump(cars, file)