import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from exercicio1_http import requisicao_segura

def extrair_livros(soup):
    """
    Extrai todos os livros de uma página BeautifulSoup (Questão 3.2)
    """
    livros = []
    articles = soup.select('article.product_pod')

    for article in articles:
        titulo = article.select_one('h3 > a')['title']
        
        preco_texto = article.select_one('p.price_color').text
        preco = float(preco_texto.replace('£', '').replace('Â', ''))
        
        disp_texto = article.select_one('p.instock.availability').text.strip()
        disponivel = "In stock" in disp_texto
        
        classes = article.select_one('p.star-rating')['class']
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(classes[1], 0) if len(classes) > 1 else 0
        
        url_relativa = article.select_one('h3 > a')['href']

        livros.append({
            'titulo': titulo,
            'preco': preco,
            'disponibilidade': disponivel,
            'rating': rating,
            'url': url_relativa
        })
    return livros

def main():
    url_base = "http://books.toscrape.com/catalogue/page-{}.html"
    todos_livros = []
    pagina = 1

    # Ciclo de Crawling (Questão 3.3)
    while True:
        url = url_base.format(pagina)
        print(f"A processar página {pagina}...")
        
        response = requisicao_segura(url)
        
        if not response:
            print("Falha na requisição ou fim das páginas.")
            break
            
        soup = BeautifulSoup(response.text, 'lxml')
        
        livros_pagina = extrair_livros(soup)
        if not livros_pagina:
            break
            
        todos_livros.extend(livros_pagina)
        
        if not soup.select_one('li.next'):
            break

        pagina += 1
        # Delay ético
        time.sleep(random.uniform(0.5, 1.5))

    # Questão 3.4 - Exportação e Análise
    print(f"Total de livros extraídos: {len(todos_livros)}")
    
    df = pd.DataFrame(todos_livros)
    
    # Exportar
    df.to_csv('dados/books.csv', index=False)
    df.to_json('dados/books.json', orient='records')
    print("Dados exportados para a pasta 'dados/'")

    # Análise simples
    if not df.empty:
        mais_caro = df.loc[df['preco'].idxmax()]
        print(f"\nLivro mais caro: {mais_caro['titulo']} (£{mais_caro['preco']})")
        print(f"Média de ratings: {df['rating'].mean():.2f}")

if __name__ == "__main__":
    main()