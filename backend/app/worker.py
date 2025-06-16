import os
import asyncio
import httpx
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .models import Submission
from .database import Base

DATABASE_URL = os.getenv("DATABASE_URL")
JUDGE0_URL = os.getenv("JUDGE0_URL")
REDIS_URL = os.getenv("REDIS_URL")

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
redis = Redis.from_url(REDIS_URL)

async def process_submission(sub_id: int) -> None:
    async with SessionLocal() as session:
        submission = await session.get(Submission, sub_id)
        if not submission:
            return
        payload = {
            "language_id": 71,
            "source_code": submission.code,
            "stdin": submission.stdin or "",
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{JUDGE0_URL}/submissions/?base64_encoded=false", json=payload)
            token = res.json()["token"]
            result = {"status": {"id": 1}}
            while result["status"]["id"] in (1, 2):
                await asyncio.sleep(1)
                r = await client.get(f"{JUDGE0_URL}/submissions/{token}?base64_encoded=false")
                result = r.json()
        submission.stdout = result.get("stdout")
        submission.stderr = result.get("stderr")
        submission.status = result["status"]["description"]
        submission.time = result.get("time")
        await session.commit()

async def worker() -> None:
    while True:
        _, raw_id = await redis.blpop("queue:sub")
        sub_id = int(raw_id)
        try:
            await process_submission(sub_id)
        except Exception:
            async with SessionLocal() as session:
                sub = await session.get(Submission, sub_id)
                if sub:
                    sub.status = "Internal Error"
                    await session.commit()

if __name__ == "__main__":
    asyncio.run(worker())
