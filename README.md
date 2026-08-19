# Financial Statement Analysis & Review

AI-powered financial statement auditing system built for the Cognizant Hackathon.

The system analyzes financial statement PDFs, performs deterministic audit checks, retrieves relevant WP-514 information using RAG, and uses Google Gemini GenAI to generate contextual explanations for audit findings.

---

## 🏗️ Architecture

```text
Financial Statement PDF
        │
        ▼
┌─────────────────────┐
│      Frontend       │
│     React + Vite    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Backend API      │
│       FastAPI       │
│      Port 8000      │
└───────┬───────┬─────┘
        │       │
        │       ▼
        │  ┌─────────────────┐
        │  │   RAG Service   │
        │  │    Port 8001    │
        │  └────────┬────────┘
        │           │
        │           ▼
        │      WP-514 Knowledge
        │
        ▼
┌─────────────────────┐
│   GenAI Service     │
│      FastAPI        │
│      Port 8002      │
│   Google Gemini     │
└─────────────────────┘
```

### Audit Flow

```text
PDF Upload
    ↓
PDF Extraction
    ↓
Normalization
    ↓
Audit Rule Engine
    ↓
Findings Generated
    ↓
RAG Retrieval
    ↓
WP-514 Context
    ↓
Gemini GenAI
    ↓
AI Explanation
    ↓
Final Audit Report
    ↓
Frontend Dashboard
```

---

# 📁 Project Structure

```text
Cognizant/
│
├── .gitignore
│
├── backend/
│   ├── api/
│   │   ├── routes_upload.py
│   │   ├── routes_status.py
│   │   ├── routes_findings.py
│   │   └── routes_report.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud.py
│   │
│   ├── dummy_data/
│   │   └── source_pdfs/
│   │
│   ├── extraction/
│   │   ├── pdf_parser.py
│   │   └── normalizer.py
│   │
│   ├── genai_services/
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── generator.py
│   │   ├── prompts.py
│   │   └── schemas.py
│   │
│   ├── integration/
│   │   └── rag_client.py
│   │
│   ├── rag-service/
│   │   ├── embeddings/
│   │   ├── ingestion/
│   │   ├── knowledge_base/
│   │   ├── retrieval/
│   │   ├── schemas/
│   │   └── vector_store/
│   │
│   ├── report/
│   │   └── report_builder.py
│   │
│   ├── rules/
│   │   ├── analytical_check.py
│   │   ├── consistency_check.py
│   │   ├── math_check.py
│   │   ├── optional_disclosure_check.py
│   │   ├── ratio_check.py
│   │   ├── spell_grammar_check.py
│   │   ├── tie_out_check.py
│   │   └── wp514_check.py
│   │
│   ├── tests/
│   ├── dummy_finstatement.db
│   ├── main.py
│   ├── pipeline.py
│   └── requirements.txt
│
├── dataset_deliverable/
│   └── Financial statement dataset
│
└── frontend/
    ├── public/
    ├── src/
    ├── package.json
    └── vite.config.js
```

---

# ⚙️ Prerequisites

Install the following:

* Python 3.10+
* Node.js 18+
* npm
* Git

---

# 🚀 Setup

## 1. Clone the Repository

```bash
git clone https://github.com/harsh0608-ai/Financial-Statement-Analysis-Review-Cognizant-Hackthon-.git
```

Then:

```bash
cd Financial-Statement-Analysis-Review-Cognizant-Hackthon-
```

---

# 🐍 Backend Setup

Create a Python virtual environment from the project root:

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

API keys are NOT included in the repository.

## Backend

Create:

```text
backend/.env
```

Use:

```text
backend/.env.example
```

as the reference for the required variables.

## GenAI

Create:

```text
backend/genai_services/.env
```

Add your own Google Gemini API key/configuration according to the GenAI service configuration.

**Never commit `.env` files or API keys to GitHub.**

---

# 🧠 RAG Service

Open a **new terminal**.

From the project root:

```bash
cd backend/rag-service
```

Activate the virtual environment if needed:

```bash
../../.venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the RAG service:

```bash
uvicorn app:app --reload --port 8001
```

RAG service:

```text
http://127.0.0.1:8001
```

Main endpoint:

```text
POST /retrieve
```

The RAG service retrieves relevant WP-514 information for audit findings.

---

# 🤖 GenAI Service

Open another **new terminal**.

From the project root:

```bash
cd backend/genai_services
```

Activate the virtual environment:

```bash
../../.venv/Scripts/activate
```

Start the GenAI service:

```bash
uvicorn app:app --reload --port 8002
```

GenAI service:

```text
http://127.0.0.1:8002
```

Main endpoint:

```text
POST /explain
```

The service uses Google Gemini to generate contextual explanations for audit findings.

---

# 🔧 Backend API

Open another terminal.

From the project root:

```bash
cd backend
```

Activate the virtual environment:

```bash
../.venv/Scripts/activate
```

Start the backend:

```bash
uvicorn main:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend

Open another terminal.

From the project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Vite will display the local URL, normally:

```text
http://localhost:5173
```

Open that URL in your browser.

---

# 🟢 Run the Complete System

The complete application uses four services.

## Terminal 1 — Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

## Terminal 2 — RAG

```bash
cd backend/rag-service
uvicorn app:app --reload --port 8001
```

