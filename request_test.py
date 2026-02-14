import requests
import json
#www3.cfc.org.br

cookies = [{'name': '_s_p_w_u', 'value': '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', 'domain': 'www3.cfc.org.br', 'path': '/', 'expires': 1771075278.238195, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}]
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
session = requests.Session()
session.headers.update({"User-Agent": user_agent})

headers ={'access-control-allow-origin': '*', 'cache-control': 'private', 'content-encoding': 'gzip', 'content-length': '5146', 'content-type': 'text/html; charset=utf-8', 'date': 'Sat, 14 Feb 2026 12:21:22 GMT', 'server': 'Microsoft-IIS/8.5', 'vary': 'Accept-Encoding', 'x-aspnet-version': '4.0.30319', 'x-aspnetmvc-version': '5.2', 'x-powered-by': 'ASP.NET'} 
base_url =  "https://www3.cfc.org.br/spwALTeste/pro-teste/Processo/ListarProcessoConsulta"


for cookie in cookies:
    if cookie['expires'] == -1:
        print("Cookie expired")

    #print(cookie['name'], cookie['value'], cookie['domain'], cookie['path'])
    session.cookies.set(
        name=cookie['name'],
        value=cookie['value'],
        domain=cookie['domain'],
        path=cookie['path']
    )

while True:  # Each process generated can have about 250 lines of data in a JSON file.
    page_size = 20
    page_num = 1
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

    ofiltro_string = json.dumps(inner_filter)
    params = {'page': page_num, 'limit': page_size, 'ofiltro': ofiltro_string}
    #response = requests.get(base_url, headers=headers, params=params)
    try:
        response = session.get(base_url, params=params)
        #response = requests.get(base_url, params=params)

        status_code = response.status_code

        if status_code!=200:
            print(f"[error] status {status_code}")
            break

        data = response.json()
        print(data)
        print(type(data))
        print(data.keys())

        #with open("data.json", "w", encoding="utf-8") as f:
        #    json.dump(data, f, indent=4, ensure_ascii=False)

        #    print("File saved successfully!")
        #current_batch = data.get("items", [])
        #print(type(current_batch))
        break

    except Exception as e:
        print(e)


