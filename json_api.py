from playwright.sync_api import sync_playwright
import getpass
import json
import pandas as pd
import numpy as np
import requests
import sys, os, time
"""
Copyright 2026 CRC/AL
Autor: Demerson Oliveira, estagiário
Criado em: Fevereiro, 2026
Modificado em: Fevereiro, 2026

Script direcionado para a aquisição de dados dos processos fiscalizatórios disponíveis do site cfc.org.br: requer acesso ao usuário do fiscal.

Notas:
Path: "www3.cfc.org.br/spwALTeste/pro-teste/Scripts/app/controllers/pro.detalhegerencial.controller.js?v=1502202601" (contains JSON data mapping)

vmc.ListaEtapas = [
    { Etapa: "Auto de Infração", codigo: 9 },
    { Etapa: "Ciência", codigo: 3 },
    { Etapa: "Ciência Julgamento", codigo: 12 },
    { Etapa: "Deliberação", codigo: 13 },
    { Etapa: "Decisão Federal", codigo: 14 },
    { Etapa: "Execução", codigo: 15 },
];

Entre outras coisas, a possibilidade de geração de relatórios permite que haja facilidade em comparar dados entre duas planilhas distintas com valores
potencialmente equivalentes e portanto de confronto de dados, o que não parece de todo prático a partir de uma página da web.
"""

USERNAME = input('Username: ')
PASSWORD = getpass.getpass('Password: ') 

def get_context_data(username, password, headless=True):
    """
    Obtém acesso aos cookies (entre outros dados) que garantem permissão de acesso aos dados JSON.
    """
    context_data = dict()

    # Abre uma página browser "invisível" que automatiza o login, assim como a extração dos cookies para uso posterior.
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context()
        page = context.new_page()

        response = page.goto("https://www3.cfc.org.br/spwALTeste/pro-teste/home/Login")
        page.wait_for_load_state("networkidle")

        # Automatização de Login
        page.locator("select[ng-model='vm.usuario.tipoUsuario']").select_option("1")
            
        input_login = page.locator('input[id$="TbUsuario"]')
        input_login.fill("")
        input_login.fill(username)

        input_password = page.locator('input[id$=TbSenha]')
        input_password.fill("")
        input_password.fill(password)
            
        login_button = page.locator('[ng-click="vm.login(vm.usuario)"]')

        # Espera uma resposta positiva do site após login para validar as credenciais do usuário antes de extrair os cookies.
        print("try triggered")
        start = time.perf_counter()
        try:
            with page.expect_response(lambda response: "Home/Index" in response.url) as response_info:
                login_button.press("Enter")
            print("Login Successful!")
            end = time.perf_counter()
        
        except KeyboardInterrupt:
            print("Operation interrupted")
            sys.exit(0)

        except Exception as e:
            print(e)
            sys.exit(0)

        print(end-start)

        context_data["Headers"] = response.headers
        context_data["Cookies"] = context.cookies()
        context_data["User-Agent"] = page.evaluate("navigator.userAgent")

    return context_data


def get_processos(context_data):
    """
    Requer cookies do usuário-fiscal para a extração dos dados JSON: retorna uma lista contendo elementos Dict, onde cada
    elemento, por sua vez, representa um processo individual.
    """
    base_url =  "https://www3.cfc.org.br/spwALTeste/pro-teste/Processo/ListarProcessoConsulta"

    all_records = []
    page_num = 1  # Número da página atual.
    PAGE_SIZE = 20  # Número de processos listados por página.

    session = requests.Session()  # Sessão especial a conter os cookies do usuário-fiscal.
    session.headers.update( {"User-Agent": context_data["User-Agent"]} )

    # Inserção dos cookies.
    for cookie in context_data["Cookies"]:
        if cookie['expires'] == -1:  # Curiosidade: 4h é a duração de validade dos cookies.
            print("Cookie expired")

        session.cookies.set(
            name=cookie['name'],
            value=cookie['value'],
            domain=cookie['domain'],
            path=cookie['path']
        )

    while True:
        
        # Filtros aplicados para a extração dos dados dos processos.
        inner_filter = {
            "numeroprocesso": "",
            "datainicioabertura": None,
            "datafimabertura": None,
            "datainicioarquivamento": "",          
            "datafimarquivamento": "",
            "qtdporpagina": 50,  # Revisar limite máximo, aqui.
            "numerodapagina": page_num,
            "filtroinstantaneo": ""
        }

        ofiltro_string = json.dumps(inner_filter)  # Converte os filtros aplicados em formato JSON.
        params = {'page': page_num, 'limit': PAGE_SIZE, 'ofiltro': ofiltro_string}  # Aplicação dos paramêtros para a sessão requests.
        try:
            response = session.get(base_url, params=params)  # Tentativa de abertura da sessão.
            status_code = response.status_code  # Resposta da tentativa.

            if status_code!=200:  # Se resposta = 200, significa não-sucesso.
                print(f"[ERROR] status {status_code}")
                break

            data = response.json()  # Depósito dos dados encontrados, se houve sucesso.
            current_batch = data.get("data", [])  # Insere os dados dict() em uma lista (list).
            if not current_batch["resultado"]:  # Se a lista vier vazia, significa que chegou-se ao limite dos dados JSON encontrados.
                break

            all_records.extend(current_batch["resultado"])  # Expande o resultado final na medida em que se encontra mais páginas JSON. 

            page_num+=1  # Segue para a página seguinte.
            time.sleep(1)  # Intervalo de 1 (um) segundo.
        
        # Lida com erros nas tentativas de extração, quebra o loop quando erro.
        except Exception as e:
            print(e)
            break

    return all_records  #  retorna uma lista do resultado da extração dos dados convertidos em dict.

if __name__=="__main__":
    context_data = get_context_data(USERNAME, PASSWORD)
    processos = get_processos(context_data) 

    mapping = None
    json_filename = "mapping.json"
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as file:
            try:
                mapping = json.load(file)
            except Exception as error:
                print(error)
                sys.exit(0)  # TEMP
    else:
        ...

    data_buffer = []
    for processo in processos:
        num_processo = processo["NumeroProcesso"]
        nome = processo["Nome"]
        num_registro = processo["NumRegistro"]
        fase_atual = str(processo["FaseAtual"])

        fase_atual_str = mapping["FaseAtual"][fase_atual]
        
        row_data = {
            "NumeroProcesso": num_processo,
            "Nome": nome,
            "NumRegistro": num_registro,
            "FaseAtual": fase_atual_str
        }

        data_buffer.append(row_data)

    processo_df = pd.DataFrame(data_buffer)
    print(processo_df.head())

    processo_df.to_excel("relatorio.xlsx", index=False)

