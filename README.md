# Zorvyn Finance Backend API 🚀

FastAPI backend with PostgreSQL database, user/record management, dashboard (HTML/JS), tests, and Docker support.

Repo: https://github.com/Pavan2207/finance_backend

## Quick Start (Local)

1. Clone: `git clone https://github.com/Pavan2207/finance_backend.git && cd finance_backend`
2. Start DB: `docker-compose up -d`
3. Install deps: `pip install -r requirements.txt`
4. Sample data: `python create_sample_data.py`
5. Run server: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:8000/app/static/index.html

## Vercel Deployment (Serverless)

**Note:** Serverless Postgres needed (Vercel Postgres free tier). API/DB cold starts possible.

1. Install CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`
   - Link to GitHub repo auto-detected.
   - Set `DATABASE_URL` env var (Vercel Postgres connection string).
4. vercel.json auto-configures FastAPI routes.

Endpoints:
- API: `{your-vercel-app}.vercel.app/api/v1/records`
- Dashboard: `{your-vercel-app}.vercel.app/app/static/index.html`

## Scripts
- `start.bat`: Full startup (DB + server)
- `refresh-data.bat`: Reset DB
- Tests: `pytest`

## Structure
```
app/
├── main.py          # FastAPI app
├── routers/         # API endpoints
├── models/          # SQLAlchemy
├── schemas/         # Pydantic
└── services/        # Business logic
tests/               # Pytest
static/              # Shared static
app/static/          # Dashboard
```

Built with ❤️ by BLACKBOXAI-assisted setup.

