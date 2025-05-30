# AI-Enhanced Job Description Generator (FastAPI + LangChain)

This project is a FastAPI backend that allows companies to create structured job postings and generate detailed AI-enhanced job descriptions using OpenAI and LangChain.

---

## 🚀 Features

- Create and manage companies and job postings
- Generate job descriptions with OpenAI
- Uses structured output via Pydantic schemas
- JSON-based API using FastAPI
- SQLAlchemy + Alembic for ORM and migrations

---

## 📦 Setup

```bash // zsh
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt