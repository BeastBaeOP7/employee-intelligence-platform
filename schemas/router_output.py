from pydantic import BaseModel
from typing import Optional 

class RouterOutput(BaseModel):
    intents: list[str]   
    employee_name: Optional[str] = None
    department_name: Optional[str] = None