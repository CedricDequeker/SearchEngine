# SearchEngine


## Description  

SearchEngine est une application web de moteur de recherche intégrant la technologie RAG !  
Développé en Python, ce projet vous permet de rechercher des documents PDF parmi une bibliothèque prédéfinie et de créer des conversations avec un chatbot ayant connaissance de vos documents.  
Le modèle d'IA étant en local, la confidentialité de toutes vos données, questions et réponses est préservée !  

Les domaines d'application pour cette technologie sont vastes :  

Médical : obtenir des réponses sur son bilan de santé.  
Entreprise : créer un assistant pour les collaborateurs, contenant des données confidentielles sur l'entreprise.  
Éducatif : concevoir un assistant répondant aux questions sur des cours spécifiques.  

Comment cela fonctionne ?  
Les documents PDF sont traités, nettoyés, puis classifiés dans l'index.  
Un index inversé est mis en place pour optimiser les recherches, et un score TF-IDF est précalculé pour améliorer les performances du moteur de recherche.  
Ce projet intègre un LLM qui, associé à l'architecture RAG et à une base de données vectorielle, est capable de répondre à des questions basées sur le contenu des fichiers PDF et ainsi de générer des résumés et des réponses pertinentes. réponses pertinantes.  

![image](https://github.com/user-attachments/assets/5f7c0c82-c7d1-42b4-b019-938b7f4fd36b)
![image](https://github.com/user-attachments/assets/174cb4cc-bb09-440a-bb9b-4197676e7d6f)


### Arborescence  

SearchEngine/  
├── chat_history/               # Stockage de l'historique des chats  
|  
├── data/                       # Dossier contenant la bibliothèque de PDF et l'index de recherche  
│   ├── index.json                # Fichier JSON pour l'indexation des documents  
│   ├── Cours AI/  
│   ├── Management/  
│   ├── Perso/  
│   └── temp/                     # Sous-dossier temporaire pour les fichiers déposés  
|  
├── static/                     # Dossier pour les fichiers statiques (CSS, images, JS)  
│   ├── css/  
│   ├── images/  
│   └── js/  
|  
├── templates/                  # Dossier pour les templates HTML  
│   ├── base.html                 # Template de base pour l'application  
│   ├── chatbot.html              # Template pour l'interface de chatbot  
│   └── home.html                 # Template pour la page d'accueil  
|  
├── vectorestore/               # Dossier pour le stockage des vecteurs de recherche  
|  
├── app.py                      # Fichier principal de l'application Flask  
├── clean.py                    # Script pour nettoyer les PDFs et les intégrer à l'index  
├── research.py                 # Script pour la recherche des documents  
├── localRAG.py                 # Script pour l'exécution local du Chatbot avec RAG  
|  
├── README.md  
└── LICENSE  


## Installation

1. Clonez le dépôt :
```sh
git clone https://github.com/CedricDequeker/SearchEngine/tree/main
cd SearchEngine
```

2. Créez un environnement virtuel et activez-le :
```sh
conda create -n [your_env_name] python=3.12.7 -y
conda activate [your_env_name]
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

3. Installez Ollama avec Mistral
Téléchargez et installez l'application Ollama : https://ollama.com
Une fois Ollama lancé, ajoutez Mistral :
```sh
ollama pull mistral
ollama list
```


## Utilisation
Lancez l'application Flask :
```sh
python app.py
```
Ouvrez votre navigateur et accédez à http://127.0.0.1:5000 pour utiliser l'application.


## Auteur
Dequeker Cédric  
https://www.linkedin.com/in/cédric-dequeker-b19027254/
