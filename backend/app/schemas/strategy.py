from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    sql_code: Optional[str] = None
    python_code: Optional[str] = None

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(StrategyBase):
    status: Optional[str] = None

class Strategy(StrategyBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class StrategyTest(BaseModel):
    test_data: dict 