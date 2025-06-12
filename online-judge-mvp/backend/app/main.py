import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from redis.asyncio import Redis

from .database import get_session, init_models
from .models import Problem, Submission
from .schemas import ProblemOut, SubmissionCreate, SubmissionOut

app = FastAPI()
redis = Redis.from_url(os.getenv("REDIS_URL"))

@app.on_event("startup")
async def startup() -> None:
    await init_models()

@app.get("/problems", response_model=list[ProblemOut])
async def list_problems(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Problem))
    return result.scalars().all()

@app.get("/problems/{problem_id}", response_model=ProblemOut)
async def get_problem(problem_id: int, session: AsyncSession = Depends(get_session)):
    problem = await session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.post("/submit", response_model=SubmissionOut, status_code=201)
async def submit(data: SubmissionCreate, session: AsyncSession = Depends(get_session)):
    sub = Submission(problem_id=data.problem_id, code=data.code, stdin=data.stdin)
    session.add(sub)
    await session.commit()
    await session.refresh(sub)
    await redis.rpush("queue:sub", sub.id)
    return sub

@app.get("/submissions/{submission_id}", response_model=SubmissionOut)
async def get_submission(submission_id: int, session: AsyncSession = Depends(get_session)):
    sub = await session.get(Submission, submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub

@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
