from __future__ import annotations

from typing import Optional
from pydantic import BaseModel

class ProblemRead(BaseModel):
    id: int
    title: str
    description: str
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None

    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    problem_id: int
    code: str
    stdin: Optional[str] = ""

class SubmissionRead(BaseModel):
    id: int
    problem_id: int
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    time: Optional[float] = None

    class Config:
        from_attributes = True