## Terminal 3 — GenAI

```bash
cd backend/genai_services
uvicorn app:app --reload --port 8002
```

## Terminal 4 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the frontend URL shown by Vite.

---

# 📄 Using the Application

1. Start all four services.
2. Open the frontend.
3. Upload an appropriate financial statement PDF.
4. Backend receives the document.
5. PDF data is extracted and normalized.
6. Audit rules analyze the financial statement.
7. Findings are generated.
8. RAG retrieves relevant WP-514 context.
9. GenAI sends the finding and retrieved context to Gemini.
10. Gemini generates a structured explanation.
11. Backend combines the audit finding with the explanation.
12. Frontend displays the final audit report.

---

# 🔍 Audit Checks

The backend contains multiple audit rule modules:

* Mathematical Accuracy
* Analytical Review
* Consistency Checks
* Ratio Analysis
* Prior Year Tie-Out
* Spelling & Grammar
* Optional Disclosure Checks
* WP-514 Checks

---

# 🧠 RAG + GenAI

The RAG and GenAI components work together as an enrichment layer.

```text
Audit Finding
      │
      ▼
Backend
      │
      ▼
RAG Service
      │
      ├── Retrieve relevant WP-514 information
      │
      ▼
GenAI Service
      │
      ├── Finding
      ├── RAG Context
      └── Prompt
      │
      ▼
Google Gemini
      │
      ▼
Structured Explanation
      │
      ▼
Backend
      │
      ▼
Frontend
```

---

# 🗄️ Database

A shared SQLite database is included:

```text
backend/dummy_finstatement.db
```

This database is committed to the repository so that team members can use the shared demo database.

---

# 📊 Dataset

The repository contains the financial statement dataset under:

```text
dataset_deliverable/
```

The dataset contains financial statement PDFs for multiple companies.

Files generally follow the naming convention:

```text
C001_current_year_FY2026.pdf
C001_signed_prior_year_FY2025.pdf
```

### Current Year

Represents the current financial year statement.

Example:

```text
C001_current_year_FY2026.pdf
```

### Signed Prior Year

Represents the signed financial statement from the previous year and can be used for prior-year comparison and tie-out analysis.

Example:

```text
C001_signed_prior_year_FY2025.pdf
```

---

# 🔌 API Endpoints

## Backend

```text
POST /upload
GET  /status/{statement_id}
GET  /findings/{statement_id}
GET  /report/{statement_id}
GET  /
```

## RAG

```text
POST /retrieve
```

## GenAI

```text
POST /explain
```

Backend Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# ⚠️ GenAI API Quota

The GenAI service depends on the Google Gemini API.

If Gemini temporarily reaches its quota or rate limit, some AI-generated explanations may fail.

The core audit engine is independent of GenAI:

```text
Deterministic Audit Engine
        │
        ├── Finding
        ├── Description
        ├── Severity
        ├── Reported Value
        ├── Expected Value
        └── Difference
                 │
                 ▼
        GenAI Enhancement
                 │
                 └── AI Explanation
```

Therefore, a temporary GenAI failure does not necessarily mean that the underlying audit finding is lost.

---

# 🔐 Security

Do NOT commit:

```text
.env
```

API keys must remain local.

The repository's `.gitignore` already excludes:

```text
.venv/
node_modules/
.env
__pycache__/
```

Each team member should create their own local `.env` files.

---

# 🛠️ Troubleshooting

## Backend does not start

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r backend/requirements.txt
```

Start:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

---

## RAG service does not start

```bash
cd backend/rag-service
pip install -r requirements.txt
uvicorn app:app --reload --port 8001
```

---

## GenAI service does not start

Check that the local GenAI `.env` is configured.

Then:

```bash
cd backend/genai_services
uvicorn app:app --reload --port 8002
```

---

## Frontend does not start

```bash
cd frontend
npm install
npm run dev
```

---

## AI explanations are missing

Check:

1. Backend is running on port `8000`.
2. RAG is running on port `8001`.
3. GenAI is running on port `8002`.
4. Gemini API configuration is present locally.
5. Gemini API quota has not been exceeded.
6. Check the GenAI terminal for errors.

---

# 👥 Team Git Workflow

Before starting new work:

```bash
git pull origin main
```

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push origin main
```

Do not commit:

```text
.env
.venv/
node_modules/
__pycache__/
```

If multiple teammates are working simultaneously, always pull the latest `main` before starting major changes.

---

# 📌 Quick Start

After cloning the repository and configuring your local environment:

### Terminal 1

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Terminal 2

```bash
cd backend/rag-service
uvicorn app:app --reload --port 8001
```

### Terminal 3

```bash
cd backend/genai_services
uvicorn app:app --reload --port 8002
```

### Terminal 4

```bash
cd frontend
npm install
npm run dev
```

Open the frontend URL shown by Vite and upload a financial statement PDF.

---

## 🎯 Project Goal

Financial Statement Analysis & Review automates key financial audit procedures by combining deterministic audit rules, WP-514 knowledge retrieval, and Generative AI explanations into a single workflow.

```text
Financial Statement
        ↓
Automated Audit
        ↓
Finding Detection
        ↓
WP-514 Retrieval
        ↓
AI Explanation
        ↓
Audit Report
```
