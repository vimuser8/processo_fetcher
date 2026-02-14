from playwright.sync_api import sync_playwright
import getpass
import json
import requests
import sys, os, time

USERNAME = input('Username: ')  # What is a way to handle unsuccessful login attempt?
PASSWORD = getpass.getpass('Password: ') 

def get_context_data(username, password, headless=True):
    """
    Logs in on a website and retrieves cookies that can be used to grant requests permission to gather data.
    """
    context_data = dict()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context()
        page = context.new_page()

        response = page.goto("https://www3.cfc.org.br/spwALTeste/pro-teste/home/Login")
        page.wait_for_load_state("networkidle")

        page.locator("select[ng-model='vm.usuario.tipoUsuario']").select_option("1")
            
        input_login = page.locator('input[id$="TbUsuario"]')
        input_login.fill("")
        input_login.fill(username)

        input_password = page.locator('input[id$=TbSenha]')
        input_password.fill("")
        input_password.fill(password)
            
        login_button = page.locator('[ng-click="vm.login(vm.usuario)"]')
        with page.expect_response(lambda response: "Home/Index" in response.url) as response_info:  # waits till credentials are validated
            login_button.press("Enter")
            #actual_password = page.input_value("input[id$=TbSenha]")
            #print(actual_password)

        context_data["Headers"] = response.headers  # in case this can be made useful
        context_data["Cookies"] = context.cookies()
        context_data["User-Agent"] = page.evaluate("navigator.userAgent")

    return context_data


def get_processos(context_data):
    """
    Once we have the cookies, etc. we're allowed to extract JSON-type data from the URL, a JSON api.
    """
    base_url =  "https://www3.cfc.org.br/spwALTeste/pro-teste/Processo/ListarProcessoConsulta"

    all_records = []
    page_num = 1
    PAGE_SIZE = 20  # processos per page

    session = requests.Session()
    session.headers.update( {"User-Agent": context_data["User-Agent"]} )

    for cookie in context_data["Cookies"]:
        if cookie['expires'] == -1:
            print("Cookie expired")

        session.cookies.set(
            name=cookie['name'],
            value=cookie['value'],
            domain=cookie['domain'],
            path=cookie['path']
        )

    while True:
        inner_filter = {
            "numeroprocesso": "",
            "datainicioabertura": None,
            "datafimabertura": None,
            "datainicioarquivamento": "",          
            "datafimarquivamento": "",
            "qtdporpagina": 50,
            "numerodapagina": page_num,
            "filtroinstantaneo": ""
        }

        ofiltro_string = json.dumps(inner_filter)  # converts filters to JSON-readable format
        params = {'page': page_num, 'limit': PAGE_SIZE, 'ofiltro': ofiltro_string}
        try:
            response = session.get(base_url, params=params)
            status_code = response.status_code

            if status_code!=200:
                print(f"[ERROR] status {status_code}")
                break

            data = response.json()
            current_batch = data.get("data", [])  # parameters: "key" but what does 
            if not current_batch["resultado"]:  # an empty list implies we have run out of process (reached the last possible page)
                break

            #print(len(current_batch["resultado"]))  #  current_match["key"] is a list that contains dicts such that each dict (containing subdicts themselves) are represented by an index, so that current_batch["resultado"][i] contains data about a WHOLE PROCESS.
            #print(current_batch["resultado"][0]["NumeroProcesso"])

            all_records.extend(current_batch["resultado"])  # more indices (processes) are added if they exist

            page_num+=1
            time.sleep(1)
        
        except Exception as e:
            print(e)
            break

    return all_records  # type(all_records) = list

if __name__=="__main__":
    context_data = get_context_data(USERNAME, PASSWORD)
    processes = get_processos(context_data) 
    for process in processes:  # processes[0] and so on... where each index represents a whole process
        print(process["NumeroProcesso"], process["NumRegistro"], process["Nome"], process["FaseAtual"], process["EtapaAtual"], process["SituacaoAtual"])

