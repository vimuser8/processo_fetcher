from selenium import webdriver
import json
import requests
import sys, os

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

user_agent = driver.execute_script("return navigator.userAgent")
driver.quit()

base_url =  "https://www3.cfc.org.br/spwALTeste/pro-teste/Processo/ListarProcessoConsulta"
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/144.0.0.0 Safari/537.36"
#print(user_agent)
headers = {
        "User-Agent": user_agent,
}
        #"X-Requested-With": "XMLHttpRequest",
        #"Accept": "application/json, text/javascript, */*; q=0.01",
        #"Content-Type": "application/json"
        #}
all_records = []
page_num = 1
PAGE_SIZE = 20

while True:

    inner_filter = {
        "NumeroProcesso": "",
        "DataInicioAbertura": None,            # null vira None
        "DataFimAbertura": None,
        "DataInicioArquivamento": "",          
        "DataFimArquivamento": "",
        "qtdPorPagina": 50,
        "numeroDaPagina": page_num,
        "filtroInstantaneo": ""
}

    oFiltro_string = json.dumps(inner_filter)
    params = {'page': page_num, 'limit': PAGE_SIZE, 'oFiltro': oFiltro_string}
    try:
        response = requests.get(base_url, headers=headers, params=params)
        status_code = response.status_code

        if status_code!=200:
            print(f"[ERROR] Status {status_code}")
            break

        print(response.text)
        #data = response.json()
        #current_batch = data.get("items", [])
        #print(type(current_batch))

    except Exception as e:
        print(e)

    break
