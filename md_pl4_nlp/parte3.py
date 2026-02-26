from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

textos = [
    "The book is on the table",
    "To be or not to be, that is the question",
    "The search for the meaning of life is the meaning of life"
]

stop_padrao = set(stopwords.words('english'))
resultado = [[w for w in word_tokenize(t.lower()) if w not in stop_padrao] for t in textos]
print(resultado)

def remover_freq_50(lista_de_textos):
    num_textos = len(lista_de_textos)
    
    # criar um conjunto de palavras para cada texto
    palavras_por_texto = []
    for frase in lista_de_textos:
        frase_minuscula = frase.lower()
        tokens = word_tokenize(frase_minuscula)
        palavras_por_texto.append(set(tokens))

    # contar a frequência de cada palavra
    contador = Counter()
    for grupo_palavras in palavras_por_texto:
        contador.update(grupo_palavras)
    
    # palavras que aparecem em mais de 50% dos textos
    palavras_para_tirar = []
    for palavra in contador:
        frequencia = contador[palavra] / num_textos
        if frequencia > 0.5:
            palavras_para_tirar.append(palavra)
    
    resultado = []
    for frase in lista_de_textos:
        frase_minuscula = frase.lower()
        tokens_da_frase = word_tokenize(frase_minuscula)
        
        frase_limpa = []
        for p in tokens_da_frase:
            if p not in palavras_para_tirar:
                frase_limpa.append(p)
        resultado.append(frase_limpa)
        
    return resultado

print(remover_freq_50(textos))