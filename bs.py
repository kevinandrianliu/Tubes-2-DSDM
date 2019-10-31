import requests
import csv
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

def crawl(cars, link, headers):
    print(str(len(cars) + 1) + ". Link = " + str(link))
    if "fhlkh" not in str(link):
        highlight = True
    else:
        highlight = False
    url_car = 'https://www.olx.co.id' + link.a.get('href')
    
    if not cars or url_car not in cars[0].values():
        req = requests.get(url_car, headers)
        print(req.history)
        if not req.history: # Filter expired cars, because no detail can be found
            bs = BeautifulSoup(req.content, 'html.parser')

            # Remove Tags
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
            # Some cars don't have added features
            if len(array_added_features) != 0:
                for feature in array_added_features:
                    list_added_features.append(feature.text)

            # Get other features
            price = bs.find("span", class_="_2xKfz").text
            year_buy = bs.find("span", class_="_18gRm").text
            item_location = bs.find("span", class_="_2FRXm").text
            car_sold = bs.find("div", class_="_2DGqt").find("span").text
            seller_name = bs.find("div", class_="_3oOe9").text
            seller_join = bs.find("div", class_="rui-3P6Ei rui-1-t_r rui-urkah rui-3Rldd").find("span").find("span").text

            # Prepare list of dictionary

            dict_items = dict(zip(list_params, list_items))
            dict_items['Fitur_Tambahan'] = list_added_features
            dict_items['Tahun_Beli_Mobil'] = year_buy
            dict_items['Lokasi'] = item_location
            dict_items['Waktu_Penjualan'] = car_sold
            dict_items['Nama_Penjual'] = seller_name
            dict_items['Waktu_Penjual_Bergabung_ke_OLX'] = seller_join
            dict_items['Dihighlight'] = highlight
            dict_items['Link'] = url_car
            dict_items['Harga'] = price
        
            cars.append(dict_items)

cars = []
counter = 0
while len(cars) < 50000:
    # Add header to smooth crawling using Mozilla
    if counter == 0:
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

        # Add options to Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        driver.get('https://www.olx.co.id/mobil-bekas_c198')
        
    more_buttons = driver.find_element_by_xpath('//button[contains(@class, "rui-3sH3b") and contains(@class, "rui-23TLR") and contains(@class, "rui-1zK8h")]')

    olx_cars = len(driver.find_elements_by_class_name("EIR5N"))
    total_cars = []
    #print(str(olx_cars))

    # Clicking button "Muat Lainnya" until finish
    while more_buttons.is_displayed():
        driver.execute_script("arguments[0].click();", more_buttons)
        time.sleep(1) # No race condition
        # Make sure the button is clicked continously
        olx_cars = len(driver.find_elements_by_class_name("EIR5N"))
        total_cars.append(olx_cars)
        button_clicked = len(total_cars)
        print(str(olx_cars))
        #print(*total_cars)
        if (olx_cars == 1000 or total_cars[button_clicked-1] - total_cars[button_clicked-2] < 20) and len(total_cars) != 1: #Maximum 1000 cars in 1 page & ensuring that if the button cannot be clicked the loop will terminate
            break
        more_buttons = driver.find_element_by_xpath('//button[contains(@class, "rui-3sH3b") and contains(@class, "rui-23TLR") and contains(@class, "rui-1zK8h")]')

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    link_cars = soup.find_all(class_="EIR5N")

    for link in link_cars:
        crawl(cars, link, headers)

    print(len(cars))
    driver.refresh()
    counter += 1

with open("car.json", "w") as file:
    json.dump(cars, file)