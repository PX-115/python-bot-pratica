# importando as libs necessárias para o projeto

from lib2to3.pgen2 import driver
import time
# import requests
import pandas as pd  # lib para tratamento de dados
# from bs4 import BeautifulSoup
# selenium é a ferramenta que irá "navegar" automaticamente no browser
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import json

url = "https://www.yugioh-card.com/en/limited/"

option = Options()

# Essa opção faz com que o browser rode em background / False faz com que o processo seja visível
# option.headless = True

# option.binary_location = "C:\\Users\\vitor\\AppData\\Local\\Programs\\Opera GX\\opera.exe" # Caminho pro executável
driver = webdriver.Edge()
driver.get(url)
driver.quit
