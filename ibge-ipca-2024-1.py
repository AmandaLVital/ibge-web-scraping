from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def esperar_elemento(driver, by, value, tempo=10):
    return WebDriverWait(driver, tempo).until(
        EC.presence_of_element_located((by, value))
    )

def esperar_e_clicar(driver, xpath, descricao, tempo=30, tentativas=3):
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
    try:
        # Esperar página carregar completamente
        time.sleep(5)
        
        # Usar o XPath original que funcionava
        elementos = driver.find_elements(By.XPATH, "//td[@class='x-col-0' and @title='%']")
        
        if len(elementos) >= 2:
            mensal = elementos[0].text
            acumulado = elementos[1].text
            
            dados = {
                'Indicador': ['IPCA - Variação mensal (%)', 'IPCA - Variação acumulada no ano (%)'],
                'Valor': [mensal, acumulado]
            }
            
            df = pd.DataFrame(dados)
            print("\nValores encontrados:")
            print(df)
            
            df.to_csv('ipca_dados.csv', index=False)
            print("\nDados salvos em 'ipca_dados.csv'")
            
            return df
        else:
            raise Exception("Não foram encontrados elementos suficientes")
            
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
        raise

try:
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    url = "https://sidra.ibge.gov.br/tabela/7060"
    driver.get(url)
    time.sleep(7)
    
    if not esperar_e_clicar(driver, "//button[@data-cmd='marcarTudo']", "Marcar todos"):
        raise Exception("Falha ao marcar todos os elementos.")
        
    if not esperar_e_clicar(driver, "//button[contains(text(),'Visualizar')]", "Visualizar"):
        raise Exception("Falha ao clicar em 'Visualizar'.")
    
    print("Aguardando resultados carregarem...")
    time.sleep(10)
    
    df = extrair_dados(driver)

except Exception as e:
    print(f"Erro durante a execução: {e}")
finally:
    driver.quit()