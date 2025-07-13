from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automacao_login import iniciar_driver, login_gs
import json
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Função auxiliar para aguardar e clicar
def clicar(driver, xpath, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()

# Função para aguardar e obter texto de um elemento
def obter_texto(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    ).text.strip()

# Acessa menus e extrai dados
def extrair_dados_GS(driver):
    try:
        # Navegação pelos menus
        clicar(driver, '//*[@id="4"]')                     # Relatórios
        clicar(driver, '//*[@id="4_0"]')                   # Minutagem
        clicar(driver, '//*[@id="periodopre"]')            # Período
        clicar(driver, '//*[@id="periodopre"]/option[2]')  # Ontem
        clicar(driver, '//*[@id="site"]/form/table/tbody/tr[5]/td/div/input')  # Filtrar

        # Captura das linhas da tabela
        linhas = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//tr[@class="cinza1" or @class="cinza2"]')
            )
        )

        dados = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if colunas:
                dados.append([col.text.strip() for col in colunas])

        return dados

    except Exception as e:
        print(f" Erro ao extrair dados: {e}")
        return []

# Captura os títulos e salva JSON com dados da tabela
def salvar_dados_json(driver, dados_tabela, nome_arquivo="dados_gs.json"):
    try:
        campos = [
            ("Cliente", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[1]'),
            ("VOIP/VOIP", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[2]'),
            ("Minutos", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[3]'),
            ("Valor Venda", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[4]'),
            ("Custo", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[5]'),
            ("Lucro", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[6]'),
            ("Lucratividade", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[7]'),
            ("Rentabilidade", '//*[@id="site"]/table/tbody/tr/td/table/tbody/tr[2]/th[8]')
        ]

        cabecalhos = {campo: obter_texto(driver, xpath) for campo, xpath in campos}
        cabecalhos["Dados"] = dados_tabela

        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(cabecalhos, f, indent=4, ensure_ascii=False)

        print(f"Dados salvos, arquivo: {nome_arquivo}")
        return True

    except Exception as e:
        print(f"Ops, teve erro ao salvar o JSON rs: {e}")
        return False

# --- Execução principal --- é necessário inserir o link do site, usuário e login
if __name__ == "__main__":
    url = ""
    usuario = ''
    senha = ""
    id_usuario = 'login'
    senha_id = 'senha'
    botao_login = '//*[@id="bt-login"]/input'

    driver = iniciar_driver(url)

    if login_gs(driver, url, usuario, senha, id_usuario, senha_id, botao_login):
        print("Login realizado com sucesso!")

        dados = extrair_dados_GS(driver)
        if dados:
            if salvar_dados_json(driver, dados, "relatorio_telefonia.json"):
                print(" JSON salvo com os dados extraídos.")
        else:
            print(" Nenhum dado encontrado para salvar.")
    else:
        print("Falha no login.")

    if driver:
        driver.quit()
