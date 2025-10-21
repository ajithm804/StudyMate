# StudyMate - Educational Chatbot for NCERT Materials

## 🎯 Purpose
StudyMate is a browser-based educational chatbot that helps school students (Classes 6-10) get detailed, context-aware answers from NCERT textbooks in Science, Maths, and English.

## 🛠 Tech Stack

### Frontend
- React (Vite)
- TailwindCSS
- Axios

### Backend
- Node.js
- Express.js
- MongoDB (optional for chat logs)

### AI Service
- Python 3.9+
- FastAPI
- FAISS (vector search)
- LangChain
- SentenceTransformers
- PyPDF2

## 🚀 Setup Instructions

### Prerequisites
- Node.js 16+
- Python 3.9+
- MongoDB (optional)

### 1. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Runs on: http://localhost:5173

### 2. Backend Setup
```bash
cd backend
npm install
npm start
```
Runs on: http://localhost:3000

### 3. AI Service Setup
```bash
cd ai_service
pip install -r requirements.txt
python app.py
```
Runs on: http://localhost:5000

### 4. Ingest NCERT PDFs (First Time Only)
```bash
# Place your NCERT PDFs in ai_service/data/raw_pdfs/
cd scripts
python ingest_pdfs.py
python rebuild_embeddings.py
```

## 📂 Project Structure

