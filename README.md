# SalesGenie AI (Forgex AI)

SalesGenie AI is an advanced agentic lead scoring, outreach generation, and sales pipeline management platform. It uses machine learning models to analyze lead engagement, predict conversion probabilities, and automate customized outreach.

---

## 🚀 Key Features

- **JWT Authentication Flow**: Secure `/auth/register`, `/auth/login`, and `/auth/me` endpoints using Flask-JWT-Extended.
- **Lead Pipeline Management**: CRUD operations on leads with stage transitions (`New Lead`, `Qualified`, `Proposal`, `Negotiation`, `Closed Won`).
- **Dynamic Lead Scoring**: Lead category segmentation (`Hot`, `Warm`, `Cold`) based on automated lead scores.
- **Machine Learning Integration**: Built-in lead conversion probability prediction powered by a Scikit-Learn `RandomForestClassifier`.
- **Real-Time KPIs**: Real-time sales metrics (Conversion Rate, Pipeline Value, Average Score, and Sales Cycle Time).

---

## 📁 Project Structure

```text
Forgex_AI/
│
├── backend/
│   ├── app.py           # Flask server, blueprints registration, and main REST endpoints
│   ├── auth_jwt.py      # JWT Auth logic (user register/login/token validation)
│   └── database.py      # SQLAlchemy models definition (User, Lead) and SQLite connection
│
├── ml_engine/
│   ├── lead_scoring.py  # RandomForestClassifier for scoring lead conversion probability
│   ├── conversation_ai.py
│   ├── outreach_gen.py
│   └── data_preprocessing.py
│
├── frontend/
│   ├── templates/       # HTML templates for the dashboard (index.html, add_lead.html)
│   └── static/          # CSS, JS, and styling assets
│
├── automation/
│   ├── crm_endpoints.py # CRM system integrations
│   └── scheduler.py     # Background task executor
│
├── requirements.txt     # Python package dependencies
└── README.md            # Project documentation (this file)
```

---

## 📊 Database Schema

The SQLite database (`sales.db`) holds two main tables managed via SQLAlchemy ORM:

### 1. `users` Table
Stores authentication details for users/agents.
- `id` (Integer, Primary Key): Unique Identifier.
- `username` (String, Unique, Index): User's handle.
- `email` (String, Unique, Index): User's email.
- `password_hash` (String): Securely hashed password.
- `created_at` (DateTime): UTC registration timestamp.

### 2. `leads` Table
Tracks sales opportunities and their scores.
- `id` (Integer, Primary Key): Unique Identifier.
- `company` (String): Company name.
- `contact` (String): Main contact person.
- `designation` (String): Contact title/designation.
- `industry` (String): Industry sector.
- `revenue` (Float): Estimated deal revenue.
- `stage` (String, Index): Pipeline stage (`New Lead`, `Qualified`, `Proposal`, `Negotiation`, `Closed Won`).
- `score` (Float): Engagement conversion score ($0-100$).
- `category` (String): Automatically computed lead category based on score:
  - **Hot**: $\ge 70$
  - **Warm**: $\ge 40$ and $< 70$
  - **Cold**: $< 40$
- `notes` (Text): Miscellaneous details.
- `created_at` (DateTime): Lead creation timestamp.

---

## 🧠 ML Lead Scoring Engine

The ML model in `ml_engine/lead_scoring.py` employs a Random Forest Classifier trained on key engagement features:
1. **Email Opens** (integer counts)
2. **Website Visits** (integer counts)
3. **Demo Requests** (binary indicator: $0$ or $1$)

It outputs a probability value which is scaled to a score between $0$ and $100$.

---

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.10+ installed.

### Setup Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/LaksariNaikM2005/SALESGENIE-AI-Forgex-AI.git
   cd SALESGENIE-AI-Forgex-AI
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python backend/app.py
   ```
   The Flask application will start on `http://127.0.0.1:5000/`.

---

## 🔌 API Reference

### 🔐 Authentication (`/auth`)
- **`POST /auth/register`**: Registers a new user.
- **`POST /auth/login`**: Authenticates credentials and returns a JWT access token.
- **`GET /auth/me`**: Fetches the authenticated user profile (requires JWT Bearer Token).

### 📈 Leads Management
- **`GET /`**: Renders dashboard UI with summary statistics.
- **`POST /add`**: Adds a new lead.
- **`POST/DELETE /delete/<lead_id>`**: Deletes a lead.
- **`POST/PUT /update_stage/<lead_id>`**: Transition lead stage.
- **`POST/PUT /update_score/<lead_id>`**: Updates a lead's score and auto-assigns lead category.
- **`GET /api/kpis`**: Returns pipeline conversion rate, pipeline value, average scores, and sales cycle metrics in JSON.
