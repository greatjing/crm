from sqlalchemy.orm import Session
import random
import time
import json
import asyncio
import os
import tempfile
import logging
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

from ..models.test import TestBatch, TestCase
from ..schemas.test import TestBatchCreate, TestDataGenerator
from .strategy import get_strategy

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_batch(db: Session, test_batch: TestBatchCreate) -> TestBatch:
    """创建测试批次"""
    logger.info(f"Creating test batch: {test_batch.dict()}")
    db_batch = TestBatch(
        name=test_batch.name,
        description=test_batch.description,
        strategy_id=test_batch.strategy_id
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    logger.info(f"Created test batch with ID: {db_batch.id}")

    # 创建测试用例
    for test_case in test_batch.test_cases:
        db_case = TestCase(
            batch_id=db_batch.id,
            input_data=test_case.input_data,
            expected_output=test_case.expected_output
        )
        db.add(db_case)
    
    db.commit()
    logger.info(f"Created {len(test_batch.test_cases)} test cases for batch {db_batch.id}")
    return db_batch

def generate_test_data(config: TestDataGenerator) -> List[Dict[str, Any]]:
    """生成测试数据"""
    test_cases = []
    
    # 生成随机测试用例
    for _ in range(config.count):
        test_case = {}
        for field, pattern in config.data_patterns.items():
            if pattern["type"] == "random_int":
                test_case[field] = random.randint(pattern["min"], pattern["max"])
            elif pattern["type"] == "random_float":
                test_case[field] = random.uniform(pattern["min"], pattern["max"])
        test_cases.append({"input_data": test_case})
    
    # 生成边界值测试用例
    if config.include_edge_cases:
        for field, pattern in config.data_patterns.items():
            # 最小值测试
            min_case = {k: random.uniform(v["min"], v["max"]) for k, v in config.data_patterns.items()}
            min_case[field] = pattern["min"]
            test_cases.append({"input_data": min_case})
            
            # 最大值测试
            max_case = {k: random.uniform(v["min"], v["max"]) for k, v in config.data_patterns.items()}
            max_case[field] = pattern["max"]
            test_cases.append({"input_data": max_case})
    
    return test_cases

async def run_test_case(db: Session, test_case: TestCase, strategy_code: str) -> None:
    """运行单个测试用例"""
    logger.info(f"Running test case {test_case.id}")
    try:
        test_case.status = 'running'
        db.commit()
        
        start_time = time.time()
        
        # 创建临时Python文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(strategy_code)
            temp_file = f.name
            logger.info(f"Created temporary file for test case {test_case.id}: {temp_file}")
        
        # 执行测试
        logger.info(f"Executing test case {test_case.id}")
        proc = await asyncio.create_subprocess_exec(
            'python', temp_file,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        input_data = json.dumps(test_case.input_data).encode()
        logger.info(f"Test case {test_case.id} input: {input_data}")
        
        stdout, stderr = await proc.communicate(input=input_data)
        execution_time = int((time.time() - start_time) * 1000)
        
        if proc.returncode == 0:
            output = stdout.decode()
            logger.info(f"Test case {test_case.id} passed. Output: {output}")
            test_case.status = 'passed'
            test_case.actual_output = json.loads(output)
        else:
            error = stderr.decode()
            logger.error(f"Test case {test_case.id} failed. Error: {error}")
            test_case.status = 'failed'
            test_case.error_message = error
        
        test_case.execution_time = execution_time
        db.commit()
        
    except Exception as e:
        logger.error(f"Error running test case {test_case.id}: {str(e)}")
        test_case.status = 'error'
        test_case.error_message = str(e)
        db.commit()
    finally:
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file)
                logger.info(f"Cleaned up temporary file for test case {test_case.id}")
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}")

