from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd

documentos = [
    "the cat sat on the mat",
    "the dog sat on the log",
    "cats and dogs are great pets",
    "the mat is for the cat",
    "dogs love to sit on logs"
]

cv = CountVectorizer()
bow_matrix = cv.fit_transform(documentos)
df_bow = pd.DataFrame(bow_matrix.toarray(), columns=cv.get_feature_names_out())
print("Matriz Bag-of-Words:")
print(df_bow)

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(documentos)
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
print("\nMatriz TF-IDF:")
print(df_tfidf)
print("palavra com maior peso no doc 4:", df_tfidf.iloc[4].idxmax())
print("com peso:", df_tfidf.iloc[4].max())

print("\nQuestão 7.3:")
print("Neste caso, o BoW")
print("'love', 'to', 'sit' e  'logs' porque são menos frequentes nos outros documentos (neste caso nem sequer aparecem em mais nenhum)")