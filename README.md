# kmc_KosenProcon_TTS

This repository contains a minimal online judge prototype.

## Getting Started (without Docker)

1. **Create a Python virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r online-judge-mvp/backend/requirements.txt
   ```

2. **Install Node.js 20 and pnpm**, then install frontend dependencies:

   ```bash
   cd online-judge-mvp/frontend
   pnpm install
   ```

3. **Configure environment variables**

   ```bash
   cp online-judge-mvp/.env.example online-judge-mvp/.env
   ```
   The default settings use SQLite and access the public Judge0 API.

4. **Run the backend and worker** (in separate terminals):

   ```bash
   cd online-judge-mvp/backend
   uvicorn app.main:app --reload
   # another terminal
   python app/worker.py
   ```

5. **Run the frontend**

   ```bash
   cd online-judge-mvp/frontend
   pnpm dev
   ```

Open <http://localhost:3000> in your browser to access the application.

This setup avoids Docker and relies on SQLite, reducing disk usage by several gigabytes compared to the container-based version.

