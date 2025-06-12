from typing import Optional
from pydantic import BaseModel

class ProblemOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    problem_id: int
    code: str
    stdin: Optional[str] = ""

class SubmissionOut(BaseModel):
    id: int
    problem_id: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    status: str
    time: Optional[float] = None

    class Config:
        from_attributes = True
