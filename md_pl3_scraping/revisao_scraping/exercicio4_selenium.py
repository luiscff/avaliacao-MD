from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def main():
    # Questão 4.1 - Configurar Chrome Options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = Chrome(options=options)
    todas_citacoes = []

    try:
        print("A iniciar scraping dinâmico...")
        driver.get("http://quotes.toscrape.com/js/")
        
        while True:
            # Questão 4.2/4.3 - Aguardar carregamento
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quote"))
            )
            
            # Abordagem Híbrida (Selenium para carregar, BS4 para extrair - Questão 4.3)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            quotes = soup.select('.quote')
            
            for q in quotes:
                texto = q.select_one('.text').text
                autor = q.select_one('.author').text
                todas_citacoes.append({'autor': autor, 'texto': texto})
            
            print(f"Extraídas {len(quotes)} citações da página atual.")

            # Questão 4.4 - Paginação (Clicar no botão Next)
            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, 'li.next > a')
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(1) # Pausa para garantir início do carregamento
            except:
                print("Não há mais páginas (botão Next não encontrado).")
                break
                
    finally:
        driver.quit()
        
    print(f"Total final de citações extraídas: {len(todas_citacoes)}")

if __name__ == "__main__":
    main()