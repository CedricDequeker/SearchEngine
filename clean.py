import fitz  # PyMuPDF
import spacy
import re

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(filepath):
    with fitz.open(filepath) as pdf_document:
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text


# Fonction pour nettoyer le texte
def clean_text(text, lang='fr'):
    nlp_fr = spacy.load('fr_core_news_sm')

    text = text.lower()

    text_pct = re.sub(r'[^\w\s]', ' ', text)    # Supprimer la ponctuation (tout sauf les lettres et les espaces)

    text = re.sub(r'\b([a-zA-Z])\b', '', text_pct)    # Supprimer les mots d'une seule lettre

    text_space = re.sub(r'[ \t\n]+', ' ', text)      # Supprimer les espaces multiples

    doc = nlp_fr(text_space)
    cleaned_text =' '.join([token.text for token in doc if not token.is_stop])    #Suppression des stop words
    
    regex = r"[^a-zA-ZàâäéèêëîïôöùûüÿçÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ ]"
    very_cleaned_text = re.sub(regex, '', cleaned_text)   # Supprimer les caractères spéciaux

    doc = nlp_fr(very_cleaned_text)
    return [token.lemma_ for token in doc]  #Tokenization et Lemmatization


# Fonction pour générer les n-grammes
def generate_ngrams(tokens, n):
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngrams.append(tokens[i:i + n])
    return ngrams


# Construire l'index inversé
def create_inverted_index(index,corpus,name):
    for word in corpus:
        if word in index:
            # Si le mot est déjà présent et que le document existe, on incrémente le compteur
            if name in index[word]:
                index[word][name] += 1
            else:
                # Si le document n'existe pas encore pour ce mot, on l'ajoute avec un compteur de 1
                index[word][name] = 1
        else:
            # Si le mot n'existe pas encore dans l'index, on crée une nouvelle entrée avec un compteur de 1
            index[word] = {name: 1}
    return index


def add_index (data,fichier_json):
    import json
    try:
        with open(fichier_json, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
    except FileNotFoundError:
        donnees = {}

    for cle, valeur in data.items():
        if cle in donnees:
            donnees[cle].update(valeur)
        else:
            donnees[cle] = valeur

    # Écrire les données mises à jour dans le fichier JSON
    with open(fichier_json, 'w', encoding='utf-8') as fichier:
        json.dump(donnees, fichier, indent=4,ensure_ascii=False)

    print(f"Le dictionnaire a été ajouté avec succès au fichier {fichier_json}")



#data=create_inverted_index({},clean_text(extract_text_from_pdf("data/Management/Project_Management_3.pdf")), "Management/Project_Management_3.pdf")
#add_index(data,fichier_json="data/index.json")