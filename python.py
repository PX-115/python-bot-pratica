# -*- encoding: utf-8 -*-

# importando as libs necessárias para o projeto

import json
import time
from lib2to3.pgen2 import driver

import requests
import pandas as pd  # lib para tratamento de dados
from bs4 import BeautifulSoup
# selenium é a ferramenta que irá "navegar" automaticamente no browser
from selenium import webdriver
from selenium.webdriver.edge.options import Options

url = "https://www.nba.com/stats/players/traditional/?PerMode=Totals&sort=PLAYER_NAME&dir=-1"
top10ranking = {}

rankings = {
    "3points": {"field": "FG3M", "label": "3PM"},
    "points": {"field": "PTS", "label": "PTS"},
    "assistants": {"field": "AST", "label": "AST"},
    "rebounds": {"field": "REB", "label": "REB"},
    "steals": {"field": "STL", "label": "STL"},
    "blocks": {"field": "BLK", "label": "BLK"},
}


def buildrank(type):

    field = rankings[type]["field"]
    label = rankings[type]["label"]

    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element_by_xpath(
        "//div[@class='nba-stat-table']//table")

    html_content = element.get_attribute("outerHTML")
    # Faz a análise do conteúdo html e transforma em dados estruturados
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find(name="table")

    # lib do Panda, converte o que recebe em dado puro, eliminando os conteúdos do html (ex; tags)
    # df stands for Data Frame
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[["Unnamed: 0", "PLAYER", "TEAM", label]]
    # Nome das colunas que serão exibidas no arquivo que o bot gera
    df.columns = ["pos", "player", "team", "total"]
    # Transforma os Dados em um Dicionário de dados próprio
    return df.to_dict("records")


option = Options()
# Essa opção faz com que o browser rode em background / False faz com que o processo seja visível
# Permanece em False pois a confirmação de cookies impede o processo de ocorrer em background
option.headless = False
driver = webdriver.Edge(options=option)
driver.get(url)
time.sleep(10)
# driver.implicitly_wait(10) / Melhor maneira de aguardar o conteúdo carregar

# Lista todos os ranks que serão gerados e armazena em top10rankings[k], onde ele é enviado para o aqruivo JSON
for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit

# Converte e salva em um arquivo JSON já formatado
with open("ranking.json", "w", encoding="utf-8") as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)
