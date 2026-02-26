from nltk.tokenize import word_tokenize, sent_tokenize
import re

texto = "Dr. Smith went to Washington D.C. on Jan. 15th, 2023. He said: 'Let's meet at 10 a.m. - I'll be there!'"

# 2.1
palavras = word_tokenize(texto)
frases = sent_tokenize(texto)

print(palavras)
print(frases)

#  2.2
print("Problema: Abreviaturas(Dr., D.C., a.m.), contrações (Let's, I'll) e pontuação isolada podem ser separadas erradamente.")

# 2.3
regex = r"(?:[A-Z]\.)+|(?:[a-z]\.)+|[A-Z][a-z]+\.|\w+(?:'\w+)?|[^\w\s]"
solucao = [t for t in re.findall(regex, texto) if t.strip()]

print(solucao)