from __future__ import annotations

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Session, select

from .models import Problem, Submission, get_engine
from .schemas import ProblemRead, SubmissionCreate, SubmissionRead
from .judge0 import run_code

app = FastAPI()

@app.get("/")
async def healthcheck():
    return Response(status_code=200)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",   # ← 追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session() -> Session:
    engine = get_engine()
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)

@app.get("/problems", response_model=list[ProblemRead])
async def list_problems(session: Session = Depends(get_session)):
    problems = session.exec(select(Problem)).all()
    return problems

@app.get("/problems/{problem_id}", response_model=ProblemRead)
async def get_problem(problem_id: int, session: Session = Depends(get_session)):
    problem = session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.post("/submit", response_model=SubmissionRead, status_code=201)
async def submit(
    data: SubmissionCreate,
    background: BackgroundTasks,
    session: Session = Depends(get_session),
):
    sub = Submission(problem_id=data.problem_id, code=data.code, stdin=data.stdin)
    session.add(sub)
    session.commit()
    session.refresh(sub)
    background.add_task(process_submission, sub.id)
    return sub

async def process_submission(submission_id: int) -> None:
    engine = get_engine()
    with Session(engine) as session:
        sub = session.get(Submission, submission_id)
        if not sub:
            return
        result = await run_code(sub.code, sub.stdin or "")
        sub.stdout = result.get("stdout")
        sub.stderr = result.get("stderr")
        sub.status = result.get("status")
        sub.time = result.get("time")
        session.add(sub)
        session.commit()

@app.get("/submissions/{submission_id}", response_model=SubmissionRead)
async def get_submission(submission_id: int, session: Session = Depends(get_session)):
    sub = session.get(Submission, submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub

@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
