import requests

#the required first parameter of the 'get' method is the 'url':
x = requests.get('https://www.olx.co.id/mobil-bekas_c198')
print(x.text)