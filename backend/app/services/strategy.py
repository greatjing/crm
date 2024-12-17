from sqlalchemy.orm import Session
from ..models.strategy import Strategy
from ..schemas.strategy import StrategyCreate, StrategyUpdate
import json
import subprocess
import tempfile
import os

def get_strategies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Strategy).offset(skip).limit(limit).all()

def get_strategy(db: Session, strategy_id: int):
    return db.query(Strategy).filter(Strategy.id == strategy_id).first()

def create_strategy(db: Session, strategy: StrategyCreate):
    db_strategy = Strategy(**strategy.dict())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

def update_strategy(db: Session, strategy_id: int, strategy: StrategyUpdate):
    db_strategy = get_strategy(db, strategy_id)
    if not db_strategy:
        return None
    
    for key, value in strategy.dict(exclude_unset=True).items():
        setattr(db_strategy, key, value)
    
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

def delete_strategy(db: Session, strategy_id: int):
    db_strategy = get_strategy(db, strategy_id)
    if not db_strategy:
        return None
    
    db.delete(db_strategy)
    db.commit()
    return db_strategy

def test_strategy(db: Session, strategy_id: int, test_data: dict):
    db_strategy = get_strategy(db, strategy_id)
    if not db_strategy:
        return None
    
    # 创建临时Python文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # 写入策略代码
        f.write(db_strategy.python_code)
        temp_file = f.name
    
    try:
        # 执行Python代码
        result = subprocess.run(
            ['python', temp_file],
            input=json.dumps(test_data),
            text=True,
            capture_output=True,
            timeout=30  # 30秒超时
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'status': 'success' if result.returncode == 0 else 'error'
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': '执行超时'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    finally:
        # 清理临时文件
        os.unlink(temp_file) 