# Online Judge MVP

This project provides a minimal online judge using FastAPI, Supabase Postgres, Render and Vercel.

## Setup Overview

1. **Create a Supabase project** and note the Postgres connection string. Enable public network access.
2. **Import this repository to Render** and deploy `online-judge-mvp/backend` as a Web Service. Set the following environment variables:
   - `DATABASE_URL` – Supabase connection string
   - `JUDGE0_URL` – `https://ce.judge0.com`
3. **Import `online-judge-mvp/frontend` to Vercel** and set `NEXT_PUBLIC_API_URL` to the Render service URL.

Supabase requires no additional schema; tables are created automatically on first launch.

## Local Development

```bash
# Backend
cd online-judge-mvp/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd ../frontend
pnpm install
pnpm dev
```

Open `http://localhost:3000` to access the app.
