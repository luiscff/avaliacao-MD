import re

texto_bruto = """RT @user123: I LOVEEEE this product!!! It's amazingg 
Check it out at https://example.com #awesome #musthave 
Can't wait to buy more!!! <3 <3 <3"""

def limpeza(texto):
    texto = texto.lower()
    texto = texto.replace('<3', 'heart')
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'@\w+|#\w+', '', texto)
    texto = re.sub(r'(.)\1+', r'\1', texto)
    texto = re.sub(r'[^\w\s.,!?]', '', texto)
    return " ".join(texto.split())

print("Texto Limpo:", limpeza(texto_bruto))