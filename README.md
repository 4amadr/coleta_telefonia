# Coleta de Dados de Telefonia com Selenium

Este projeto automatiza o processo de login e coleta de relatórios em sistemas web de telefonia (como GS e Callix), utilizando Python com a biblioteca Selenium. Ele foi criado para facilitar a extração de dados de ligações, minutos, custos e lucros de operadoras ou plataformas de telefonia.

---

## 📅 Casos de uso

* Automatiza o login em plataformas de relatórios de telefonia
* Extrai dados do dia anterior automaticamente
* Armazena os dados coletados em formato `.json`

---

## 📚 Estrutura do Projeto

```
coleta_telefonia/
├── automacao_login.py      # Lógica de login e interação com interfaces de sites GS e Callix
├── coleta_GS.py            # Execução principal e funções de coleta/salvamento dos relatórios GS
├── relatorio_telefonia.json# Arquivo de saída com dados extraídos (gerado automaticamente)
```

---

## 🚀 Tecnologias Utilizadas

* Python 3
* Selenium WebDriver
* WebDriver Manager
* Google Chrome (modo headless)

---

## 🔧 Requisitos

* Python 3.8+
* Google Chrome instalado
* ChromeDriver compatível (instalado automaticamente via `webdriver_manager`)

Instale as dependências:

```bash
pip install -r requirements.txt
```

**Exemplo de `requirements.txt`:**

```
selenium
webdriver-manager
pandas
```

---

## 🔄 Como usar

### 1. Configurar credenciais e URL

Edite o arquivo `coleta_GS.py` nas variáveis:

```python
url = "https://exemplo.com/login"
usuario = "seu_usuario"
senha = "sua_senha"
```

### 2. Executar o script

```bash
python coleta_GS.py
```

O script:

* Acessa o site
* Realiza o login
* Navega até os relatórios de "Minutagem"
* Seleciona o período "Ontem"
* Coleta os dados da tabela
* Salva tudo no arquivo `relatorio_telefonia.json`

---

## 📁 Arquivos principais

### `automacao_login.py`

Contém funções para:

* Iniciar o navegador com configurações de segurança desativadas
* Fazer login no sistema GS ou Callix
* Navegar até a tabela de ligações e selecionar o dia anterior

### `coleta_GS.py`

Responsável por:

* Controlar a execução geral
* Acessar menus do GS automaticamente
* Extrair os dados da tabela
* Salvar as informações estruturadas em um arquivo `.json`

---

## 🚫 Limitações conhecidas

* Os XPaths estão adaptados a um layout específico (se o site mudar, podem parar de funcionar)
* Não possui tratamento de login 2FA
* A coleta é feita para um período fixo (ontem), mas pode ser ajustada

---

## 🌐 Futuras melhorias

* Adicionar logging estruturado (loguru, por exemplo)
* Exportar para CSV/Excel além de JSON
* Adicionar interface web ou CLI com opções de data
* Coleta multiplataforma (GS, Callix, Vonix, etc)

---

## ✉️ Contato

Caso queira contribuir, relatar bugs ou sugerir melhorias:

* GitHub: [@4amadr](https://github.com/4amadr)

---

> "Automatizar rotinas repetitivas libera tempo para pensar em soluções criativas."
