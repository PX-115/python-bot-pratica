# -*- encoding: utf-8 -*-

# importando as libs necessárias para o projeto

from lib2to3.pgen2 import driver
import time
# import requests
import pandas as pd  # lib para tratamento de dados
from bs4 import BeautifulSoup
# selenium é a ferramenta que irá "navegar" automaticamente no browser
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from lib2to3.pgen2 import driver
import json

url = "https://www.nba.com/stats/players/traditional/?sort=TEAM_ABBREVIATION&dir=-1"

option = Options()
# Essa opção faz com que o browser rode em background / False faz com que o processo seja visível
# Permanece em False pois a confirmação de cookies impede o processo de ocorrer em background
option.headless = False
driver = webdriver.Edge(options=option)
driver.get(url)
time.sleep(10)

driver.find_element_by_xpath(
    "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[9]").click()

element = driver.find_element_by_xpath(
    "//div[@class='nba-stat-table']//table")

html_content = element.get_attribute("outerHTML")
# Faz a análise do conteúdo html e transforma em dados estruturados
soup = BeautifulSoup(html_content, "html.parser")
table = soup.find(name="table")

# lib do Panda, converte o que recebe em dado puro, eliminando os conteúdos do html (ex; tags)
# df stands for Data Frame
df_full = pd.read_html(str(table))[0].head(10)
df = df_full[["Unnamed: 0", "PLAYER", "TEAM", "PTS"]]
# Nome das colunas que serão exibidas no arquivo que o bot gera
df.columns = ["pos", "player", "team", "total"]

top10ranking = {}
top10ranking["points"] = df.to_dict("records")
driver.quit

# Converte e salva em um arquivo JSON
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)
