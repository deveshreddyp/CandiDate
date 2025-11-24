import os
import csv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pdfplumber
import re
from sentence_transformers import SentenceTransformer, util

# Initialize Flask with the current folder as the root for static files
app = Flask(__name__, static_folder='../', static_url_path='/')
CORS(app, resources={r"/*": {"origins": "*"}})

DATASET_FILE = 'training_data.csv'

# Ensure feedback CSV exists
if not os.path.exists(DATASET_FILE):
    with open(DATASET_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['resume_text', 'jd_text', 'human_score'])

print("Loading ML Model...")
if os.path.exists('./fine_tuned_model'):
    print("✨ Loading CUSTOM Fine-Tuned Model...")
    model = SentenceTransformer('./fine_tuned_model')
else:
    print("Loading Standard Pre-trained Model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model Loaded Successfully!")

# --- UTILITIES ---
def clean_text(text):
    text = text.replace('/', ' ').replace('.', ' ').replace(',', ' ').replace('-', ' ')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def extract_text_from_pdf(file_storage):
    try:
        with pdfplumber.open(file_storage) as pdf:
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

def get_meaningful_keywords(text):
    basic_stops = {'and', 'the', 'to', 'of', 'in', 'for', 'with', 'a', 'an', 'as', 'at', 'by', 'on', 'or', 'is', 'it', 'be', 'are'}
    recruit_stops = {
        'experience', 'years', 'work', 'team', 'using', 'build', 'create', 'develop', 
        'project', 'application', 'performance', 'optimize', 'ensure', 'responsible', 
        'responsibilities', 'proficient', 'knowledge', 'must', 'have', 'ability', 'strong', 
        'proven', 'track', 'record', 'excellent', 'skills', 'preferred', 'qualification'
    }
    all_stops = basic_stops.union(recruit_stops)
    words = clean_text(text).split()
    return set([w for w in words if len(w) > 2 and w not in all_stops])

def redact_pii(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]', text)
    text = re.sub(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b', '[PHONE REDACTED]', text)
    return text

# --- ROUTES ---

# Serve the Frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../', 'index.html')

# Serve other static files (images, js, etc.) if they are in the root
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../', path)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files or 'jd' not in request.form:
        return jsonify({"error": "Missing data"}), 400

    file = request.files['resume']
    jd_text = request.form['jd']
    resume_text = extract_text_from_pdf(file)
    cleaned_resume = clean_text(resume_text)
    
    redacted_text = redact_pii(resume_text)
    
    if not resume_text.strip():
        return jsonify({"error": "Empty PDF"}), 400

    jd_keywords = get_meaningful_keywords(jd_text)
    matched = set()
    missing = set()
    
    for word in jd_keywords:
        if word in cleaned_resume:
            matched.add(word)
        else:
            missing.add(word)
    
    keyword_score = 0
    if len(jd_keywords) > 0:
        keyword_score = (len(matched) / len(jd_keywords)) * 100

    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(jd_text, convert_to_tensor=True)
    cosine_raw = util.cos_sim(embeddings1, embeddings2).item()
    
    scalar = 4.0 if os.path.exists('./fine_tuned_model') else 3.5
    vector_score_scaled = min(cosine_raw * scalar * 100, 100)
    
    final_score = round((vector_score_scaled * 0.4) + (keyword_score * 0.6), 1)
    status = "Shortlisted" if final_score >= 40 else "Rejected"

    return jsonify({
        "matchScore": final_score,
        "status": status,
        "redacted_resume": redacted_text[:500] + "...",
        "summary": f"Hybrid Analysis: Semantic ({int(vector_score_scaled)}%) + Keywords ({int(keyword_score)}%).",
        "matching": list(matched) if matched else ["None"],
        "missing": list(missing)[:5],
        "questions": [f"Tell me about your experience with {w}?" for w in list(missing)[:2]]
    })

@app.route('/feedback', methods=['POST'])
def save_feedback():
    if 'resume' not in request.files or 'jd' not in request.form or 'score' not in request.form:
        return jsonify({"error": "Missing feedback data"}), 400

    try:
        file = request.files['resume']
        jd_text = request.form['jd']
        score = request.form['score']

        resume_text = extract_text_from_pdf(file)
        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(jd_text)

        with open(DATASET_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([cleaned_resume, cleaned_jd, score])

        return jsonify({"message": "Training data saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)