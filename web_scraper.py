import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
from typing import Optional, Dict, List, Any

def scrape_static_page(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[BeautifulSoup]:
    """Enhanced static page scraping with better error handling and user agent."""
    try:
        # Default headers to mimic a real browser
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        if headers:
            default_headers.update(headers)
        
        response = requests.get(url, headers=default_headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página estática {url}: {e}")
        return None

def extract_search_results(soup: BeautifulSoup, search_engine: str = "google") -> List[Dict[str, Any]]:
    """Extract search results from different search engines."""
    results = []
    
    try:
        if search_engine.lower() == "google":
            # Updated selectors for Google search results
            result_selectors = [
                'div.g',  # Main result container
                'div[data-sokoban-container]',  # Alternative container
            ]
            
            for selector in result_selectors:
                result_containers = soup.find_all('div', class_=lambda x: x and 'g' in x.split() if x else False)
                if result_containers:
                    break
            
            for container in result_containers[:5]:  # Get top 5 results
                try:
                    # Try different title selectors
                    title_element = (container.find('h3') or 
                                   container.find('a') or 
                                   container.find('div', class_='BNeawe vvjwJb AP7Wnd'))
                    
                    title = title_element.get_text().strip() if title_element else "Sem título"
                    
                    # Try different snippet selectors
                    snippet_element = (container.find('span', class_='aCOpRe') or
                                     container.find('div', class_='BNeawe s3v9rd AP7Wnd') or
                                     container.find('div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'))
                    
                    snippet = snippet_element.get_text().strip() if snippet_element else "Sem descrição"
                    
                    # Try to get URL
                    link_element = container.find('a', href=True)
                    url = link_element['href'] if link_element else ""
                    
                    if title and snippet:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url,
                            'source': 'google'
                        })
                        
                except Exception as e:
                    continue
                    
        elif search_engine.lower() == "bing":
            # Bing search result selectors
            result_containers = soup.find_all('li', class_='b_algo')
            
            for container in result_containers[:5]:
                try:
                    title_element = container.find('h2')
                    title = title_element.get_text().strip() if title_element else "Sem título"
                    
                    snippet_element = container.find('p')
                    snippet = snippet_element.get_text().strip() if snippet_element else "Sem descrição"
                    
                    link_element = container.find('a', href=True)
                    url = link_element['href'] if link_element else ""
                    
                    results.append({
                        'title': title,
                        'snippet': snippet,
                        'url': url,
                        'source': 'bing'
                    })
                except Exception:
                    continue
    
    except Exception as e:
        print(f"Erro ao extrair resultados de busca: {e}")
    
    return results

def search_web(query: str, search_engine: str = "google", num_results: int = 5) -> Dict[str, Any]:
    """Perform web search with enhanced result extraction."""
    try:
        # Construct search URL
        if search_engine.lower() == "google":
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
        elif search_engine.lower() == "bing":
            search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}&count={num_results}"
        else:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
            search_engine = "google"
        
        print(f"🔍 Searching: {search_url}")
        
        # Get page content
        soup = scrape_static_page(search_url)
        if not soup:
            return {"query": query, "results": [], "error": "Failed to retrieve search page"}
        
        # Extract results
        results = extract_search_results(soup, search_engine)
        
        # Add metadata
        search_data = {
            "query": query,
            "search_engine": search_engine,
            "timestamp": datetime.datetime.now().isoformat(),
            "num_results": len(results),
            "results": results
        }
        
        return search_data
        
    except Exception as e:
        print(f"Erro na busca web: {e}")
        return {"query": query, "results": [], "error": str(e)}

def get_page_summary(url: str, max_paragraphs: int = 3) -> Dict[str, Any]:
    """Get a summary of a web page content."""
    try:
        soup = scrape_static_page(url)
        if not soup:
            return {"url": url, "summary": "", "error": "Failed to retrieve page"}
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Sem título"
        
        # Extract main content paragraphs
        paragraphs = soup.find_all('p')
        content_paragraphs = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 50:  # Only consider substantial paragraphs
                content_paragraphs.append(text)
                if len(content_paragraphs) >= max_paragraphs:
                    break
        
        summary = "\n\n".join(content_paragraphs)
        
        return {
            "url": url,
            "title": title_text,
            "summary": summary,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"url": url, "summary": "", "error": str(e)}

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


