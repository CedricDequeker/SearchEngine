from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_ollama import OllamaLLM

#Variables générales
LLM_MODEL = "mistral"
PERSIST_DIRECTORY = "vectorestore"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L6-v2"
VECTORSTORE = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))

#1. Importer un document PDF dans une base de données vectorielle
def import_pdf_document (document_name,chunk_size=1000, chunk_overlap=200,embedding_model="sentence-transformers/paraphrase-MiniLM-L6-v2",persist_directory="vectorestore"):

    try:
        loader = PyPDFLoader(document_name)
        documents = loader.load()
    except Exception as e:
        print(f"Erreur lors du chargement du document : {e}, vérfiez que le fichier existe et est au format pdf.")

    existing_docs = get_existing_documents(VECTORSTORE)
    if document_name in existing_docs:
        print(f"Le document {document_name} est déjà indexé. Import annulé.")
        return
    
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,  # Taille des chunks
    chunk_overlap=chunk_overlap  # Chevauchement
    )   

    chunks = []
    for doc in documents:
        page_chunks = text_splitter.create_documents([doc.page_content])
        for chunk in page_chunks:
            chunks.append({
                "text": chunk.page_content,  # Texte brut
                "metadata": doc.metadata  # Métadonnées
            })

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    vectorstore.add_texts(texts=[chunk["text"] for chunk in chunks],
    metadatas=[chunk["metadata"] for chunk in chunks])

    print("Metadata", [chunk["metadata"] for chunk in chunks])
    print("Document", document_name, "importé avec succès !")

#import_pdf_document("data/Perso/CV_DEQUEKER_fr.pdf")


#2. Système de recherche et de réponse basé sur RAG   
def RAG_system(query,vectorstore, llm_model,document_name=None):
    if document_name is not None:
        relevant_docs_score = vectorstore.similarity_search_with_score(query, k=4, filter = {"source": 'data/' + document_name})
        relevant_docs = [doc for doc, score in relevant_docs_score]
    else :
        relevant_docs_score = vectorstore.similarity_search_with_score(query, k=4)
        relevant_docs = [doc for doc, score in relevant_docs_score if score <= 50]

    if relevant_docs:
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"Répond à cette questions UNIQUEMENT à l'aide du contexte suivant. Voici le contexte :\n{context}\n Répond à cette question : {query}. Tu ne dois pas mentionner l'existence du contexte dans ta réponse."
    else:
        print("Aucun document pertinent trouvé. Utilisation du modèle LLM pour répondre à la question.")
        prompt = f"{query}"
    
    llm = OllamaLLM(model=llm_model)
    response = llm.invoke(prompt)

    return response

#3. Récupérer les nom des documents existants dans la base de données vectorielle
def get_existing_documents(vectorstore):
    collection = vectorstore.get()  # Récupère toutes les données stockées
    sources = set()
    
    if "metadatas" in collection:
        for metadata in collection["metadatas"]:
            if metadata and "source" in metadata:
                sources.add(metadata["source"])  # Stocker uniquement la source unique
    
    return sources

#4. Supprimer un document de la base de données vectorielle
def delete_document(vectorstore, document_name):
    collection = vectorstore.get()
    ids_to_remove = []

    for i, metadata in enumerate(collection.get("metadatas", [])):
        if metadata and metadata.get("source") == document_name:
            ids_to_remove.append(collection["ids"][i])

    if ids_to_remove:
        vectorstore.delete(ids=ids_to_remove)
        print(f"Document {document_name} supprimé de la base vectorielle.")
    else:
        print(f"Aucun document nommé {document_name} trouvé.")


#print(get_existing_documents(VECTORSTORE))
#delete_document(VECTORSTORE, "data/Jumbo/Jumbo.pdf")
#DOCUMENT_NAME = "data/Management/Project_Management_3.pdf"
#import_pdf_document(DOCUMENT_NAME)


#while True:
#    query = input("\nPosez votre question (ou tapez 'exit' pour quitter) : ")
#    if query.lower() == "exit":
#        print("\nFin de la session. À bientôt !")
#        break
#    response = RAG_system(query, VECTORSTORE, LLM_MODEL)
#    response = VECTORSTORE.similarity_search_with_score(query, k=4)
#    for doc, score in response:
#        print(f"Source: {doc.metadata.get('source', 'Unknown')}, Score: {score}")
#    #print("Réponse :", response)