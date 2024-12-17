from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db
from .models import strategy as models
from .schemas import strategy as schemas
from .services import strategy as strategy_service

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="信贷信用风险策略测试平台")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的HTTP方法
    allow_headers=["*"],  # 允许的HTTP头
)

@app.get("/")
def read_root():
    return {"message": "信贷信用风险策略测试平台API"}

# 策略相关的路由
@app.get("/api/strategies", response_model=List[schemas.Strategy])
def get_strategies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    strategies = strategy_service.get_strategies(db, skip=skip, limit=limit)
    return strategies

@app.get("/api/strategies/{strategy_id}", response_model=schemas.Strategy)
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = strategy_service.get_strategy(db, strategy_id)
    if strategy is None:
        raise HTTPException(status_code=404, detail="策略不存在")
    return strategy

@app.post("/api/strategies", response_model=schemas.Strategy)
def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    return strategy_service.create_strategy(db=db, strategy=strategy)

@app.put("/api/strategies/{strategy_id}", response_model=schemas.Strategy)
def update_strategy(strategy_id: int, strategy: schemas.StrategyUpdate, db: Session = Depends(get_db)):
    updated_strategy = strategy_service.update_strategy(db, strategy_id, strategy)
    if updated_strategy is None:
        raise HTTPException(status_code=404, detail="策略不存在")
    return updated_strategy

@app.delete("/api/strategies/{strategy_id}", response_model=schemas.Strategy)
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = strategy_service.delete_strategy(db, strategy_id)
    if strategy is None:
        raise HTTPException(status_code=404, detail="策略不存在")
    return strategy

@app.post("/api/strategies/{strategy_id}/test")
def test_strategy(strategy_id: int, test_data: schemas.StrategyTest, db: Session = Depends(get_db)):
    strategy = strategy_service.get_strategy(db, strategy_id)
    if strategy is None:
        raise HTTPException(status_code=404, detail="策略不存在")
    
    result = strategy_service.test_strategy(db, strategy_id, test_data.test_data)
    if result is None:
        raise HTTPException(status_code=500, detail="测试执行失败")
    return result 