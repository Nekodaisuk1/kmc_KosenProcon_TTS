from __future__ import annotations

import os
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, echo=False)
    return _engine

class Problem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    sample_input: str | None = None
    sample_output: str | None = None

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    problem_id: int = Field(foreign_key="problem.id")
    code: str
    stdin: str | None = None
    status: str = "Queued"
    stdout: str | None = None
    stderr: str | None = None
    time: float | None = None

def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
