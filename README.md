# FastAPI RBAC Project

## Overview
A simple REST API with:
- User Registration & Login
- JWT Authentication
- Role-Based Access Control (RBAC)
- PostgreSQL (SQLModel ORM)

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL running locally

### Install

```bash
git clone <repo>
cd fastapi_rbac_project
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Configure DB
Update `.env` with your DB credentials. Create the DB manually first.

### Run the app

```bash
uvicorn app.main:app --reload
```

### API Endpoints

#### 📘 API Documentation
- GET `/docs` — API Documentation (swagger), We can test APIs directly from here. 

#### 🛡️ Auth
- POST `/v1/auth/register` — Register a new user
- POST `/v1/auth/login` — Login and receive JWT token

#### 📁 Projects
- GET `/v1/projects` — List all projects
- POST `/v1/projects` — Create a new project (admin only)
- GET `/v1/projects/{project_id}` — Get details of a specific project by ID
- PUT `/v1/projects/{project_id}` — Update a project by ID (admin only)
- DELETE `/v1/projects/{project_id}` — Delete a project by ID (admin only)

#### 👤 User Management
- GET `/v1/user/{user_id}` — Get user details by ID
- PUT `/v1/user/{user_id}` — Update user details by ID
- DELETE `/v1/user/{user_id}` — Delete user by ID (admin only)

#### ⚙️ System
- GET `/ping` — Health check endpoint (returns "pong")


## Project Quick Demonstration Video: