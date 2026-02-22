import requests
import time
import random

def main():
    url = "http://httpbin.org/get"
    
    # Questão 1.1
    # Criar headers realistas (User-Agent, Accept-Language)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8'
    }

    # Fazer requisição GET
    response = requests.get(url, headers=headers)

    # Verificar status code
    print(f"Status Code: {response.status_code}")

    # Imprimir os headers enviados (estão na resposta)
    dados = response.json()
    print("\n--- Headers Enviados ---")
    print(dados.get('headers'))

    # Questão 1.2
    # Extrair o IP do cliente da resposta
    ip_cliente = dados.get('origin')
    print(f"\nIP do Cliente: {ip_cliente}")

    # Identificar o Content-Type da resposta
    content_type = response.headers.get('Content-Type')
    print(f"Content-Type da Resposta: {content_type}")

# Questão 1.3
def requisicao_segura(url, headers=None, timeout=5, tentativas=3):
    """
    Realiza uma requisição GET segura com retries e tratamento de erros.
    """
    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(tentativas):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Tentativa {i+1} falhou: {e}")
            if i < tentativas - 1:
                time.sleep(random.uniform(1, 2)) # Espera antes de tentar dnv
    
    return None

if __name__ == "__main__":
    main()