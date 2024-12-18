from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class TestCaseBase(BaseModel):
    input_data: Dict[str, Any]
    expected_output: Optional[Dict[str, Any]] = None

class TestCaseCreate(TestCaseBase):
    pass

class TestCase(TestCaseBase):
    id: int
    batch_id: int
    status: str
    actual_output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TestBatchBase(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_id: int

class TestBatchCreate(TestBatchBase):
    test_cases: List[TestCaseCreate]

class TestBatch(TestBatchBase):
    id: int
    status: str
    test_cases: List[TestCase]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TestDataGenerator(BaseModel):
    """测试数据生成器配置"""
    count: int = 10  # 生成的测试用例数量
    data_patterns: Dict[str, Dict[str, Any]] = {
        "credit_score": {
            "type": "random_int",
            "min": 300,
            "max": 850
        },
        "loan_amount": {
            "type": "random_float",
            "min": 1000,
            "max": 1000000
        },
        "annual_income": {
            "type": "random_float",
            "min": 10000,
            "max": 1000000
        }
    }
    include_edge_cases: bool = True  # 是否包含边界值测试用例

class TestReport(BaseModel):
    """测试报告"""
    batch_id: int
    summary: Dict[str, Any]
    test_cases: List[TestCase]
    statistics: Dict[str, Any]
    charts_data: Dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True 