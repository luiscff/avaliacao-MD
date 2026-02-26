import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

texto_noticia = """Apple Inc. announced yesterday that CEO Tim Cook will visit Portugal next week. 
The company plans to open a new office in Lisbon with 500 employees. 
Microsoft's Satya Nadella also expressed interest in expanding to Porto. 
The EU Commission approved the deal on January 15, 2024."""

tokens = word_tokenize(texto_noticia)
tags = pos_tag(tokens)
arvore_ner = ne_chunk(tags)

entidades = []
for no in arvore_ner:
    if hasattr(no, 'label'):
        nome = " ".join(c[0] for c in no)
        tipo = no.label()
        entidades.append((nome, tipo))

df = pd.DataFrame(entidades, columns=['Entidade', 'Tipo'])
print(df)
print("\nFrequências:")
print(df['Entidade'].value_counts())

print("\nQuestão 6.4:")
print("Erros possíveis: Apple e Microsoft podem ser considerados pessoas por começarem com letras maiúsculas. Tim Cook pode ser considerado uma organização por ter CEO antes. A data é ignorada. Pode nao separar 'Apple' de 'Inc.', por exemplo.")