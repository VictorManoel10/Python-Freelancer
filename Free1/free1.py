from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

# Configuração de opções para o ChromeDriver
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    # Desativa a solicitação de confirmação ao baixar arquivos
    'download.prompt_for_download': False,
    # Define o diretório padrão para salvar os downloads
    'download.default_directory': r'C:\Users\lordz\Documents\Python Freelancer\Python-Freelancer\Free1\relatorios',
    # Permite múltiplos downloads sem confirmação
    'profile.default_content_setting_values.automatic_downloads': 1,
})

# Inicializa o navegador Chrome com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

# 1. Acessa o site para consulta de empresas
driver.get('https://consulta-empresa.netlify.app/')
sleep(2.5)  # Aguarda o carregamento inicial do site

# 2. Realiza o login no site
# Localiza o campo de usuário e insere o nome
campo_usuario = driver.find_element(By.XPATH, "//input[@id='username']")
sleep(1)
campo_usuario.click()
campo_usuario.send_keys('jhonatan')

# Localiza o campo de senha e insere a senha
campo_senha = driver.find_element(By.XPATH, "//input[@id='password']")
sleep(1)
campo_senha.click()
campo_senha.send_keys('12345678')

# Localiza e clica no botão "Entrar" para acessar a plataforma
botao_entrar = driver.find_element(By.XPATH, "//button[@class='btn btn-primary btn-lg']")
sleep(1)
botao_entrar.click()
sleep(3)

# Função para baixar relatórios e renomeá-los com base no nome da empresa
def baixar_relatorios_das_empresas(driver):
    # Localiza os nomes das empresas exibidos na página
    nomes_empresas = driver.find_elements(By.XPATH, "//td[@name='nome_empresa']")
    # Localiza os botões de download associados a cada empresa
    botoes_download_pdf = driver.find_elements(By.XPATH, "//button[@class='download-btn']")
    
    # Itera sobre os nomes das empresas e seus respectivos botões de download
    for nome, botao_pdf in zip(nomes_empresas, botoes_download_pdf):
        # Clica no botão de download
        botao_pdf.click()
        sleep(2)  # Aguarda o início do download

        # Define os caminhos e nomes de arquivos para renomear os relatórios
        diretorio = r'C:\Users\lordz\Documents\Python Freelancer\Python-Freelancer\Free1\relatorios'
        nome_antigo = 'perfil_empresa.pdf'  # Nome padrão do arquivo baixado
        novo_nome = f'{nome.text}.pdf'  # Nome novo baseado no nome da empresa

        # Monta os caminhos completos para renomeação
        caminho_completo_antigo = os.path.join(diretorio, nome_antigo)
        caminho_completo_novo = os.path.join(diretorio, novo_nome)

        # Aguarda até que o arquivo seja completamente baixado
        while not os.path.exists(caminho_completo_antigo):
            sleep(1)
        
        # Renomeia o arquivo baixado com o nome da empresa correspondente
        os.rename(caminho_completo_antigo, caminho_completo_novo)

# Loop para iterar entre as páginas e baixar os relatórios de todas as empresas
while True:
    # Baixa e renomeia os relatórios da página atual
    baixar_relatorios_das_empresas(driver)
    
    # Localiza o botão "Próxima Página"
    botao_proxima_pagina = driver.find_element(By.XPATH, "//button[@id='nextBtn']")
    
    # Verifica se o botão está desabilitado (indicando que não há mais páginas)
    if botao_proxima_pagina.get_attribute('disabled'):
        break  # Sai do loop se não houver mais páginas

    # Caso contrário, clica no botão para ir para a próxima página
    botao_proxima_pagina.click()
    sleep(3)  # Aguarda o carregamento da próxima página

# Aguarda o usuário pressionar ENTER antes de encerrar o programa
input('Aperte ENTER para fechar')
