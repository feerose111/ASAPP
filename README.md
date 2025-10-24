# 🧠 ASAPP – AI Software Assistant Project Planner

ASAPP is an **AI-powered software assistant** that helps generate complete **project plans**, analyze **tech stacks**, and assist developers in automating project setup using intelligent language models.  
It integrates **FastAPI**, **LangChain**, **Streamlit**, and **ChromaDB** to build an interactive system for idea-to-project transformation.

---

## 🧩 Overview

**ASAPP** allows users to input project details (name, type, goals, duration, and tech preferences)  
and generates a complete **AI-driven project plan**.  
It’s designed to assist in early software planning phases, providing realistic suggestions and structured outputs.

The system also features:
- Contextual memory using **ChromaDB**
- Backend automation with **FastAPI**
- Interactive UI using **Streamlit**
- Modular architecture for easy scaling and modification

---

## ⚙️ Features

✅ AI-generated project plans based on simple input  
✅ Contextual memory for improved chat interactions  
✅ Streamlit frontend for interactive use  
✅ FastAPI backend for API routing  
✅ Config loader for environment and API keys  
✅ Organized modular architecture  

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Database / Vector Store** | ChromaDB |
| **AI / NLP** | LangChain + Hugging Face|
| **Language** | Python |
| **Environment** | Virtual Environment (.venv) |

---

## 📁 Project Structure
```
ASAPP/
│
├── backend/
│ ├── app.py
│ ├── agent/
│ ├── utils/
│ └── init.py
│
├── frontend/
│ ├── pages/
│ ├── main.py
│ └── init.py
│
├── requirements.txt
└── README.md
```

---
## 🛠️ Installation

Follow these steps to run ASAPP locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/ASAPP.git
cd ASAPP
```

### 2️⃣ Create Virtual Environment
```
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

#### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
```
Create a .env file in the project root and add:

HF_TOKEN=your_huggingface_token
BACKEND_URL=your_backend_url
```

### 5️⃣ Run Backend
```
cd ASAPP/backend
uvicorn app:app --reload
```

### 6️⃣ Run Frontend
```
cd ASAPP/frontend
streamlit run main.py
```

### 7️⃣ Access the App
```
Go to 👉 http://localhost:8501
```

### ▶️ Usage:
- Open the app in your browser.
- Enter the project name, type, goals, and tech stack.
- Click Submit to generate a complete project plan.
- Interact with the AI assistant to refine or expand your plan.
- Explore and save the generated details for your implementation.

### 📚 Learnings & Takeaways

While developing ASAPP, I learned and implemented several new skills that helped shape my AI engineering journey:

### 🧠 Technical Learnings
- Integrated LangChain for contextual AI workflows.
- Understood how to implement ChromaDB for vector-based memory.
- Built FastAPI endpoints with modular and async design.
- Connected a Streamlit frontend to backend APIs.
- Managed configuration files and dynamic environment setup.
- Structured a scalable AI-driven app with a clean architecture.

### 🚀 Personal Growth
- Strengthened understanding of prompt engineering.
- Learned how to combine LLMs with backend logic.
- Improved debugging and API integration skills.
- Enhanced ability to turn abstract ideas into real, functional systems.

### 🔮 Future Improvements
- Enable project export as JSON or PDF.
- Improve context persistence using a database backend.
- Enhance UI/UX with multi-step chat and project revision mode.

### 👨‍💻 Author
Firoj Raut

AI Engineer & Full Stack Developer

📍 Nepal

