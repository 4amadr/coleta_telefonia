from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
import pandas as pd

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-web-security')




def iniciar_driver(url):
    # Ignora avisos de segurança
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')

    try:
        driver = webdriver.Chrome(
            options.add_argument("--headless=new"),
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options 
            
        )
        driver.get(url)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o driver: {e}")
        return None


def login_gs(driver, url, usuario, senha, id_usuario, senha_id, botao_login):
    try:
        
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id_usuario))
        ).send_keys(usuario)

        driver.find_element(By.ID, senha_id).send_keys(senha)
        driver.find_element(By.XPATH, botao_login).click()

        return True
    except Exception as e:
        print(f"Erro durante o login: {e}")
        return False
    
def login_callix(driver, url, usuario, senha, campo_usuario_locator, campo_senha_locator, botao_login_locator):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(campo_usuario_locator)
        ).send_keys(usuario)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(campo_senha_locator)
        ).send_keys(senha)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(botao_login_locator)
        ).click()
        
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/clx-menu/nav/ul/li[6]/a/span'))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/clx-menu/nav/ul/li[6]/ul/li[5]/a'))
        ).click()
        
        #tabela de ligações dos clientes
        table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="router-view"]/clx-page/div[2]/clx-data-table/div/table'))
        )
        
        table_element.click()
        print("Tabela encontrada, começando a coletar os dados do dia...")
        
        
        # encontrar linhas com os dados
        linhas = WebDriverWait(table_element, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
        )
        '''
            opção para selecionar a data para o dia anterior da coleta
            sempre precisa ser a data anterior do dia atual
        '''
        try:
            # seleciona a data
            WebDriverWait(table_element, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="router-view"]/clx-page/div[2]/clx-data-table/clx-filter/div[1]/div[2]/clx-filter-tag/clx-datetime-filter-tag/clx-filter-tag-wrapper/div/span[2]'))
        ).click()
            
            # seleciona o dia anterior 
            WebDriverWait(table_element, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="router-view"]/clx-page/div[2]/clx-data-table/clx-filter/div[2]/div[1]/ul/li[3]'))
        ).click()
            
            '''o site só mostra as 10 primeiros agentes
            aqui será feita uma alteração para mostrar todos os 100 agentes
            mesmo que não haja 100 agentes vai mostrar todas do dia para coletas sem erros'''
            
            # seleciona a opção de mostragem
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-y4bw-container"]'))
            ).click()
            
        except TimeoutException as e:
            print("Erro ao localizar o botão de data:", e)
        
        '''WebDriverWait(table_element, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="router-view"]/clx-page/div[2]'))
        ).click()'''
        
        # armazenamento de todos os dados de ligação
        dados_lig = []
        
        # percorre todas as linhas
        for linha in linhas:
            spans = linha.find_elements(By.TAG_NAME, 'span')
            dados = [span.text.strip() for span in spans]
            if dados:
                dados_lig.append(dados)
                
        for linha in dados_lig:
            print(linha)
        
        return True
    except Exception as e:
        print(f"Erro ao logar: {e}")
        return False
#def login_vonix():