"""
Purpose of this script is to fetch data from digital records contained in a website and export it neatly as an xslx file.
"""
from playwright.sync_api import sync_playwright
import pandas as pd

LOGIN = "batista"
PASSWORD = "1010"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www3.cfc.org.br/spwALTeste/SCCTeste/login.aspx")

    page.wait_for_load_state("networkidle")

    input_login = page.locator('input[id$="txtUsuario_I"]')
    input_login.fill("")
    input_login.fill(LOGIN)

    input_password = page.locator('input[id$=txtSenha_I]')
    input_password.fill("")
    input_password.fill(PASSWORD)

    login_button = page.locator('input[id$="btnConfirmar_I"]')
    login_button.press("Enter")

    fisc_icon = page.locator("[id=\"3\"]")
    #fisc_icon.wait_for(state="visible", timeout=10000)  # Could well be used to test for right permissions after login
    fisc_icon.click()
    #page.wait_for_timeout(300)

    fisc_icon_2 = page.locator("[id=\"10\"]")
    #fisc_icon.wait_for(state="visible", timeout=10000)  # how to adapt this to headless mode?
    fisc_icon_2.click() 
    #page.wait_for_load_state('networkidle')

    processo_btn = page.locator("button[ng-click*='listarComPaginacao']")
    
    """
    <div class="spw-color-text--teal-700 quadradoicone col-xs-6 col-sm-4 col-md-4 col-lg-4 ng-scope" ng-if="false != true" ng-click="vmp.irPara('/spwALTeste/pro-teste/processo/consulta')" role="button" tabindex="0">
                            <i class="material-icons spw-material-icons--40pt">folder</i>
                            <div class="fontetexto">Processo</div>
                        </div>
    """

    page.wait_for_timeout(3000)

    browser.close()

