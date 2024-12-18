from sqlalchemy.orm import Session
from ..models.strategy import Strategy
from ..schemas.strategy import StrategyCreate, StrategyUpdate
import json
import subprocess
import tempfile
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_strategies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Strategy).offset(skip).limit(limit).all()

def get_strategy(db: Session, strategy_id: int):
    return db.query(Strategy).filter(Strategy.id == strategy_id).first()

def create_strategy(db: Session, strategy: StrategyCreate):
    logger.info(f"Creating strategy with data: {strategy.dict()}")
    db_strategy = Strategy(**strategy.dict())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    logger.info(f"Created strategy: {db_strategy.id}, sql_code: {db_strategy.sql_code}, python_code: {db_strategy.python_code}")
    return db_strategy

def update_strategy(db: Session, strategy_id: int, strategy: StrategyUpdate):
    logger.info(f"Updating strategy {strategy_id} with data: {strategy.dict()}")
    db_strategy = get_strategy(db, strategy_id)
    if not db_strategy:
        return None
    
    for key, value in strategy.dict(exclude_unset=True).items():
        setattr(db_strategy, key, value)
    
    db.commit()
    db.refresh(db_strategy)
    logger.info(f"Updated strategy: {db_strategy.id}, sql_code: {db_strategy.sql_code}, python_code: {db_strategy.python_code}")
    return db_strategy

  ## ... existing code ... 