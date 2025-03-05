import json
import math

# Charger l'index des documents
def load_index(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


# Fonction pour pré-calculer les scores TF-IDF
def calculate_tfidf(index, doc_count):
    tfidf_index = {}
    for term, docs in index.items():
        idf = math.log(doc_count / len(docs))  # Inverse Document Frequency
        tfidf_index[term] = {}
        for doc, count in docs.items():
            tf = count  # Term Frequency
            tfidf_index[term][doc] = tf * idf
    return tfidf_index


# Rechercher les documents avec un score de pertinence optimisé
def search_index_tfidf(query,tfidf_index):
    query_terms = query.lower().split()
    #tockenization et lemmatization non pertinente ici car long à executer et n'ajoute de la valeur que sur les verbes 
    doc_scores = {}

    for term in query_terms:
        if term in tfidf_index:
            for doc, score in tfidf_index[term].items():
                if doc not in doc_scores:
                    doc_scores[doc] = 0
                doc_scores[doc] += score

    # Normalisation des scores sur 100
    if doc_scores:
        max_score = max(doc_scores.values())
        doc_scores = {doc: round((score / max_score) * 100, 2) for doc, score in doc_scores.items()}


    # Tri des documents par score de pertinence
    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:3]


#index = load_index('data/index.json')
#tfidf_index = calculate_tfidf(index, 6)
#print(search_index_tfidf("cv dequeker et dauphin jumbo",tfidf_index))