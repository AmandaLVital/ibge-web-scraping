from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def esperar_elemento(driver, by, value, tempo=10):
    """Aguarda até que um elemento esteja presente na página."""
    return WebDriverWait(driver, tempo).until(
        EC.presence_of_element_located((by, value))
    )

def esperar_e_clicar(driver, xpath, descricao, tempo=30, tentativas=3):
    """Aguarda e clica em um elemento específico."""
    for tentativa in range(tentativas):
        try:
            print(f"Aguardando {descricao}... (Tentativa {tentativa + 1})")
            elemento = esperar_elemento(driver, By.XPATH, xpath, tempo)
            driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", elemento)
            time.sleep(2)
            return True
        except Exception as e:
            if tentativa == tentativas - 1:
                print(f"Erro final ao clicar em {descricao}: {e}")
                return False
            time.sleep(2)

def extrair_dados(driver):
    """Extrai os dados de variação percentual (XPath: '%')."""
    # XPath para todas as variações com título "%"
    mensal_xpath = "//td[@class='x-col-0' and @title='%']"

    # Encontrar todos os elementos
    elementos = driver.find_elements(By.XPATH, mensal_xpath)

    # Extrair os valores
    valores = [elemento.text for elemento in elementos]

    print("Valores encontrados:")
    for valor in valores:
        print(valor)

    return valores

def capturar_html(driver):
    """Captura o HTML da página para depuração."""
    try:
        html = driver.page_source
        with open("pagina_carregada.html", "w", encoding="utf-8") as file:
            file.write(html)
        print("HTML da página salvo como 'pagina_carregada.html'")
    except Exception as e:
        print(f"Erro ao salvar HTML: {e}")

try:
    # Configurações do ChromeDriver
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Abrir URL
    url = "https://sidra.ibge.gov.br/tabela/7060"
    driver.get(url)
    time.sleep(7)

    # Clicar no botão "Marcar todos"
    if not esperar_e_clicar(driver, "//button[@data-cmd='marcarTudo']", "Marcar todos"):
        raise Exception("Falha ao marcar todos os elementos.")

    # Clicar no botão "Visualizar"
    if not esperar_e_clicar(driver, "//button[contains(text(),'Visualizar')]", "Visualizar"):
        raise Exception("Falha ao clicar em 'Visualizar'.")

    print("Aguardando resultados carregarem...")
    time.sleep(10)

    # Capturar o HTML da página para depuração
    capturar_html(driver)

    # Extrair os dados
    valores = extrair_dados(driver)

    # Caso queira salvar em um arquivo ou usar os valores extraídos, você pode continuar aqui
    # Por exemplo, você pode salvar em um CSV ou realizar outra operação.

except Exception as e:
    print(f"Erro durante a execução: {e}")
finally:
    driver.quit()
