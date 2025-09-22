from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
    project_name: str
    project_type: str
    duration: str
    tech_stack: str
    goals: str
    description: Optional[str] = None