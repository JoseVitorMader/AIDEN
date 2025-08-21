import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_static_page(url):
    """Realiza webscraping em páginas estáticas."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta exceção para erros HTTP
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página estática {url}: {e}")
        return None

def scrape_dynamic_page(url, element_id=None, class_name=None, tag_name=None):
    """Realiza webscraping em páginas dinâmicas usando Selenium."""
    options = Options()
    options.add_argument('--headless')  # Executar em modo headless (sem interface gráfica)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # É necessário ter o ChromeDriver instalado e no PATH, ou especificar o caminho.
    # Para o ambiente sandbox, pode ser necessário instalar o ChromeDriver.
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        if element_id:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        elif class_name:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
        elif tag_name:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, tag_name))
            )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except Exception as e:
        print(f"Erro ao acessar a página dinâmica {url}: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    # Exemplo de uso para página estática
    print("\n--- Teste de Webscraping Estático ---")
    static_url = "https://www.google.com"
    static_soup = scrape_static_page(static_url)
    if static_soup:
        print(f"Título da página estática: {static_soup.title.string}")

    # Exemplo de uso para página dinâmica (requer ChromeDriver)
    # Para testar, você precisaria de um site com conteúdo carregado via JS
    # e o ChromeDriver configurado corretamente no ambiente.
    print("\n--- Teste de Webscraping Dinâmico (requer ChromeDriver) ---")
    dynamic_url = "https://www.google.com"
    # element_id, class_name ou tag_name para esperar o carregamento
    dynamic_soup = scrape_dynamic_page(dynamic_url, element_id="APjFqb") # Exemplo de ID de elemento do Google
    if dynamic_soup:
        print(f"Título da página dinâmica: {dynamic_soup.title.string}")


