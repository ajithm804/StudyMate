# StudyMate - AI-Powered NCERT Chatbot

## 📚 Overview

**StudyMate** is an open-source educational chatbot designed to help students (Classes 6-10) get direct, context-aware answers from NCERT textbooks in Science, Maths, and English. It uses advanced AI (including Google Gemini) and vector search to provide accurate, curriculum-aligned responses.

---

## 🚀 Features

- **ChatGPT-like interface** for students and teachers
- **Contextual answers** from NCERT PDFs (Classes 6-10)
- **Supports Science, Maths, English**
- **Uses FAISS for semantic search**
- **Gemini API integration** for natural answers (optional)
- **Multi-service architecture:** React frontend, Node.js backend, Python AI service
- **Easy PDF ingestion and embedding**
- **Mobile-friendly UI**

---

## 🛠 Tech Stack

- **Frontend:** React (Vite), TailwindCSS, Axios
- **Backend:** Node.js, Express.js, MongoDB (optional)
- **AI Service:** Python 3.9+, FastAPI, FAISS, LangChain, SentenceTransformers, PyPDF2, Gemini API

---

## 📂 Project Structure

```
StudyMate1/
├── ai_service/           # Python FastAPI AI service
│   ├── app.py
│   ├── model/
│   ├── data/
│   │   ├── raw_pdfs/     # Place NCERT PDFs here
│   │   ├── processed_texts/
│   │   └── vector_store/
│   └── .env
├── backend/              # Node.js Express API
│   ├── server.js
│   ├── routes/
│   ├── models/
│   ├── controllers/
│   └── .env
├── frontend/             # React + Vite frontend
│   ├── src/
│   ├── public/
│   └── .env
├── scripts/              # Utility scripts
│   ├── ingest_pdfs.py
│   ├── rebuild_embeddings.py
│   └── check_structure.py
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/studymate.git
cd StudyMate1
```

### 2. Install Python Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ai_service/requirements.txt
```

### 3. Install Node.js Dependencies

```powershell
cd backend
npm install
cd ../frontend
npm install
```

### 4. Add NCERT PDFs

Place your NCERT PDFs in:

```
ai_service/data/raw_pdfs/
```

### 5. Ingest PDFs and Build Embeddings

```powershell
cd scripts
python ingest_pdfs.py
python rebuild_embeddings.py
```

### 6. (Optional) Add Gemini API Key

Get your free key from [Google AI Studio](https://aistudio.google.com/app/apikey) and add to:

```
ai_service/.env
GEMINI_API_KEY=your_key_here
```

### 7. Start All Services

Open three terminals:

**AI Service:**
```powershell
cd ai_service
python app.py
```

**Backend:**
```powershell
cd backend
node server.js
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 💬 Usage

- Open [http://localhost:5173](http://localhost:5173) in your browser.
- Ask questions like:
  - "What did Rama Natha do?"
  - "Explain the water cycle."
  - "What are fractions?"

---

## 🧑‍💻 Development & Customization

- **Add new PDFs:** Place them in `ai_service/data/raw_pdfs/` and re-run ingestion/embedding scripts.
- **Change chunking:** Edit `model/preprocess.py` for smarter text extraction.
- **Improve answers:** Use Gemini API for natural responses, or tweak extraction logic in `response_engine.py`.

---

## 🆘 Troubleshooting

- **PDFs not found:** Ensure they are in `ai_service/data/raw_pdfs/`.
- **AI service not ready:** Run `ingest_pdfs.py` and `rebuild_embeddings.py`.
- **Gemini errors:** Check `.env` and install `google-generativeai`.
- **Port conflicts:** Kill old processes using `netstat -ano | findstr :PORT` and `taskkill /PID <PID> /F`.
- **VSCode import errors:** Select the correct interpreter (`.venv\Scripts\python.exe`).

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push and open a PR

---

## 📄 License

MIT License

---

## 🙋 FAQ

**Q: Can I use other textbooks?**  
A: Yes! Place any PDF in `raw_pdfs/` and re-ingest.

**Q: Is Gemini required?**  
A: No, but it improves answer quality.

**Q: How do I reset everything?**  
A: Delete `processed_texts/` and `vector_store/`, then re-run ingestion and embedding scripts.

---

## 📬 Contact

For help or suggestions, open an issue or email: `your@email.com`

---

Happy Learning! 🚀

