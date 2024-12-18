from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class TestBatch(Base):
    """测试批次"""
    __tablename__ = "test_batches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    strategy_id = Column(Integer, ForeignKey('strategies.id'))
    status = Column(Enum('pending', 'running', 'completed', 'failed', name='test_batch_status'), default='pending')
    test_cases = relationship("TestCase", back_populates="batch")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TestCase(Base):
    """测试用例"""
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey('test_batches.id'))
    input_data = Column(JSON)
    expected_output = Column(JSON, nullable=True)
    actual_output = Column(JSON, nullable=True)
    status = Column(Enum('pending', 'running', 'passed', 'failed', 'error', name='test_case_status'), default='pending')
    error_message = Column(Text, nullable=True)
    execution_time = Column(Integer, nullable=True)  # 毫秒
    batch = relationship("TestBatch", back_populates="test_cases")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 