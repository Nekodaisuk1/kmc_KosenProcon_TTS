from __future__ import annotations

import os
import httpx

JUDGE0_URL = os.getenv("JUDGE0_URL", "https://ce.judge0.com")

async def run_code(code: str, stdin: str) -> dict:
    payload = {
        "language_id": 71,  # Python 3
        "source_code": code,
        "stdin": stdin,
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{JUDGE0_URL}/submissions/?base64_encoded=false&wait=true",
            json=payload,
        )
        data = res.json()
    return {
        "stdout": data.get("stdout"),
        "stderr": data.get("stderr"),
        "status": data["status"]["description"],
        "time": data.get("time"),
    }
