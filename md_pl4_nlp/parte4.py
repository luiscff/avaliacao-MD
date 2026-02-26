from nltk.stem import PorterStemmer, WordNetLemmatizer

palavras_teste = ['running', 'ran', 'runs', 'better', 'went', 'studies', 'studying', 'cacti', 'cactus']
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

for p in palavras_teste:
    print(f"Palavra: {p} | Stemming: {stemmer.stem(p)} | Lemmatization: {lemmatizer.lemmatize(p, pos='v')}")

print("\nQuestão 4.2:")
print("a) Stemming é superior em velocidade e agrupamento bruto (ex: studies -> studi)")
print("b) Lemmatization é superior na preservação morfológica e semântica (ex: better -> good)")
print("c) Ambos falham em gírias e erros ortográficos")