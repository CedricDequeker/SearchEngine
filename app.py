from flask import Flask, render_template, send_from_directory, request, redirect, url_for , jsonify
import json
import os
import localRAG
import time
import research

app = Flask(__name__)

# Dossier contenant les fichiers PDF
DATA_FOLDER = 'data'
HISTORY_FOLDER = "chat_history"
UPLOAD_FOLDER = 'data/temp'
os.makedirs(HISTORY_FOLDER, exist_ok=True)

# Pré-calcul du TF-IDF
index = research.load_index("data/index.json")
tfidf_index = research.calculate_tfidf(index, 6)

def generate_history_file():
    timestamp = int(time.time())
    return os.path.join(HISTORY_FOLDER, f"chat_history_{timestamp}.json")

def load_chat_history(history_file):
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            return json.load(file)
    return []

def save_to_chat_history(query, answer,history_file, document_name=None):
    chat_history = load_chat_history(history_file)
    chat_history.append({"Query": query, "Answer": answer, "Document" : document_name})
    with open(history_file, "w") as file:
        json.dump(chat_history, file, indent=4)


global HISTORY_FILE
HISTORY_FILE = generate_history_file()


@app.route('/', methods=['GET'])
def home():
    global HISTORY_FILE
    HISTORY_FILE = generate_history_file()
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def process_query():
    if request.method == 'POST':
        results = []
        query = request.form.get('query')
        results = research.search_index_tfidf(query,tfidf_index)
    return jsonify(results)
    
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot(): 
    global HISTORY_FILE
    if request.method == 'POST':
        query = request.form.get("query")
        filename = request.form.get('filePath') 
        if filename :
            answer = localRAG.RAG_system(query, localRAG.VECTORSTORE, localRAG.LLM_MODEL,document_name=filename)
            save_to_chat_history(query, answer, HISTORY_FILE, document_name=filename)
            chat_history = load_chat_history(HISTORY_FILE)
            # If the request is an AJAX request, return JSON
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(chat_history=chat_history)

        answer = localRAG.RAG_system(query, localRAG.VECTORSTORE, localRAG.LLM_MODEL)
        save_to_chat_history(query, answer, HISTORY_FILE)
        chat_history = load_chat_history(HISTORY_FILE)
        return jsonify(chat_history=chat_history)
    
    if request.method == 'GET':
        HISTORY_FILE = generate_history_file()
        filename = request.args.get('filePath')
        query = request.args.get("query")

        if query :
            answer = localRAG.RAG_system(query, localRAG.VECTORSTORE, localRAG.LLM_MODEL,document_name=filename)
            save_to_chat_history(query, answer, HISTORY_FILE, document_name=filename)
        elif filename :
            DOCUMENT_NAME = "data/" + filename
            localRAG.import_pdf_document(DOCUMENT_NAME)
        else :
            chat_history = load_chat_history(HISTORY_FILE)
            return render_template('chatbot.html', chat_history=chat_history)
        
        chat_history = load_chat_history(HISTORY_FILE)
        return render_template('chatbot.html', chat_history=chat_history, filename=filename)


@app.route('/get-history', methods=['GET'])
def get_history():
    history_files = sorted(
    [f for f in os.listdir(HISTORY_FOLDER) if f.endswith('.json')],
    key=lambda x: os.path.getmtime(os.path.join(HISTORY_FOLDER, x)),
    reverse=True
    )[:5]
    return jsonify(history_files)

@app.route('/history', methods=['POST'])
def history():
    global HISTORY_FILE
    chat_history = request.form.get("history")
    HISTORY_FILE = "chat_history\\" + chat_history
    chat = load_chat_history(HISTORY_FILE)
    filename = chat[-1].get("Document")
    return render_template('chatbot.html', chat_history=chat, filename=filename)

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    return send_from_directory('data', filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Aucun fichier reçu'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nom de fichier vide'})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({'success': True, 'file_path': f'/temp/{file.filename}'})

@app.route('/subfolders')
def get_subfolders():
    subfolders = [f.name for f in os.scandir('data') if f.is_dir()]
    subfolders = [folder for folder in subfolders if folder != 'temp']
    return jsonify(subfolders)

@app.route('/files_in_folder/<folder>')
def get_files_in_folder(folder):
    folder_path = os.path.join('data', folder)
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)

