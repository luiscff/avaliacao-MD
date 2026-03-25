from neo4j import GraphDatabase 
import spacy 
import pandas as pd 
from typing import List, Dict, Tuple 
import re 

# Carregue o modelo NLP em português 
nlp = spacy.load("pt_core_news_sm") 

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session(database="joao") as session:
            result = session.run(query, parameters)
            return [record for record in result]

conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")

try:
    result = conn.query("RETURN 'Funcionou' as message")
    print(result[0]["message"])
except Exception as e:
    print(f"Erro ao conectar: {e}")

def extract_entities(text: str) -> List[Tuple[str, str]]:
    """
    Retorne lista de tuplas (entidade, tipo) 
    TODO: Implemente a extração de entidades usando spaCy 
    Dica: Use nlp(text) e itere sobre doc.ents
    """
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    
    return entities

texto_exemplo = """
A OpenAI lançou o ChatGPT em novembro de 2022. Sam Altman criou a empresa.
ChatGPT utiliza aprendizagem profunda e foi desenvolvido em São Francisco.
"""

entities = extract_entities(texto_exemplo)

print("Entidades encontradas:")
for entity, label in entities:
    print(f"- {entity} ({label})")

def extract_relations(text: str) -> List[Tuple[str, str, str]]:
    """
    Extrai relações simples baseadas em padrões sintáticos. 
    Retorna lista de triplas (sujeito, relação, objeto) 
    TODO: Implemente a extração de relações baseada em dependências sintáticas 
    Dica: Procure por tokens com dep_ == "nsubj" e os seus objetos diretos
    """
    doc = nlp(text)
    relations = []

    for token in doc:
        if token.dep_ == "nsubj":
            verb = token.head
            
            subject = token.text
            relation = verb.lemma_
            
            for child in verb.children:
                if child.dep_ in ("obj", "iobj"):
                    obj = child.text
                    relations.append((subject, relation, obj))
    
    return relations

relations = extract_relations(texto_exemplo)

print("\nRelações encontradas:")
for subj, rel, obj in relations:
    print(f"- {subj} --[{rel}]--> {obj}")

# 2.3: A abordagem sintática falha ao lidar com frases complexas, voz passiva ou coreferências. Além disso, é muito rígida e ignora o contexto global. Para melhorar, poderíamos usar modelos de Machine Learning treinados para Extração de Relações (Relation Extraction) ou recorrer a Modelos de Linguagem (LLMs, como o BERT) para interpretar a semântica da frase.


def create_knowledge_graph(conn: Neo4jConnection, entities: List[Tuple[str, str]],
                           relations: List[Tuple[str, str, str]]):
    """
    Crie nós e relacionamentos no Neo4j baseado nas entidades e relações extraídas 
     
    TODO: Implemente a criação do knowledge graph 
    Dicas:  
    - Use CONSTRAINT para garantir unicidade dos nomes das entidades 
    - Use MERGE para criar nós evitando duplicação 
    - Use MATCH para encontrar nós existentes antes de criar relacionamentos
    """

    conn.query("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE")

    for name, label in entities:
        conn.query("""
            MERGE (e:Entity {name: $name})
            SET e.type = $type
        """, parameters={"name": name, "type": label})

    for subj, rel, obj in relations:
        conn.query("""
            MATCH (s:Entity {name: $subj})
            MATCH (o:Entity {name: $obj})
            MERGE (s)-[:RELACIONA_SE {tipo: $rel}]->(o)
        """, parameters={"subj": subj, "rel": rel, "obj": obj})

create_knowledge_graph(conn, entities, relations)
print("Knowledge graph criado com sucesso!")


def query_graph(conn: Neo4jConnection, entity_name: str):
    """
    Consulte o knowledge graph para encontrar conexões de uma entidade
    TODO: Implemente a consulta que retorna uma entidade e as suas conexões
    Dica: Use OPTIONAL MATCH para encontrar relacionamentos em ambas as direções
    """

    query = """
        MATCH (e:Entity {name: $name})
        OPTIONAL MATCH (e)-[r]-(connected)
        RETURN e.name AS entity, 
               collect(connected.name) AS connections, 
               collect(type(r) + ': ' + r.tipo) AS relation_types
    """
    
    result = conn.query(query, parameters={"name": entity_name})
    return result[0] if result else None


info = query_graph(conn, "OpenAI")
if info:
    print(f"\nEntidade: {info['entity']}")
    print(f"Conexões: {info['connections']}")
    print(f"Tipos de relação: {info['relation_types']}")

# 3.3- Porque ele atua como um "Get or Create" porque primeiro verifica se o nó já existe, se sim, reaproveita-o, se não, cria-o. Isto evita a inserção de nós duplicados. O CREATE insere sempre uma nova linha, o que cria lixo na base de dados. As CONSTRAINTS são vitais porque garantem a integridade dos dados (não permitem dois nós com o mesmo nome) e criam um índice automático que acelera a velocidade da própria instrução MERGE.

def process_documents(conn: Neo4jConnection, documents: List[Dict]):
    """ 
    Processe múltiplos documentos e enriquece o knowledge graph 
    Dicas: 
    - Para cada documento, extraia entidades e relações 
    - Crie nós do tipo Document com propriedades id, source e text 
    - Conecte as entidades aos documentos com relacionamento MENTIONED_IN 
    """

    for doc in documents:
        ents = extract_entities(doc["texto"])
        rels = extract_relations(doc["texto"])
        
        create_knowledge_graph(conn, ents, rels)
        
        conn.query("""
            MERGE (d:Document {id: $id})
            SET d.text = $texto, d.source = $fonte
        """, parameters={"id": doc["id"], "texto": doc["texto"], "fonte": doc["fonte"]})
        
        for name, _ in ents:
            conn.query("""
                MATCH (e:Entity {name: $name})
                MATCH (d:Document {id: $doc_id})
                MERGE (e)-[:MENTIONED_IN]->(d)
            """, parameters={"name": name, "doc_id": doc["id"]})

documentos = [ 
    { 
        "id": 1, 
        "texto": "Elon Musk fundou a SpaceX em 2002. A empresa lançou o Falcon 9.", 
        "fonte": "Wikipedia" 
    }, 
    { 
        "id": 2, 
        "texto": "Tesla, liderada por Elon Musk, produz veículos elétricos.", 
        "fonte": "Notícia" 
    }, 
    { 
        "id": 3, 
        "texto": "SpaceX e Tesla colaboram em projetos de tecnologia sustentável.", 
        "fonte": "Artigo" 
    } 
]

process_documents(conn, documentos) 
print("Documentos processados e integrados ao grafo!")

def find_important_entities(conn: Neo4jConnection):
    """ 
    Encontra as entidades mais conectadas no grafo 
    TODO: Implemente a análise de centralidade de grau 
    Dica: Conte o número de entidades distintas conectadas a cada nó 
    """

    query = """
        MATCH (e:Entity)-[r]-()
        RETURN e.name AS entidade, e.type AS tipo, count(DISTINCT r) AS num_conexoes
        ORDER BY num_conexoes DESC
        LIMIT 5
    """

    result = conn.query(query)
    for row in result:
        print(f"{row['entidade']} ({row['tipo']}): {row['num_conexoes']} conexões")

find_important_entities(conn)