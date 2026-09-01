# FORGE_X AI

> AI-powered Lead Management, Lead Scoring, Sales Workflow Automation, Follow-up Management, and Sales Recommendations Platform.

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Problem Statement](#2-problem-statement)
- [3. Project Objective](#3-project-objective)
- [4. Proposed Solution](#4-proposed-solution)
- [5. Core Features](#5-core-features)
- [6. System Architecture](#6-system-architecture)
- [7. Technology Stack](#7-technology-stack)
- [8. Project Structure](#8-project-structure)
- [9. Complete Implementation Process](#9-complete-implementation-process)
- [10. Development Environment Setup](#10-development-environment-setup)
- [11. Python Virtual Environment](#11-python-virtual-environment)
- [12. Dataset Pipeline](#12-dataset-pipeline)
- [13. Data Preprocessing](#13-data-preprocessing)
- [14. Feature Engineering](#14-feature-engineering)
- [15. Machine Learning Model](#15-machine-learning-model)
- [16. Model Evaluation](#16-model-evaluation)
- [17. ML Inference](#17-ml-inference)
- [18. Backend Implementation](#18-backend-implementation)
- [19. Database Implementation](#19-database-implementation)
- [20. Authentication](#20-authentication)
- [21. Lead Management](#21-lead-management)
- [22. Follow-up Management](#22-follow-up-management)
- [23. Activity Management](#23-activity-management)
- [24. AI Recommendations](#24-ai-recommendations)
- [25. ML API Integration](#25-ml-api-integration)
- [26. Frontend Implementation](#26-frontend-implementation)
- [27. Automation](#27-automation)
- [28. API Reference](#28-api-reference)
- [29. Running the Project](#29-running-the-project)
- [30. API Testing](#30-api-testing)
- [31. Git and GitHub](#31-git-and-github)
- [32. CI/CD](#32-cicd)
- [33. Security](#33-security)
- [34. Error Handling and Debugging](#34-error-handling-and-debugging)
- [35. Current Project Status](#35-current-project-status)
- [36. Known Limitations](#36-known-limitations)
- [37. Remaining Implementation](#37-remaining-implementation)
- [38. Recommended Next Steps](#38-recommended-next-steps)
- [39. Production Readiness](#39-production-readiness)
- [40. Future Improvements](#40-future-improvements)
- [41. Development Timeline](#41-development-timeline)
- [42. Conclusion](#42-conclusion)

---

# 1. Project Overview

FORGE_X AI is an AI-assisted sales and lead management platform designed to help sales teams manage leads, analyze lead quality, predict purchase/conversion probability, manage follow-ups, record sales activities, and generate AI-assisted recommendations.

The project combines:

- Full-stack web application
- REST API backend
- Relational database
- Machine learning lead scoring
- Follow-up management
- Sales activity tracking
- AI recommendations
- Automation infrastructure
- Git/GitHub based development
- CI/CD foundation

The project is organized into separate application layers:

```text
FORGE_X AI
│
├── Frontend        (React + Vite)
├── Backend         (Flask REST API)
├── AI/ML Engine    (scikit-learn pipeline)
├── Database        (SQLite + Alembic migrations)
├── Automation      (APScheduler scaffold)
├── Integrations    (CRM, email, external API scaffolds)
└── DevOps / CI/CD  (GitHub Actions scaffold)
```

**Author:** Laksari Naik M
**License:** MIT
**Repository:** [github.com/LaksariNaikM2005/Forgex-AI-](https://github.com/LaksariNaikM2005/Forgex-AI-)

---

# 2. Problem Statement

Sales teams face critical challenges:

1. **Manual lead prioritization** — sales representatives spend significant time evaluating which leads to pursue, often relying on intuition rather than data
2. **Inconsistent follow-up** — without automated tracking, high-value opportunities are missed or contacted too late
3. **No data-driven scoring** — most CRM systems store lead data but do not provide quantitative scoring based on historical win/loss patterns
4. **Lack of actionable intelligence** — sales managers cannot easily identify which leads are most likely to convert
5. **Fragmented workflow** — activities, follow-ups, and recommendations are tracked in separate tools instead of one unified platform

---

# 3. Project Objective

1. Build a REST API backend for complete lead lifecycle management with JWT-based authentication
2. Design and implement a complete ML pipeline: raw data → preprocessing → feature engineering → model training → evaluation → inference
3. Train a Random Forest classifier on historical sales pipeline data to predict deal outcomes (Won/Lost)
4. Integrate ML predictions directly into the lead creation API so every new lead receives an automatic `lead_score` and `purchase_probability`
5. Provide rule-based AI recommendations using lead scores, pipeline stage, and deal status
6. Track all sales activities and follow-ups per lead with full CRUD operations
7. Scaffold a React + Vite frontend for future UI development
8. Implement database schema versioning with Alembic migrations
9. Set up project infrastructure for automation, integrations, testing, and CI/CD

---

# 4. Proposed Solution

FORGE_X AI addresses the problem through a three-layer intelligent CRM:

### Layer 1 — Data Management

- Lead CRUD operations (create, read, update, delete)
- Activity logging (calls, emails, meetings)
- Follow-up scheduling and tracking
- User authentication and role management

### Layer 2 — Machine Learning

- Historical sales data preprocessing (8,801 sales opportunities)
- Temporal feature engineering with data leakage prevention
- Random Forest classification model for Win/Loss prediction
- Real-time inference on lead creation producing `lead_score` (0–100) and `purchase_probability` (0.0–1.0)

### Layer 3 — Intelligent Recommendations

- Rule-based AI recommendation engine
- Recommendations based on ML scores, pipeline stage, and deal status
- Priority classification (High / Medium / Low)
- Linkage between recommendations and follow-up actions

### Complete ML Flow

```text
POST /api/leads (create lead)
    │
    ├── Insert lead into database (flush, no commit)
    ├── Map CRM fields → 26 ML features (build_ml_input)
    ├── Load trained Random Forest model
    ├── Run predict_proba() → purchase_probability
    ├── Calculate lead_score = probability × 100
    ├── Save lead_score + purchase_probability to lead record
    └── Commit entire transaction atomically
```

---

# 5. Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| User Registration & Login | Secure auth with Werkzeug password hashing and JWT tokens | 🟢 Complete |
| Lead CRUD | Create, read, update, delete leads with auto ML scoring on creation | 🟢 Complete |
| ML Lead Scoring | Random Forest predicts `lead_score` (0–100) on lead creation | 🟢 Complete |
| Purchase Probability | ML model outputs win probability (0.0–1.0) per lead | 🟢 Complete |
| AI Recommendations | Rule-based engine using score, probability, stage, status | 🟢 Complete |
| Activity Tracking | Log calls, emails, meetings per lead | 🟢 Complete |
| Follow-up Management | Schedule, track, complete follow-ups linked to recommendations | 🟢 Complete |
| Database Migrations | Alembic-managed schema versioning with upgrade/downgrade | 🟢 Complete |
| Health Check API | `/api/health` endpoint for monitoring | 🟢 Complete |
| CORS Configuration | Frontend-backend cross-origin communication | 🟢 Complete |
| Standalone ML Predict API | `/api/ml/predict` for direct model inference | 🟢 Complete |
| Frontend UI | Dashboard, lead list, score visualization | 🔴 Not implemented |
| Automated Testing | Unit, integration, e2e tests | 🔴 Not implemented |
| CI/CD Pipeline | GitHub Actions workflows | 🔴 Not implemented |
| Docker Deployment | Docker Compose configuration | 🔴 Not implemented |

---

# 6. System Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                     FORGE_X AI ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    HTTP/JSON     ┌──────────────────────────┐ │
│  │   Frontend    │ ◄─────────────► │     Flask Backend         │ │
│  │  React + Vite │   (port 5173)   │     (port 5000)           │ │
│  │  [scaffold]   │                 │                           │ │
│  └──────────────┘                  │  Blueprints               │ │
│                                    │   ├── auth_bp             │ │
│                                    │   ├── leads_bp            │ │
│                                    │   ├── activities_bp       │ │
│                                    │   ├── recommendations_bp  │ │
│                                    │   ├── followups_bp        │ │
│                                    │   └── ml_bp               │ │
│                                    │                           │ │
│                                    │  Services                 │ │
│                                    │   ├── lead_service.py     │ │
│                                    │   └── ai_service.py       │ │
│                                    │                           │ │
│                                    │  Repositories             │ │
│                                    │   └── lead_repository.py  │ │
│                                    └──────────┬────────────────┘ │
│                                               │                  │
│                          ┌────────────────────┼───────────────┐  │
│                          ▼                    ▼               │  │
│                ┌──────────────┐    ┌──────────────────┐       │  │
│                │   SQLite DB   │    │   ML Engine       │      │  │
│                │forge_x_ai.db │    │  (scikit-learn)    │      │  │
│                │               │    │                   │      │  │
│                │ Tables:       │    │ preprocessor.py   │      │  │
│                │  • users      │    │ feature_eng.py    │      │  │
│                │  • leads      │    │ train.py          │      │  │
│                │  • activities │    │ predict.py        │      │  │
│                │  • ai_recs    │    │ evaluate.py       │      │  │
│                │  • follow_ups │    │                   │      │  │
│                └──────────────┘    └──────────────────┘       │  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Backend Layered Architecture

```text
HTTP Request
    │
    ▼
Routes (Blueprints)       ← HTTP layer, request/response handling
    │
    ▼
Services                  ← Business logic, ML integration
    │
    ▼
Repositories              ← Database operations
    │
    ▼
Models (SQLAlchemy ORM)   ← Table definitions, relationships
    │
    ▼
SQLite Database           ← Persistent storage
```

---

# 7. Technology Stack

### Backend

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Authentication | Flask-JWT-Extended |
| Password Hashing | Werkzeug |
| CORS | Flask-CORS |
| Configuration | python-dotenv |
| Production Server | Gunicorn |

### Frontend

| Component | Technology |
|-----------|-----------|
| Language | JavaScript (ES Modules) |
| Framework | React 19 |
| Build Tool | Vite 8 |
| HTTP Client | Axios 1.19 |
| Routing | React Router DOM 7 |
| Linting | ESLint |

### Machine Learning

| Component | Technology |
|-----------|-----------|
| Data Processing | Pandas, NumPy |
| ML Framework | scikit-learn |
| Algorithm | RandomForestClassifier |
| Feature Pipeline | ColumnTransformer, OneHotEncoder, SimpleImputer |
| Model Serialization | Joblib |

### Database

| Component | Technology |
|-----------|-----------|
| Engine | SQLite (development) |
| Schema Migrations | Alembic via Flask-Migrate |

### DevOps

| Component | Technology |
|-----------|-----------|
| Version Control | Git / GitHub |
| CI/CD | GitHub Actions (scaffold) |
| Containerization | Docker Compose (scaffold) |

---

# 8. Project Structure

```text
FORGE_X AI/
│
├── .env.example                         # Environment variable template
├── .gitignore                           # Git ignore rules
├── .dockerignore                        # Docker ignore (scaffold)
├── LICENSE                              # MIT License
├── README.md                            # This document
├── docker-compose.yml                   # Docker Compose (scaffold)
│
├── backend/                             # Flask REST API
│   ├── run.py                           # Application entry point
│   ├── requirements.txt                 # Python dependencies
│   └── app/
│       ├── __init__.py                  # Flask app factory
│       ├── config.py                    # Configuration (env, DB URI, JWT)
│       ├── extensions.py                # SQLAlchemy, Migrate, JWT, CORS
│       ├── models/
│       │   ├── __init__.py              # Model exports
│       │   ├── user.py                  # User model
│       │   ├── lead.py                  # Lead model (score, probability)
│       │   ├── lead_activity.py         # LeadActivity model
│       │   ├── ai_recommendation.py     # AIRecommendation model
│       │   └── follow_up_history.py     # FollowUpHistory model
│       ├── routes/
│       │   ├── auth.py                  # /api/auth/*
│       │   ├── leads.py                 # /api/leads/*
│       │   ├── activities.py            # /api/leads/<id>/activities
│       │   ├── recommendations.py       # /api/leads/<id>/recommendations
│       │   ├── followups.py             # /api/leads/<id>/followups
│       │   └── ml.py                    # /api/ml/predict
│       ├── services/
│       │   ├── lead_service.py          # Lead logic + ML integration
│       │   ├── ai_service.py            # Rule-based recommendations
│       │   └── auth_service.py          # (placeholder)
│       ├── repositories/
│       │   ├── lead_repository.py       # Lead DB operations
│       │   └── user_repository.py       # (placeholder)
│       ├── middleware/                   # (planned)
│       ├── schemas/                     # (planned for marshmallow)
│       └── utils/                       # (planned)
│
├── ai_ml_engine/                        # Machine Learning pipeline
│   ├── requirements.txt                 # ML dependencies
│   ├── data/
│   │   ├── raw/                         # Source CSV datasets
│   │   │   ├── accounts.csv             # 86 company accounts
│   │   │   ├── products.csv             # 7 product lines
│   │   │   ├── sales_pipeline.csv       # 8,801 sales opportunities
│   │   │   ├── sales_teams.csv          # 36 sales agents
│   │   │   └── metadata.csv            
│   │   └── processed/
│   │       └── training_dataset.csv     # 6,712 processed records
│   ├── preprocessing/
│   │   └── preprocessor.py             # Data cleaning and merging
│   ├── features/
│   │   └── feature_engineering.py      # ColumnTransformer pipeline
│   ├── training/
│   │   └── train.py                    # Model training (RandomForest)
│   ├── evaluation/
│   │   └── evaluate.py                 # Dataset quality report
│   ├── inference/
│   │   └── predict.py                  # Single-lead prediction
│   ├── models/
│   │   ├── lead_scoring_model.joblib            # Trained model (~8.5 MB)
│   │   ├── lead_scoring_model_api_baseline.joblib
│   │   └── lead_scoring_model_backup.joblib     # Previous backup (~30 MB)
│   ├── utils/                           # (placeholders)
│   └── notebooks/                       # (planned for EDA)
│
├── database/
│   ├── forge_x_ai.db                   # SQLite database (~72 KB)
│   ├── backups/
│   │   └── forge_x_ai_invalid_20260824.db
│   ├── migrations/
│   │   ├── alembic.ini                 # Alembic configuration
│   │   ├── env.py                      # Flask-Migrate environment
│   │   ├── script.py.mako             # Migration template
│   │   └── versions/
│   │       └── f2017afa1b1c_create_initial_database_schema.py
│   └── seed/                            # (planned for demo data)
│
├── frontend/
│   ├── package.json                    # NPM dependencies
│   ├── vite.config.js                  # Vite configuration
│   ├── index.html                      # HTML entry point
│   └── src/
│       ├── main.jsx                    # React DOM entry
│       ├── App.jsx                     # Default Vite template
│       ├── App.css / index.css         # Default styles
│       ├── assets/                     # Static images
│       ├── components/                 # (empty — planned)
│       ├── context/                    # (empty — planned)
│       ├── hooks/                      # (empty — planned)
│       ├── layouts/                    # (empty — planned)
│       ├── pages/                      # (empty — planned)
│       ├── services/                   # (empty — planned)
│       ├── styles/                     # (empty — planned)
│       └── utils/                      # (empty — planned)
│
├── automation/
│   ├── scheduler.py                    # (empty scaffold)
│   ├── requirements.txt                # APScheduler, requests
│   ├── jobs/                           # (empty)
│   ├── notifications/                  # (empty)
│   ├── utils/                          # (empty)
│   └── workers/                        # (empty)
│
├── integrations/
│   ├── requirements.txt                # (empty)
│   ├── crm/                            # (empty — planned)
│   ├── email/                          # (empty — planned)
│   ├── external_apis/                  # (empty — planned)
│   └── utils/                          # (empty)
│
├── scripts/
│   ├── health_check.py                 # (empty placeholder)
│   ├── init_db.py                      # (empty placeholder)
│   ├── seed_demo.py                    # (empty placeholder)
│   └── validate_environment.py         # (empty placeholder)
│
├── tests/
│   ├── conftest.py                     # (empty)
│   ├── api/                            # (empty)
│   ├── e2e/                            # (empty)
│   ├── integration/                    # (empty)
│   ├── ml/                             # (empty)
│   ├── performance/                    # (empty)
│   ├── security/                       # (empty)
│   └── unit/                           # (empty)
│
├── docs/
│   ├── api/                            # (empty)
│   ├── architecture/                   # (empty)
│   ├── database/                       # (empty)
│   ├── deployment/                     # (empty)
│   ├── developer/                      # (empty)
│   ├── ml/                             # (empty)
│   ├── testing/                        # (empty)
│   ├── troubleshooting/                # (empty)
│   └── user/                           # (empty)
│
└── .github/
    └── workflows/
        └── ci.yml                      # (empty — CI not configured)
```

---

# 9. Complete Implementation Process

### Phase 1 — Project Initialization (Aug 24, 2026)

1. Created GitHub repository with MIT License and `.gitignore`
2. Scaffolded the full monorepo directory structure with all subdirectories
3. Created `__init__.py` files for all Python packages
4. Initialized React + Vite frontend (`npm create vite@latest`)
5. Installed frontend dependencies: `react`, `react-dom`, `react-router-dom`, `axios`
6. Created `.env.example` with all configuration variables
7. Created `requirements.txt` files for backend, ML engine, and automation
8. Committed as `chore: initialize FORGE_X AI project` (`71c8e57`)

### Phase 2 — Backend + ML Pipeline Implementation (Aug 24–26, 2026)

1. Implemented Flask application factory pattern (`backend/app/__init__.py`)
2. Configured SQLAlchemy, JWT, CORS, and Migrate extensions
3. Created all 5 SQLAlchemy models with relationships and cascades
4. Generated Alembic migration for the initial database schema
5. Ran `flask db upgrade` to create the SQLite database
6. Implemented authentication routes: register, login, me (JWT)
7. Implemented lead CRUD with service/repository pattern
8. Implemented activity tracking routes
9. Implemented follow-up management routes with status validation
10. Implemented AI recommendation routes with rule-based engine
11. Built complete ML preprocessing pipeline (4 CSV files → merged training dataset)
12. Implemented temporal historical feature engineering with leakage prevention
13. Trained Random Forest classifier (400 trees, max_depth=12)
14. Built inference module (`predict_lead`) returning `lead_score` and `purchase_probability`
15. Integrated ML prediction into `lead_service.add_lead()` for automatic scoring
16. Created standalone ML prediction API endpoint (`/api/ml/predict`)
17. Committed as `Integrate ML lead scoring API and training pipeline` (`2136647`)

### Phase 3 — Merge and Push (Aug 26, 2026)

1. Merged development work into `main` branch
2. Pushed to GitHub remote (`origin/main`)
3. Committed as `Merge GitHub initial repository` (`6a2147b`)

### Post-Commit Changes (Uncommitted)

- Modified `backend/app/repositories/lead_repository.py` — changed from `commit()` to `flush()` for atomic ML transactions
- Modified `backend/app/services/lead_service.py` — added `build_ml_input()` and ML prediction in `add_lead()`

---

# 10. Development Environment Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Git

### Clone Repository

```bash
git clone https://github.com/LaksariNaikM2005/Forgex-AI-.git
cd "FORGE_X AI"
```

### Configure Environment

```bash
copy .env.example .env
```

Edit `.env` and set:

```env
APP_NAME=FORGE_X_AI
APP_ENV=development
DEBUG=true
HOST=127.0.0.1
PORT=5000
DATABASE_URL=sqlite:///database/forge_x_ai.db
JWT_SECRET_KEY=<your-secure-random-string>
CORS_ORIGINS=http://localhost:5173
OPENAI_API_KEY=
```

> **Important:** Replace `<your-secure-random-string>` with a strong random value. Never commit the `.env` file.

---

# 11. Python Virtual Environment

### Create and Activate

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate
```

### Install Dependencies

```bash
# Backend dependencies
pip install -r backend/requirements.txt

# ML engine dependencies
pip install -r ai_ml_engine/requirements.txt
```

### Backend Dependencies (`backend/requirements.txt`)

```text
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-CORS
Flask-JWT-Extended
marshmallow
python-dotenv
bcrypt
gunicorn
```

### ML Dependencies (`ai_ml_engine/requirements.txt`)

```text
pandas
numpy
scikit-learn
joblib
```

---

# 12. Dataset Pipeline

### Raw Data Sources

Located in `ai_ml_engine/data/raw/`:

| File | Records | Columns | Description |
|------|---------|---------|-------------|
| `accounts.csv` | 86 | 7 | Company accounts (sector, revenue, employees, location, subsidiary) |
| `products.csv` | 7 | 3 | Product catalog — GTX, MG, GTK series with sales prices |
| `sales_pipeline.csv` | 8,801 | 8 | Historical opportunities (agent, product, account, deal_stage, dates, value) |
| `sales_teams.csv` | 36 | 3 | Sales agents with manager and regional office assignments |
| `metadata.csv` | — | — | Dataset metadata |

### Sample Data

**accounts.csv:**
```csv
account,sector,year_established,revenue,employees,office_location,subsidiary_of
Acme Corporation,technolgy,1996,1100.04,2822,United States,
Betasoloin,medical,1999,251.41,495,United States,
```

**products.csv:**
```csv
product,series,sales_price
GTX Basic,GTX,550
GTX Pro,GTX,4821
GTK 500,GTK,26768
```

**sales_pipeline.csv:**
```csv
opportunity_id,sales_agent,product,account,deal_stage,engage_date,close_date,close_value
1C1I7A6R,Moses Frase,GTX Plus Basic,Cancity,Won,2016-10-20,2017-03-01,1054
```

### Processed Output

- **File:** `ai_ml_engine/data/processed/training_dataset.csv`
- **Records:** 6,712 (Won + Lost deals only)
- **Columns:** 26 features + 1 target (`target`: Won=1, Lost=0)

---

# 13. Data Preprocessing

**File:** `ai_ml_engine/preprocessing/preprocessor.py`

### Steps Executed by `build_training_dataset()`

1. **Load** 4 raw CSV files using `pd.read_csv()`
2. **Normalize** all column names to lowercase
3. **Clean** text columns — strip whitespace from all string fields
4. **Filter** sales pipeline to only Won/Lost deals
5. **Create target** — `Won → 1`, `Lost → 0`
6. **Parse** `engage_date` as datetime, drop rows with invalid dates
7. **Merge** pipeline with accounts (on `account`)
8. **Merge** with products (on `product`)
9. **Merge** with sales_teams (on `sales_agent`)
10. **Extract temporal features:**
    - `engage_year` = year of engagement
    - `engage_month` = month of engagement
    - `engage_quarter` = quarter of engagement
    - `engage_dayofweek` = day of week (0=Monday)
11. **Calculate** `account_age` = `engage_year` − `year_established`
12. **Compute temporal historical features** (see Feature Engineering)
13. **Select** 26 feature columns + target column
14. **Save** to `ai_ml_engine/data/processed/training_dataset.csv`

### Run Preprocessing

```bash
python -m ai_ml_engine.preprocessing.preprocessor
```

### Output

```text
Training dataset saved to: ai_ml_engine/data/processed/training_dataset.csv
Shape: (6712, 27)

Target distribution:
1    3864
0    2848
```

---

# 14. Feature Engineering

**File:** `ai_ml_engine/features/feature_engineering.py`

### Categorical Features (9)

| Feature | Source | Description |
|---------|--------|-------------|
| `account` | accounts.csv | Company name |
| `sector` | accounts.csv | Industry (technology, medical, retail, etc.) |
| `office_location` | accounts.csv | Country |
| `subsidiary_of` | accounts.csv | Parent company (nullable) |
| `product` | products.csv | Product name |
| `series` | products.csv | Product series (GTX, MG, GTK) |
| `sales_agent` | sales_teams.csv | Sales representative name |
| `manager` | sales_teams.csv | Team manager |
| `regional_office` | sales_teams.csv | Regional office (Central, West, East) |

### Numeric Features (17)

| Feature | Source | Description |
|---------|--------|-------------|
| `year_established` | accounts.csv | Company founding year |
| `revenue` | accounts.csv | Company revenue |
| `employees` | accounts.csv | Employee count |
| `sales_price` | products.csv | Product price |
| `engage_year` | Derived | Year of engagement |
| `engage_month` | Derived | Month of engagement |
| `engage_quarter` | Derived | Quarter of engagement |
| `engage_dayofweek` | Derived | Day of week (0=Monday) |
| `account_age` | Derived | Years since establishment |
| `historical_global_win_rate` | Derived | Smoothed global win rate (all deals before this one) |
| `historical_account_win_rate` | Derived | Smoothed win rate for this account |
| `historical_product_win_rate` | Derived | Smoothed win rate for this product |
| `historical_agent_win_rate` | Derived | Smoothed win rate for this agent |
| `historical_sector_win_rate` | Derived | Smoothed win rate for this sector |
| `account_previous_deals` | Derived | Number of prior deals for this account |
| `product_previous_deals` | Derived | Number of prior deals for this product |
| `agent_previous_deals` | Derived | Number of prior deals by this agent |

### Temporal Historical Features (Leakage Prevention)

The preprocessor computes historical win rates using **only records that occurred before** the current opportunity's engage date. This prevents data leakage from future data.

Win rates use Laplace smoothing: `(wins + 5) / (total + 10)`, defaulting to `0.5` when no prior data exists.

### scikit-learn Preprocessing Pipeline

```python
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
])

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])

preprocessor = ColumnTransformer([
    ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
    ("numeric", numeric_pipeline, NUMERIC_FEATURES),
])
```

### Run Feature Engineering Verification

```bash
python -m ai_ml_engine.features.feature_engineering
```

---

# 15. Machine Learning Model

**File:** `ai_ml_engine/training/train.py`

### Algorithm

**Random Forest Classifier** (scikit-learn)

| Hyperparameter | Value | Rationale |
|----------------|-------|-----------|
| `n_estimators` | 400 | Ensemble of 400 decision trees for stability |
| `max_depth` | 12 | Limits tree depth to prevent overfitting |
| `min_samples_split` | 8 | Minimum samples to split a node |
| `min_samples_leaf` | 4 | Minimum samples in a leaf |
| `class_weight` | `"balanced"` | Handles class imbalance (Won vs Lost) |
| `random_state` | 42 | Reproducibility |
| `n_jobs` | -1 | Use all CPU cores |

### Data Split (Chronological Temporal Split)

Records are sorted by `engage_year`, `engage_month`, `engage_dayofweek` — no random shuffling. This prevents data leakage from future deals.

| Split | Percentage | Records | Purpose |
|-------|-----------|---------|---------|
| Training | 60% | ~4,027 | Model fitting |
| Validation | 20% | ~1,343 | Hyperparameter evaluation |
| Test | 20% | ~1,342 | Final performance assessment |

### Training Pipeline

```python
pipeline = Pipeline([
    ("preprocessor", create_preprocessor()),   # ColumnTransformer
    ("model", RandomForestClassifier(
        n_estimators=400,
        max_depth=12,
        min_samples_split=8,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )),
])

pipeline.fit(X_train, y_train)
```

### Model Persistence

The trained pipeline (preprocessor + model) is saved as a single file:

```text
ai_ml_engine/models/lead_scoring_model.joblib (~8.5 MB)
```

### Run Training

```bash
python -m ai_ml_engine.training.train
```

---

# 16. Model Evaluation

**File:** `ai_ml_engine/evaluation/evaluate.py`

### Metrics Computed During Training

Both validation and test sets are evaluated with:

| Metric | Description |
|--------|-------------|
| Accuracy | Overall correct predictions |
| Precision | True positives / (True positives + False positives) |
| Recall | True positives / (True positives + False negatives) |
| F1 Score | Harmonic mean of precision and recall |
| ROC-AUC | Area under the ROC curve |

Metrics are printed to stdout during training. They are not persisted to files.

### Dataset Quality Report

The `evaluate.py` module generates:

- Dataset shape and size
- Target distribution (Won vs Lost counts and percentages)
- Missing value analysis per column
- Feature-target correlation matrix
- Duplicate row detection

### Run Evaluation Report

```bash
python -m ai_ml_engine.evaluation.evaluate
```

---

# 17. ML Inference

**File:** `ai_ml_engine/inference/predict.py`

### `predict_lead(lead_data)` Function

1. Loads the trained pipeline from `lead_scoring_model.joblib`
2. Creates a single-row DataFrame from the input dictionary
3. Fills missing feature columns with `None`
4. Reorders columns to match the 26-feature training schema
5. Runs `model.predict_proba()` → probability of "Won" class
6. Runs `model.predict()` → class label (Won/Lost)
7. Calculates `lead_score = round(probability × 100, 2)`
8. Returns:

```python
{
    "prediction": "Won" or "Lost",
    "purchase_probability": 0.7423,    # float, 4 decimals
    "lead_score": 74.23,               # probability × 100, 2 decimals
}
```

### Two Inference Paths

| Path | Trigger | Saves to DB? |
|------|---------|-------------|
| Automatic | `POST /api/leads` (via `lead_service.add_lead()`) | Yes — scores saved to lead record |
| Direct | `POST /api/ml/predict` (via `ml_bp` route) | No — returns scores only |

### Run Standalone Inference Test

```bash
python -m ai_ml_engine.inference.predict
```

---

# 18. Backend Implementation

### Application Factory

**File:** `backend/app/__init__.py`

```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register 6 blueprints: auth, leads, activities, recommendations, followups, ml

    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": app.config["APP_NAME"]}, 200

    return app
```

### Extensions

**File:** `backend/app/extensions.py`

Centralized instances of: `SQLAlchemy`, `Migrate`, `JWTManager`, `CORS`

### Configuration

**File:** `backend/app/config.py`

- Reads from `.env` via `python-dotenv`
- Database URI defaults to `sqlite:///database/forge_x_ai.db`
- JWT secret from `JWT_SECRET_KEY` env var
- CORS origins from comma-separated `CORS_ORIGINS`
- Debug mode from `DEBUG` env var

### Entry Point

**File:** `backend/run.py`

```python
app = create_app()
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
```

---

# 19. Database Implementation

### Engine

SQLite — file located at `database/forge_x_ai.db` (~72 KB)

### Schema (5 Tables)

**users:**

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| name | VARCHAR(120) | NOT NULL |
| email | VARCHAR(255) | NOT NULL, UNIQUE, INDEXED |
| password_hash | VARCHAR(255) | NOT NULL |
| role | VARCHAR(50) | NOT NULL, DEFAULT 'sales_rep' |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE |
| created_at | DATETIME | NOT NULL |
| updated_at | DATETIME | NOT NULL |

**leads:**

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| company | VARCHAR(255) | NOT NULL, INDEXED |
| contact_name | VARCHAR(120) | NULLABLE |
| email | VARCHAR(255) | NULLABLE, INDEXED |
| phone | VARCHAR(50) | NULLABLE |
| stage | VARCHAR(50) | NOT NULL, DEFAULT 'New Lead', INDEXED |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'Open', INDEXED |
| value | FLOAT | NOT NULL, DEFAULT 0.0 |
| lead_score | FLOAT | NULLABLE (ML-generated, 0–100) |
| purchase_probability | FLOAT | NULLABLE (ML-generated, 0.0–1.0) |
| last_contact_at | DATETIME | NULLABLE |
| response_time | FLOAT | NULLABLE |
| sales_cycle | FLOAT | NULLABLE |
| assigned_to | INTEGER | FK → users.id, INDEXED |
| created_at | DATETIME | NOT NULL |
| updated_at | DATETIME | NOT NULL |

**ai_recommendations:**

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| lead_id | INTEGER | NOT NULL, FK → leads.id, INDEXED |
| recommendation | TEXT | NOT NULL |
| priority | VARCHAR(50) | NOT NULL, DEFAULT 'Medium' |
| reason | TEXT | NULLABLE |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE |
| generated_at | DATETIME | NOT NULL |

**lead_activities:**

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| lead_id | INTEGER | NOT NULL, FK → leads.id, INDEXED |
| activity_type | VARCHAR(50) | NOT NULL |
| description | TEXT | NULLABLE |
| activity_at | DATETIME | NOT NULL |
| created_at | DATETIME | NOT NULL |

**follow_up_history:**

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| lead_id | INTEGER | NOT NULL, FK → leads.id, INDEXED |
| recommendation_id | INTEGER | NULLABLE, FK → ai_recommendations.id, INDEXED |
| action | VARCHAR(100) | NOT NULL |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'pending' |
| scheduled_at | DATETIME | NULLABLE |
| completed_at | DATETIME | NULLABLE |
| created_at | DATETIME | NOT NULL |

### Relationships

- `User` → one-to-many → `Lead` (via `assigned_to`)
- `Lead` → one-to-many → `LeadActivity` (cascade delete)
- `Lead` → one-to-many → `AIRecommendation` (cascade delete)
- `Lead` → one-to-many → `FollowUpHistory` (cascade delete)
- `AIRecommendation` → one-to-many → `FollowUpHistory`

### Migration

**File:** `database/migrations/versions/f2017afa1b1c_create_initial_database_schema.py`

Created: Aug 24, 2026. Creates all 5 tables with proper constraints and indexes. Supports upgrade and downgrade.

### Initialize Database

```bash
cd backend
flask db upgrade --directory ../database/migrations
```

---

# 20. Authentication

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/auth/register` | None | Create user account |
| POST | `/api/auth/login` | None | Login, receive JWT token |
| GET | `/api/auth/me` | JWT | Get current user profile |

### Registration

1. Validates required fields: `name`, `email`, `password`
2. Checks for duplicate email
3. Hashes password with `werkzeug.security.generate_password_hash()`
4. Creates user record
5. Returns user data (201)

### Login

1. Validates `email` and `password`
2. Looks up user by email
3. Verifies password with `check_password_hash()`
4. Checks `is_active` flag
5. Generates JWT: `create_access_token(identity=str(user.id))`
6. Returns `access_token` + user data (200)

### Protected Routes

All lead, activity, recommendation, and follow-up routes use `@jwt_required()`. The JWT token must be sent as `Authorization: Bearer <token>`.

### Role System

Roles stored in `users.role` (default: `sales_rep`). Role-based access control is **not enforced** at the route level yet.

---

# 21. Lead Management

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/leads` | JWT | Create lead + auto ML scoring |
| GET | `/api/leads` | JWT | List all leads |
| GET | `/api/leads/<id>` | JWT | Get single lead |
| PUT | `/api/leads/<id>` | JWT | Update lead |
| DELETE | `/api/leads/<id>` | JWT | Delete lead |

### Lead Creation Flow (with ML Integration)

**File:** `backend/app/services/lead_service.py`

```text
add_lead(data)
    │
    ├── create_lead(data)             → INSERT + flush (no commit)
    ├── build_ml_input(data)          → Map CRM fields → 26 ML features
    ├── predict_lead(ml_input)        → Load model → predict
    ├── lead.lead_score = score       → Save to record
    ├── lead.purchase_probability     → Save to record
    └── db.session.commit()           → Atomic transaction
```

If ML prediction fails: `db.session.rollback()` — the lead is NOT saved.

### Feature Mapping (`build_ml_input`)

Maps API lead data to the 26 ML features:

- `company` → `account`
- Missing engagement dates → current date defaults
- Missing historical features → smoothed defaults (0.5 win rates, 0 deal counts)

### Serialization

Every lead response includes `lead_score` and `purchase_probability` fields.

---

# 22. Follow-up Management

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/leads/<id>/followups` | JWT | Create follow-up |
| GET | `/api/leads/<id>/followups` | JWT | List follow-ups for lead |
| PUT | `/api/followups/<id>` | JWT | Update follow-up |
| DELETE | `/api/followups/<id>` | JWT | Delete follow-up |

### Features

- Required fields: `follow_up_at` (ISO 8601), `notes`
- Optional: `status` (default: `pending`), `recommendation_id`
- Status validation: only `pending`, `completed`, `cancelled` allowed
- Auto-sets `completed_at` when status changes to `completed`
- Links follow-ups to AI recommendations via `recommendation_id` FK
- ISO 8601 datetime parsing with timezone handling

---

# 23. Activity Management

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/leads/<id>/activities` | JWT | Log activity |
| GET | `/api/leads/<id>/activities` | JWT | List activities (newest first) |

### Fields

- `activity_type` (required): e.g., "call", "email", "meeting"
- `description` (optional): free-text notes
- `activity_at`: auto-set to current UTC time
- Ordered by `activity_at DESC`

---

# 24. AI Recommendations

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/leads/<id>/recommendations` | JWT | Generate recommendation |
| GET | `/api/leads/<id>/recommendations` | JWT | List recommendations |
| PUT | `/api/recommendations/<id>` | JWT | Update recommendation |
| DELETE | `/api/recommendations/<id>` | JWT | Delete recommendation |

### Rule-Based Engine

**File:** `backend/app/services/ai_service.py`

```text
IF lead_score >= 80 OR purchase_probability >= 0.80:
    → "Contact immediately, prioritize follow-up" (High)

ELIF stage contains "qualified":
    → "Schedule product demo or sales meeting" (High)

ELIF status is "won" or "closed":
    → "Maintain relationship, explore upselling" (Low)

ELIF lead_score >= 50 OR purchase_probability >= 0.50:
    → "Follow up, identify requirements" (Medium)

ELSE:
    → "Send introductory message, collect info" (Medium)
```

Recommendations include: text, priority (High/Medium/Low), reason, completed flag.

---

# 25. ML API Integration

### Backend ↔ ML Connection

**File:** `backend/app/services/lead_service.py`

The ML engine is imported directly into the backend service layer:

```python
from ai_ml_engine.inference.predict import predict_lead
```

### Automatic Scoring (on lead creation)

```python
def add_lead(data):
    lead = create_lead(data)
    ml_input = build_ml_input(data)
    prediction = predict_lead(ml_input)
    lead.lead_score = prediction["lead_score"]
    lead.purchase_probability = prediction["purchase_probability"]
    db.session.commit()
    return serialize_lead(lead)
```

### Standalone ML API

**File:** `backend/app/routes/ml.py`

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/ml/predict` | None | Direct ML prediction without saving |

```python
@ml_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    result = predict_lead(data)
    return jsonify(result), 200
```

> **Note:** `/api/ml/predict` does not require JWT authentication.

---

# 26. Frontend Implementation

### Current State: Vite Default Template (Not Customized)

The frontend was initialized with React 19 + Vite 8 but remains the default scaffold:

- `App.jsx` contains the Vite "Get Started" counter template
- No custom pages, components, services, hooks, or context providers
- Directory structure exists for future development

### Installed Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react | 19.2.8 | UI framework |
| react-dom | 19.2.8 | DOM rendering |
| react-router-dom | 7.18.2 | Client-side routing |
| axios | 1.19.0 | HTTP client |

### CORS Ready

Backend CORS is configured to accept requests from `http://localhost:5173` (Vite default).

### What Needs to Be Built

- Auth context provider (JWT token management)
- Axios API service with token interceptor
- Login / Register pages
- Lead dashboard with score visualization
- Lead detail page with activities, recommendations, follow-ups
- Routing configuration

---

# 27. Automation

### Current State: Scaffold Only

**File:** `automation/scheduler.py` — empty placeholder

### Dependencies (`automation/requirements.txt`)

```text
APScheduler
python-dotenv
requests
```

### Planned Capabilities

- Scheduled follow-up reminders
- Automated lead re-scoring
- Notification workers
- Background job processing

---

# 28. API Reference

### Health Check

| Method | Path | Auth | Response |
|--------|------|------|----------|
| GET | `/api/health` | None | `{"status": "ok", "service": "FORGE_X_AI"}` |

### Authentication

| Method | Path | Auth | Request Body | Success Response |
|--------|------|------|-------------|-----------------|
| POST | `/api/auth/register` | None | `{"name", "email", "password", "role?"}` | `201` `{"message", "user": {"id", "name", "email", "role"}}` |
| POST | `/api/auth/login` | None | `{"email", "password"}` | `200` `{"message", "access_token", "user": {…}}` |
| GET | `/api/auth/me` | JWT | — | `200` `{"id", "name", "email", "role", "is_active"}` |

### Leads

| Method | Path | Auth | Request Body | Success Response |
|--------|------|------|-------------|-----------------|
| POST | `/api/leads` | JWT | `{"company", "contact_name?", "email?", "phone?", "stage?", "status?", "value?", …}` | `201` `{"message", "lead": {…, "lead_score", "purchase_probability"}}` |
| GET | `/api/leads` | JWT | — | `200` `{"leads": [{…}]}` |
| GET | `/api/leads/<id>` | JWT | — | `200` `{"lead": {…}}` |
| PUT | `/api/leads/<id>` | JWT | `{fields to update}` | `200` `{"message", "lead": {…}}` |
| DELETE | `/api/leads/<id>` | JWT | — | `200` `{"message"}` |

### Activities

| Method | Path | Auth | Request Body | Success Response |
|--------|------|------|-------------|-----------------|
| POST | `/api/leads/<id>/activities` | JWT | `{"activity_type", "description?"}` | `201` `{"message", "activity": {…}}` |
| GET | `/api/leads/<id>/activities` | JWT | — | `200` `{"activities": [{…}]}` |

### Recommendations

| Method | Path | Auth | Request Body | Success Response |
|--------|------|------|-------------|-----------------|
| POST | `/api/leads/<id>/recommendations` | JWT | — | `201` `{"message", "recommendation": {…}}` |
| GET | `/api/leads/<id>/recommendations` | JWT | — | `200` `{"recommendations": [{…}]}` |
| PUT | `/api/recommendations/<id>` | JWT | `{fields to update}` | `200` `{"message", "recommendation": {…}}` |
| DELETE | `/api/recommendations/<id>` | JWT | — | `200` `{"message"}` |

### Follow-ups

| Method | Path | Auth | Request Body | Success Response |
|--------|------|------|-------------|-----------------|
| POST | `/api/leads/<id>/followups` | JWT | `{"follow_up_at", "notes", "status?", "recommendation_id?"}` | `201` `{"message", "followup": {…}}` |
| GET | `/api/leads/<id>/followups` | JWT | — | `200` `{"followups": [{…}]}` |
| PUT | `/api/followups/<id>` | JWT | `{fields to update}` | `200` `{"message", "followup": {…}}` |
| DELETE | `/api/followups/<id>` | JWT | — | `200` `{"message"}` |

### ML Prediction

| Method | Path | Auth | Request Body | Success Response |
|--------|------|------|-------------|-----------------|
| POST | `/api/ml/predict` | None | `{26 ML feature fields}` | `200` `{"prediction", "lead_score", "purchase_probability"}` |

---

# 29. Running the Project

### Start Backend

```bash
cd backend
python run.py
```

Server starts at `http://127.0.0.1:5000`

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Dev server starts at `http://localhost:5173`

### Run ML Pipeline

```bash
# Step 1: Preprocess raw data
python -m ai_ml_engine.preprocessing.preprocessor

# Step 2: Verify feature engineering
python -m ai_ml_engine.features.feature_engineering

# Step 3: Train model
python -m ai_ml_engine.training.train

# Step 4: Generate dataset report
python -m ai_ml_engine.evaluation.evaluate

# Step 5: Test inference
python -m ai_ml_engine.inference.predict
```

---

# 30. API Testing

### Using cURL

```bash
# 1. Register
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'

# 2. Login
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# 3. Create lead (with ML scoring)
curl -X POST http://127.0.0.1:5000/api/leads \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "company": "Acme Corporation",
    "contact_name": "John Doe",
    "email": "john@acme.com",
    "value": 5000,
    "sector": "technolgy",
    "revenue": 1100.04,
    "employees": 2822,
    "product": "GTX Basic",
    "sales_agent": "Moses Frase"
  }'

# 4. List leads
curl http://127.0.0.1:5000/api/leads \
  -H "Authorization: Bearer <TOKEN>"

# 5. Generate recommendation
curl -X POST http://127.0.0.1:5000/api/leads/1/recommendations \
  -H "Authorization: Bearer <TOKEN>"

# 6. Create follow-up
curl -X POST http://127.0.0.1:5000/api/leads/1/followups \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"follow_up_at": "2026-09-01T10:00:00Z", "notes": "Schedule product demo"}'

# 7. Log activity
curl -X POST http://127.0.0.1:5000/api/leads/1/activities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"activity_type": "call", "description": "Initial discovery call"}'

# 8. Direct ML prediction
curl -X POST http://127.0.0.1:5000/api/ml/predict \
  -H "Content-Type: application/json" \
  -d '{
    "account": "Acme Corporation",
    "sector": "technolgy",
    "year_established": 1996,
    "revenue": 1100.04,
    "employees": 2822,
    "product": "GTX Basic",
    "sales_price": 550,
    "sales_agent": "Moses Frase"
  }'

# 9. Health check
curl http://127.0.0.1:5000/api/health
```

---

# 31. Git and GitHub

### Repository

- **Remote:** `https://github.com/LaksariNaikM2005/Forgex-AI-`
- **Branch:** `main` (single branch)
- **License:** MIT

### Commit History

| Date | Hash | Message |
|------|------|---------|
| Aug 24, 2026 | `f6db84d` | Initial commit (`.gitignore`, `LICENSE`, blank `README.md`) |
| Aug 24, 2026 | `71c8e57` | chore: initialize FORGE_X AI project (full scaffold, frontend, configs) |
| Aug 26, 2026 | `2136647` | Integrate ML lead scoring API and training pipeline (backend, ML, DB) |
| Aug 26, 2026 | `6a2147b` | Merge GitHub initial repository |

### Uncommitted Changes

| File | Status |
|------|--------|
| `backend/app/repositories/lead_repository.py` | Modified (flush instead of commit) |
| `backend/app/services/lead_service.py` | Modified (added build_ml_input, ML integration) |

### Git Commands Used

```bash
git init
git add .
git commit -m "chore: initialize FORGE_X AI project"
git commit -m "Integrate ML lead scoring API and training pipeline"
git remote add origin https://github.com/LaksariNaikM2005/Forgex-AI-.git
git push -u origin main
```

---

# 32. CI/CD

### Current State: Not Configured

- `.github/workflows/ci.yml` exists but is empty
- No automated testing, linting, or deployment pipelines

### Planned Configuration

```yaml
# .github/workflows/ci.yml (planned)
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r backend/requirements.txt
      - run: pip install -r ai_ml_engine/requirements.txt
      - run: pytest tests/
```

---

# 33. Security

### Implemented

| Measure | Implementation |
|---------|---------------|
| Password hashing | `werkzeug.security.generate_password_hash` / `check_password_hash` |
| JWT authentication | Flask-JWT-Extended with Bearer tokens |
| Route protection | `@jwt_required()` on all data endpoints |
| Account status check | Login verifies `user.is_active` before token issuance |
| CORS restriction | Only `http://localhost:5173` allowed |
| `.env` in `.gitignore` | Secrets not committed to version control |
| SQL injection protection | SQLAlchemy ORM parameterized queries |

### Not Implemented

| Concern | Notes |
|---------|-------|
| JWT token expiration | Not explicitly configured (uses library defaults) |
| Token refresh | No refresh token mechanism |
| Rate limiting | No request throttling |
| Input validation schemas | Basic checks only, no marshmallow validation |
| RBAC enforcement | Roles stored but not checked at route level |
| HTTPS | Not configured (development only) |
| `/api/ml/predict` auth | ML predict endpoint has no `@jwt_required()` |
| Model integrity | No model signing or verification |

---

# 34. Error Handling and Debugging

### Error Handling Patterns

**Authentication errors:**
- Missing fields → `400` `{"error": "name, email and password are required"}`
- Duplicate email → `409` `{"error": "User with this email already exists"}`
- Bad credentials → `401` `{"error": "Invalid email or password"}`
- Inactive account → `403` `{"error": "User account is inactive"}`

**Lead errors:**
- Missing company → `400` `{"error": "company is required"}`
- Lead not found → `404` `{"error": "Lead not found"}`
- ML prediction failure → `400` (exception message)

**Follow-up errors:**
- Missing follow_up_at → `400` `{"message": "follow_up_at is required"}`
- Invalid datetime → `400` `{"message": "Invalid follow_up_at format. Use ISO 8601."}`
- Invalid status → `400` `{"message": "Invalid status", "allowed_statuses": [...]}`

**ML errors:**
- No JSON body → `400` `{"error": "JSON request body is required"}`
- Model not found → `500` `{"error": "Model not found: ..."}`

### Debugging Artifacts

| File | Indicates |
|------|-----------|
| `database/backups/forge_x_ai_invalid_20260824.db` | Database was recreated after initial invalid state |
| `backend/app/__init__.py.backup` | App factory was modified during development |
| `backend/app/routes/ml.py.backup` | ML route was modified during integration |
| `ai_ml_engine/data/processed/training_dataset_backup.csv` | Training dataset was regenerated |

---

# 35. Current Project Status

### Overall Completion: ~55%

### Status Table

| # | Component | Status | Details |
|---|-----------|--------|---------|
| 1 | Project setup | 🟢 Complete | Directory structure, configs, requirements |
| 2 | Backend API | 🟢 Complete | 6 blueprints, 18 endpoints |
| 3 | Database schema | 🟢 Complete | 5 tables, migrations, indexes |
| 4 | Authentication | 🟢 Complete | Register, login, JWT protection |
| 5 | Lead CRUD | 🟢 Complete | Full CRUD with ML auto-scoring |
| 6 | Follow-ups | 🟢 Complete | CRUD with status validation |
| 7 | Activities | 🟢 Complete | Create and list per lead |
| 8 | AI Recommendations | 🟢 Complete | Rule-based engine, CRUD |
| 9 | ML Preprocessing | 🟢 Complete | 4 CSVs → 6,712 training records |
| 10 | Feature Engineering | 🟢 Complete | 26 features, temporal leak prevention |
| 11 | ML Training | 🟢 Complete | RandomForest, temporal split, saved model |
| 12 | ML Evaluation | 🟢 Complete | Metrics on validation + test sets |
| 13 | ML Inference | 🟢 Complete | predict_lead() returns score + probability |
| 14 | Lead Scoring | 🟢 Complete | lead_score (0–100) on creation |
| 15 | Purchase Probability | 🟢 Complete | purchase_probability (0.0–1.0) on creation |
| 16 | Backend ↔ ML Integration | 🟢 Complete | Atomic transactions, feature mapping |
| 17 | ML Predict API | 🟢 Complete | Standalone /api/ml/predict |
| 18 | Frontend scaffold | 🟡 Partial | Vite + React initialized, no custom UI |
| 19 | Frontend ↔ Backend | 🔴 Not done | No API client, no pages |
| 20 | Automated testing | 🔴 Not done | Empty test directories |
| 21 | CI/CD | 🔴 Not done | Empty ci.yml |
| 22 | Docker | 🔴 Not done | Empty docker-compose.yml |
| 23 | Automation | 🔴 Not done | Empty scheduler.py |
| 24 | Integrations | 🔴 Not done | Empty CRM/email/API directories |
| 25 | Utility scripts | 🔴 Not done | Empty health_check, init_db, seed_demo |

### ML Flow Verification

```text
Create Lead → Feature Engineering → ML Prediction → lead_score → purchase_probability → Database → API Response → Frontend Display
    🟢              🟢                   🟢             🟢              🟢                 🟢          🟢             🔴
```

**Backend ML flow is COMPLETE and VERIFIED.** Frontend display is the only incomplete step.

---

# 36. Known Limitations

1. **SQLite** is not suitable for production — does not support concurrent writes
2. **ML model loaded per request** — no caching, loads `.joblib` file on every prediction
3. **No API pagination** — `GET /api/leads` returns all leads
4. **No request validation schemas** — basic field checks only
5. **ML predict endpoint is unauthenticated** — `/api/ml/predict` has no JWT requirement
6. **Frontend is default template** — no custom UI
7. **No automated tests** — zero test coverage
8. **Uncommitted changes** — critical ML integration code not committed to Git
9. **No logging** — no structured logging configured
10. **Model metrics not persisted** — evaluation results printed to stdout only

---

# 37. Remaining Implementation

### High Priority

- [ ] Build frontend auth flow (login, register, JWT storage)
- [ ] Build lead dashboard with score/probability display
- [ ] Write automated tests (pytest)
- [ ] Add `@jwt_required()` to `/api/ml/predict`
- [ ] Commit uncommitted ML integration code

### Medium Priority

- [ ] Add marshmallow request validation schemas
- [ ] Add API pagination and filtering
- [ ] Configure JWT token expiration
- [ ] Add Python logging
- [ ] Cache ML model at app startup
- [ ] Create seed script with demo data

### Lower Priority

- [ ] Implement RBAC enforcement
- [ ] Configure Docker Compose
- [ ] Set up GitHub Actions CI/CD
- [ ] Build automation scheduler
- [ ] Implement external integrations

---

# 38. Recommended Next Steps

### Sprint 1: Frontend Foundation (1–2 weeks)

- Set up React Router: `/login`, `/register`, `/dashboard`, `/leads`, `/leads/:id`
- Create Axios API service with JWT interceptor
- Build auth context provider
- Implement login and registration pages
- Build lead list with score column
- Build lead detail page with activities, recommendations, follow-ups

### Sprint 2: Testing and Validation (1 week)

- Write pytest unit tests for services and repositories
- Write API integration tests for all endpoints
- Write ML pipeline tests
- Add marshmallow schemas
- Set up pytest-cov

### Sprint 3: Security and Hardening (1 week)

- Configure JWT expiration and refresh
- Secure ML endpoint
- Implement RBAC
- Add rate limiting (Flask-Limiter)
- Add structured logging

### Sprint 4: DevOps and Production (1 week)

- Docker Compose (backend, frontend, database)
- Migrate to PostgreSQL
- GitHub Actions CI/CD
- API pagination
- ML model caching

---

# 39. Production Readiness

### Score: 3/10

| Criterion | Ready | Notes |
|-----------|-------|-------|
| Core API functionality | ✅ | All endpoints working |
| ML pipeline | ✅ | Training and inference functional |
| Authentication | ⚠️ | Works but needs expiration, refresh, RBAC |
| Frontend | ❌ | No UI |
| Testing | ❌ | Zero tests |
| Error handling | ⚠️ | Basic, not standardized |
| Logging | ❌ | Not configured |
| Monitoring | ❌ | Health check only |
| CI/CD | ❌ | Not configured |
| Containerization | ❌ | Not configured |
| Database | ⚠️ | SQLite, not production-grade |
| Security | ⚠️ | ML endpoint unauthenticated |
| Performance | ⚠️ | No pagination, no model caching |

---

# 40. Future Improvements

### Short Term

- Frontend dashboard with lead scoring visualization
- Request validation with marshmallow
- API pagination, sorting, filtering
- JWT token refresh
- Role-based access control
- Comprehensive test suite

### Medium Term

- PostgreSQL migration
- Redis caching for ML model and responses
- Docker Compose deployment
- CI/CD pipeline
- Lead import/export (CSV, Excel)
- Email notification service
- Activity-based lead re-scoring

### Long Term

- Real-time updates via WebSocket
- Advanced ML models (XGBoost, LightGBM, neural networks)
- A/B testing for recommendation strategies
- LLM-powered natural language recommendations
- Multi-tenant architecture
- Kubernetes deployment
- ML experiment tracking (MLflow)
- Feature store for real-time feature serving

---

# 41. Development Timeline

| Date | Milestone |
|------|-----------|
| Aug 24, 2026 | GitHub repository created, project scaffolded |
| Aug 24, 2026 | React + Vite frontend initialized |
| Aug 24, 2026 | Database migration generated |
| Aug 24–26, 2026 | Backend API implemented (auth, leads, activities, recommendations, follow-ups) |
| Aug 24–26, 2026 | ML pipeline built (preprocessing, features, training, inference, evaluation) |
| Aug 26, 2026 | ML integrated into lead creation API |
| Aug 26, 2026 | All code pushed to GitHub |
| Aug 29, 2026 | Comprehensive README.md documentation generated |

---

# 42. Conclusion

**FORGE_X AI** is a well-architected AI-powered CRM platform with a strong backend foundation and a complete, functional ML pipeline. The core value proposition — **automatic lead scoring on creation** — is fully implemented and operational:

1. A lead is created via the API
2. The ML model (Random Forest, 400 trees, trained on 6,712 historical sales records) instantly predicts the win probability
3. The `lead_score` (0–100) and `purchase_probability` (0.0–1.0) are saved to the database in the same atomic transaction
4. Every API response includes the ML-generated scores
5. The AI recommendation engine uses these scores to generate actionable follow-up suggestions

### Strengths

- Clean layered architecture (Routes → Services → Repositories → Models)
- Proper ML integration with atomic transactions and sensible defaults
- Temporal feature engineering with data leakage prevention
- Well-designed database schema with relationships and migration support
- Extensible project structure prepared for testing, automation, and integrations

### Current Blockers

- No frontend UI — React app is still the default Vite template
- No automated tests — zero test coverage
- Uncommitted ML integration code in `lead_service.py` and `lead_repository.py`

### Most Important Next Step

> Build the frontend authentication and lead dashboard to make the ML scoring visible to end users, then write automated tests to ensure stability.

---

**FORGE_X AI** — *Turning sales data into actionable intelligence.*

*MIT License © 2026 Laksari Naik M*