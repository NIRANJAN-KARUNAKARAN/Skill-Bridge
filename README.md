SkillBridge - Setup & Reproduction Guide
==========================================================================
 
This guide explains how anyone (a teammate, evaluator, or new
contributor) can clone this repository and run the full SkillBridge
system (backend + frontend + database) locally, and where it is
deployed live.
 
--------------------------------------------------------------------------
1. PROJECT OVERVIEW
--------------------------------------------------------------------------
 
SkillBridge is an Intelligent Job Market & Skill-Gap Analysis Platform
(India vs Malaysia). It takes a candidate resume, extracts skills,
compares them against real market data, and produces a weighted
skill-gap score with job/skill recommendations.
 
--------------------------------------------------------------------------
2. TECH STACK
--------------------------------------------------------------------------
 
Backend      : Python (Flask / FastAPI / Django - specify which one)
Frontend     : (fill in - e.g. React, Vue, plain HTML/JS)
Database     : (fill in - e.g. PostgreSQL, MySQL, SQLite, MongoDB)
Hosting      : (fill in - e.g. Render, Vercel, Railway, AWS)
 
--------------------------------------------------------------------------
3. PREREQUISITES
--------------------------------------------------------------------------
 
Before starting, make sure these are installed on your machine:
 
    - Git
    - Python 3.11+ (check with: python --version)
    - Node.js + npm (only if the frontend needs it)
    - A running database instance (local or cloud), matching what is
      listed above
 
--------------------------------------------------------------------------
4. CLONE THE REPOSITORY
--------------------------------------------------------------------------
 
    git clone https://github.com/<your-username>/Skill-Bridge.git
    cd Skill-Bridge
 
--------------------------------------------------------------------------
5. BACKEND SETUP
--------------------------------------------------------------------------
 
    cd backend
    python -m venv venv
 
    # Activate virtual environment
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
 
    pip install -r requirements.txt
 
Environment variables:
    - Copy .env.example to .env
    - Fill in real values (database URL, API keys, secret keys) in
      your local .env file
    - NEVER commit the real .env file to GitHub
 
    cp .env.example .env
 
Run the backend:
 
    python app.py
    (or: flask run   /   uvicorn app:app --reload   - depending on framework)
 
The backend should now be running at, for example:
    http://localhost:5000
 
--------------------------------------------------------------------------
6. DATABASE SETUP
--------------------------------------------------------------------------
 
    - Create a local database matching the name in your .env file
    - Run migrations / schema setup script:
          python manage_db.py migrate     (adjust to your actual script)
    - (Optional) Load sample data:
          python load_sample_data.py      (adjust to your actual script)
 
--------------------------------------------------------------------------
7. FRONTEND SETUP
--------------------------------------------------------------------------
 
    cd ../frontend
    npm install
    npm start
 
The frontend should now be running at, for example:
    http://localhost:3000
 
Make sure the frontend's API base URL (in its config/.env file) points
to the backend address from Step 5.
 
--------------------------------------------------------------------------
8. RUNNING TESTS
--------------------------------------------------------------------------
 
    cd backend
    pytest
 
Tests also run automatically through CI on every push/PR
(see .github/workflows/ci.yml).
 
--------------------------------------------------------------------------
9. LIVE DEPLOYMENT
--------------------------------------------------------------------------
 
Deployed URL   : (fill in your live link once deployed)
Hosting service: (fill in - Render / Vercel / Railway / AWS etc.)
 
Deployment notes:
    - Environment variables are set directly in the hosting platform's
      dashboard (not committed to GitHub)
    - (Add any other deployment-specific notes here, e.g. build
      command, start command, auto-deploy on push to main)
 
--------------------------------------------------------------------------
10. TROUBLESHOOTING
--------------------------------------------------------------------------
 
    - "Module not found" -> Make sure virtual environment is activated
      and requirements.txt is fully installed
    - "Database connection error" -> Check .env database URL and that
      the database service is running
    - "CORS error" in frontend -> Check backend CORS settings allow the
      frontend's URL
    - Port already in use -> Change the port in .env or stop the other
      process using that port
 
--------------------------------------------------------------------------
11. PROJECT STRUCTURE REFERENCE
--------------------------------------------------------------------------
 
Skill-Bridge/
├── .github/workflows/ci.yml
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   └── tests/
├── frontend/
│   ├── package.json
│   └── src/
└── README.md
