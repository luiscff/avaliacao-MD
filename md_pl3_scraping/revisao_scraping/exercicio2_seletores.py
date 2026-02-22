import requests
from bs4 import BeautifulSoup

def main():
    url = "http://quotes.toscrape.com"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'lxml')

    print("--- Questão 2.1 (find/find_all) ---")
    # Usando find_all(), extraia todas as citações
    citacoes = soup.find_all('div', class_='quote')
    print(f"Total de citações encontradas: {len(citacoes)}")

    # Extrair todos os autores
    autores = soup.find_all('small', class_='author')
    print(f"Total de autores encontrados: {len(autores)}")
    
    # Extrair todas as tags
    tags = soup.find_all('a', class_='tag')
    print(f"Total de tags encontradas: {len(tags)}")

    # Usando find(), extraia o primeiro autor
    primeiro_autor = soup.find('small', class_='author').text
    print(f"Primeiro autor: {primeiro_autor}")

    # Extrair a primeira citação
    primeira_citacao = soup.find('div', class_='quote').find('span', class_='text').text
    print(f"Primeira citação: {primeira_citacao}")

    # Extrair o link "Next" (se existir)
    next_link = soup.find('li', class_='next')
    if next_link:
        print(f"Link Next: {next_link.find('a')['href']}")

    print("\n--- Questão 2.2 (select/select_one) ---")
    # Todas as tags dentro de cada citação (Exemplo para a primeira)
    primeira_quote_tags = soup.select_one('.quote').select('.tag')
    print(f"Tags da 1ª citação: {[t.text for t in primeira_quote_tags]}")

    # O autor da primeira citação usando hierarquia CSS
    autor_css = soup.select_one('.quote .author').text
    print(f"Autor (via CSS): {autor_css}")

    print("\n--- Questão 2.3 (Atributos) ---")
    # Exemplo na primeira citação
    quote_obj = soup.find('div', class_='quote')
    
    # Valor do href do link About do autor (geralmente é irmão do author ou filho do span)
    link_about = quote_obj.select_one('a[href*="author"]')['href']
    print(f"Link About: {link_about}")

    # Número total de tags
    num_tags = len(quote_obj.select('.tag'))
    print(f"Número de tags: {num_tags}")

if __name__ == "__main__":
    main()