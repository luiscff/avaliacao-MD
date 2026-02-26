from nltk.tokenize import word_tokenize
from nltk import pos_tag

frase = "They are flying planes to Paris for a conference"
tokens = word_tokenize(frase)
tags = pos_tag(tokens)
print(tags)

print("\nQuestão 5.2:")
print("Ambiguidade gramatical: 'flying' pode ser interpretado como um verbo ou como um adjetivo")