async def run_test_batch(db: Session, batch_id: int) -> None:
    """运行测试批次"""
    logger.info(f"Starting test batch {batch_id}")
    batch = db.query(TestBatch).filter(TestBatch.id == batch_id).first()
    if not batch:
        logger.error(f"Test batch {batch_id} not found")
        return
    
    try:
        batch.status = 'running'
        db.commit()
        logger.info(f"Updated batch {batch_id} status to running")
        
        strategy = get_strategy(db, batch.strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {batch.strategy_id} not found")
        
        logger.info(f"Found strategy {strategy.id} for batch {batch_id}")
        
        # 并行执行测试用例
        tasks = []
        for test_case in batch.test_cases:
            task = asyncio.create_task(run_test_case(db, test_case, strategy.python_code))
            tasks.append(task)
        
        logger.info(f"Created {len(tasks)} tasks for batch {batch_id}")
        await asyncio.gather(*tasks)
        logger.info(f"Completed all tasks for batch {batch_id}")
        
        # 更新批次状态
        failed_cases = db.query(TestCase).filter(
            TestCase.batch_id == batch_id,
            TestCase.status.in_(['failed', 'error'])
        ).count()
        
        batch.status = 'failed' if failed_cases > 0 else 'completed'
        db.commit()
        logger.info(f"Updated batch {batch_id} status to {batch.status}")
        
    except Exception as e:
        logger.error(f"Error running batch {batch_id}: {str(e)}")
        batch.status = 'failed'
        db.commit()
        raise e

def generate_test_report(db: Session, batch_id: int) -> Dict[str, Any]:
    """生成测试报告"""
    logger.info(f"Generating report for batch {batch_id}")
    batch = db.query(TestBatch).filter(TestBatch.id == batch_id).first()
    if not batch:
        logger.error(f"Test batch {batch_id} not found")
        raise ValueError("Test batch not found")
    
    # 获取测试用例数据
    test_cases = db.query(TestCase).filter(TestCase.batch_id == batch_id).all()
    logger.info(f"Found {len(test_cases)} test cases for batch {batch_id}")
    
    try:
        # 创建DataFrame进行数据分析
        df_data = []
        for case in test_cases:
            case_data = {
                'status': case.status,
                'execution_time': case.execution_time if case.execution_time is not None else 0,
            }
            # 添加输出数据
            if case.actual_output:
                case_data.update({
                    'risk_level': case.actual_output.get('risk_level'),
                    'risk_score': case.actual_output.get('risk_score'),
                })
            # 添加输入数据
            if case.input_data:
                case_data.update(case.input_data)
            df_data.append(case_data)
        
        df = pd.DataFrame(df_data)
        logger.info(f"Created DataFrame with columns: {df.columns.tolist()}")
        
        # 生成统计信息
        statistics = {
            'total_cases': len(test_cases),
            'passed_cases': len([c for c in test_cases if c.status == 'passed']),
            'failed_cases': len([c for c in test_cases if c.status == 'failed']),
            'error_cases': len([c for c in test_cases if c.status == 'error']),
            'avg_execution_time': float(df['execution_time'].mean()) if len(df) > 0 else 0,
            'max_execution_time': int(df['execution_time'].max()) if len(df) > 0 else 0,
            'min_execution_time': int(df['execution_time'].min()) if len(df) > 0 else 0
        }
        
        logger.info(f"Generated statistics for batch {batch_id}: {statistics}")
        
        # 生成图表
        charts = {}
        
        # 1. 测试结果分布饼图
        if len(df) > 0:
            plt.figure(figsize=(8, 8))
            status_counts = df['status'].value_counts()
            plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
            plt.title('Test Results Distribution')
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            charts['results_distribution'] = base64.b64encode(buf.getvalue()).decode()
        
        # 2. 风险等级分布条形图
        if 'risk_level' in df.columns and len(df['risk_level'].dropna()) > 0:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x='risk_level')
            plt.title('Risk Level Distribution')
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            charts['risk_level_distribution'] = base64.b64encode(buf.getvalue()).decode()
        
        # 3. 执行时间箱线图
        if len(df) > 0 and df['execution_time'].sum() > 0:
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df, y='execution_time')
            plt.title('Execution Time Distribution')
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            charts['execution_time_distribution'] = base64.b64encode(buf.getvalue()).decode()
        
        logger.info(f"Generated charts for batch {batch_id}")
        
        return {
            'batch_id': batch_id,
            'summary': {
                'name': batch.name,
                'description': batch.description,
                'status': batch.status,
                'created_at': batch.created_at,
                'updated_at': batch.updated_at
            },
            'statistics': statistics,
            'charts_data': charts,
            'test_cases': test_cases
        }
    except Exception as e:
        logger.error(f"Error generating report for batch {batch_id}: {str(e)}")
        raise