import requests
from bs4 import BeautifulSoup
import time


html = requests.get('https://www.kuaidaili.com/free/inha/2/')
soup = BeautifulSoup(html.text, 'lxml').find_all('td')
print(soup)