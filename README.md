VN Infra Hybrid - AI Recruitment System 🚀

A next-generation Applicant Tracking System (ATS) that combines Local Machine Learning for privacy-first resume scoring with Cloud Generative AI for smart automation. This platform bridges the gap between traditional keyword matching and modern semantic understanding.

🌟 Key Features

🧠 Hybrid AI Engine

Local Brain (Privacy-First): Uses Sentence-BERT (Python) running locally to score resumes based on semantic meaning (e.g., knowing "Django" relates to "Python"), ensuring sensitive candidate data never leaves your server.

Cloud Brain (Generative Power): Uses Llama-3 (via Groq) or Gemini to generate creative content like interview questions, email drafts, and job descriptions.

🔄 Self-Learning (RLHF)

Feedback Loop: Includes a "human-in-the-loop" system. Recruiters can correct the AI's score manually.

Adaptive Training: These corrections are saved to a local dataset (training_data.csv) and used to retrain the model, making it smarter and more aligned with your specific hiring culture over time.

🎤 Voice Interview Mode

AI Interviewer: Auto-generates context-aware interview questions based on skills missing from the candidate's resume.

Text-to-Speech: Reads questions aloud using the browser's Speech Synthesis API.

Speech-to-Text: Allows candidates to answer verbally using the Web Speech API.

👥 Multi-User Roles

Recruiter Dashboard: Complete control center for posting jobs, viewing applications (Kanban/Table view), scheduling interviews, and analyzing skill gaps.

Candidate Portal: Dedicated login for applicants to track their status, view scores, and read recruiter notes.

📊 Advanced Analytics

Skill Gap Analysis: Visualizes the most common missing skills across all applicants.

Recruitment Funnel: Doughnut charts showing the distribution of candidates (Pending vs. Shortlisted vs. Rejected).

🛠️ Tech Stack

Component

Technology

Frontend

HTML5, CSS3 (Modern Variables), JavaScript (Vanilla ES6+)

Backend

Python 3.12, Flask (REST API)

ML Model

all-MiniLM-L6-v2 (Sentence Transformers/BERT)

Cloud AI

Groq API (Llama 3.3 70B), Google Gemini

Database

localStorage (App State), IndexedDB (File Storage), CSV (Training Data)

Visualization

Chart.js

PDF Processing

pdf.js, pdfplumber, jsPDF

🚀 Installation & Setup

1. Prerequisites

Python 3.10 or higher installed.

A modern web browser (Chrome/Edge recommended for Speech API).

2. Backend Setup

Open a terminal in the project folder:

# Install dependencies
pip install -r requirements.txt

# (Optional) Generate synthetic training data (creates 500 sample resumes)
python backend/generate_data.py

# (Optional) Train the custom model using synthetic + real feedback data
python backend/train_model.py

# Start the server
python backend/app.py


The server will start at http://127.0.0.1:5000.

3. Frontend Setup

Simply open index.html in your browser.

Note: For the best experience (especially for Voice features), use VS Code's "Live Server" extension or Python's http.server to serve the HTML file.

🤖 How to Use

Login:

Recruiter: Use code deva.

Candidate: Register a new account or use guest mode.

Configure AI: Click the ⚙️ Gear icon. Select "Groq" and paste your free API Key.

Post a Job: Go to the dashboard and create a new job opening (use AI to write the description!).

Check Resumes: Upload a PDF and paste the JD. The system calculates a Match Score (0-100%).

Analyze & Act:

View the Skill Gap Chart.

Drag candidates on the Kanban Board.

Schedule Interviews and download .ics calendar files.

Voice Interview: Click "Start Voice Interview" to have the AI conduct a verbal screening.

📂 Project Structure

/
├── index.html              # Main Frontend Application (Single Page App)
├── backend/
│   ├── app.py              # Flask API Server & PII Redaction Logic
│   ├── train_model.py      # ML Training Script (RLHF)
│   ├── generate_data.py    # Synthetic Data Generator (Faker)
│   └── fine_tuned_model/   # (Created after training)
├── requirements.txt        # Python Dependencies
├── synthetic_dataset.csv   # Generated Base Knowledge
├── training_data.csv       # Real-world Feedback Data (RLHF)
└── README.md               # This file


🎓 Academic Credits

Developed by Devesh Reddy, Nihal DR, and Tanusree Reddy as part of the VN Infra Reality initiative.
