VN Infra Hybrid - AI Recruitment System 🚀

A next-generation Applicant Tracking System (ATS) that combines Local Machine Learning for privacy-first resume scoring with Cloud Generative AI for smart automation.

🌟 Features

🧠 Hybrid AI Engine:

Local Brain: Uses Sentence-BERT (Python) to score resumes based on semantic meaning, not just keywords.

Cloud Brain: Uses Llama-3 (via Groq) or Gemini to write emails, job descriptions, and interview questions.

🔒 Privacy First: Resume parsing and scoring happen locally. Your candidate data never leaves your server for analysis.

🎤 Voice Interview Mode: Auto-generates interview questions based on missing skills and reads them aloud using browser Text-to-Speech.

🔄 Self-Learning (RLHF): Includes a "Feedback Loop" where you can correct the AI's score. The system learns from your corrections to improve over time.

📊 Analytics Dashboard: Visualizes hiring funnels and candidate distribution.

🛠️ Tech Stack

Component

Technology

Frontend

HTML5, CSS3 (Variables), JavaScript (Vanilla)

Backend

Python 3.12, Flask

ML Model

all-MiniLM-L6-v2 (Sentence Transformers)

Cloud AI

Groq API (Llama 3.3 70B), Google Gemini

Data

localStorage (App State), IndexedDB (Files), CSV (Training)

🚀 Installation & Setup

1. Prerequisites

Python 3.10 or higher installed.

A modern web browser (Chrome/Edge recommended for Speech API).

2. Backend Setup

Open a terminal in the project folder:

# Install dependencies
pip install -r requirements.txt

# (Optional) Generate synthetic training data
python backend/generate_data.py

# (Optional) Train the custom model
python backend/train_model.py

# Start the server
python backend/app.py


The server will start at http://127.0.0.1:5000.

3. Frontend Setup

Simply open index.html in your browser.

Note: For the best experience, use VS Code's "Live Server" extension to serve the HTML file.

🤖 How to Use

Login: Use the Recruiter Code: deva.

Configure AI: Click the ⚙️ Gear icon. Select "Groq" and paste your free API Key (get one from console.groq.com).

Post a Job: Go to the dashboard and create a new job opening.

Check Resumes: Go to "Resume Check", upload a PDF, and paste the JD.

Analyze: The system will give a Match Score (0-100%).

Interview: Click "Start Interview" to have the AI interview the candidate using voice.

📂 Project Structure

/
├── index.html              # Main Frontend Application
├── backend/
│   ├── app.py              # Flask API Server
│   ├── train_model.py      # ML Training Script
│   ├── generate_data.py    # Synthetic Data Generator
│   └── fine_tuned_model/   # (Created after training)
├── requirements.txt        # Python Dependencies
├── synthetic_dataset.csv   # Generated Training Data
├── training_data.csv       # Real-world Feedback Data
└── README.md               # This file


🎓 Academic Credits

Developed by Devesh Reddy, Nihal DR, and Tanusree Reddy as part of the VN Infra Reality initiative.