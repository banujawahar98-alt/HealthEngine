# MindCare: AI-Powered Mental Health Assessment & Well-being Support Engine

> **Academic Project & Viva Demonstration Release**  
> *Important Notice: This application provides screening and well-being support only. It does not diagnose mental-health conditions or replace professional medical care.*

---

## 📌 Project Overview

**MindCare Engine** is a full-stack, production-grade web application designed for standardized mental health screening, mood tracking, AI-assisted empathetic guidance, and well-being progress analytics.

### Key Capabilities
- 📋 **Validated Assessment Engine**: Standardized PHQ-9 (Depression), GAD-7 (Anxiety), PSS-10 (Perceived Stress), and WHO-5 (Well-being) questionnaires with deterministic scoring logic.
- 🛡️ **AI Safety & Escalation Guardrails**: Automated detection of high-risk / self-harm keyword expressions with immediate LLM suppression and verified 24/7 crisis helpline escalation.
- 🤖 **MindCare AI Assistant & RAG Retrieval**: Retrieval-Augmented Generation (RAG) providing evidence-informed wellness guidance.
- 📊 **Dynamic Recharts Analytics**: Real-time charts tracking screening scores, daily mood, stress levels, energy, and sleep duration.
- 📄 **PDF Report Generation**: Downloadable screening report detailing scores, severity levels, trend summaries, and suggested next steps.
- 🔍 **Curated Knowledge Library**: Categorized articles on sleep hygiene, academic burnout, grounding techniques, and stress reduction.
- 👨‍⚕️ **Professional Directory**: Directory of licensed counselors and mental health specialists.
- ⚙️ **Admin Dashboard**: Aggregated analytics and content management for resources, assessments, and crisis helplines.
- 🔬 **Experimental ML Prediction Module**: Scikit-Learn Random Forest Classifier model evaluating well-being tiers and returning evaluation metrics.

---

## 🛠️ Architecture & Tech Stack

### Frontend
- **Framework**: React.js 18 + TypeScript + Vite
- **Routing**: React Router v6
- **Data Visualization**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios with JWT Bearer Interceptors
- **Styling**: Modern Custom CSS Design Tokens & Glassmorphism UI (Tailwind-free)

### Backend
- **Framework**: Python 3.11+ / FastAPI
- **Architecture**: Clean Layered Architecture (`Router` ➔ `Controller` ➔ `Service` ➔ `Repository` ➔ `Database`)
- **Authentication**: JWT Bearer Tokens with Passlib/Bcrypt password hashing
- **Data Engine**: Motor (Async MongoDB) with an in-memory database fallback engine for zero-dependency offline runs.
- **Reporting**: ReportLab PDF Engine
- **Machine Learning**: Scikit-Learn & NumPy

---

## 📁 Repository Structure

```text
HealthEngine/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── admin.py
│   │   │       ├── ai.py
│   │   │       ├── assessments.py
│   │   │       ├── auth.py
│   │   │       ├── crisis.py
│   │   │       ├── dashboard.py
│   │   │       ├── ml.py
│   │   │       ├── mood.py
│   │   │       ├── professionals.py
│   │   │       ├── resources.py
│   │   │       └── users.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── mongodb.py
│   │   │   ├── seed_data.py
│   │   │   └── indexes.py
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── assessment_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── ml_service.py
│   │   │   ├── mood_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── report_service.py
│   │   │   ├── safety_service.py
│   │   │   └── scoring_service.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   └── test_services.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## ⚡ Quick Start & Installation

### Option 1: Running Local Development Servers

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
*Backend runs at `http://localhost:8000`. API Docs available at `http://localhost:8000/docs`.*

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs at `http://localhost:5173`.*

---

### Option 2: Docker Compose
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

---

## 🧪 Running Automated Test Suite

Run unit and integration tests across scoring algorithms, AI safety detection, PDF generation, ML model evaluation, and RAG retrieval:

```bash
cd backend
python -m pytest
```

---

## 🔐 Security & Healthcare Guardrails

1. **Deterministic Scoring**: Questionnaire scores are calculated strictly via standard Python mathematical rules and never generated by an LLM.
2. **LLM Non-Diagnostic Scope**: Prompts strictly instruct the model to provide empathetic, educational support without diagnosing or prescribing medication.
3. **Safety Layer Suppression**: Immediate crisis phrases trigger automated safety overrides that suppress LLM completion and present verified emergency resources.
4. **Data Privacy**: Users can export their JSON data or delete their accounts at any time.

---

## 📜 License & Citation

Developed for academic presentation, project review, and viva demonstration.
