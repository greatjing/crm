from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取数据库URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 执行查询
result = db.execute("SELECT id, name, sql_code, python_code FROM strategies WHERE id = 3")
row = result.fetchone()

if row:
    print("\n=== 策略详情 ===")
    print(f"ID: {row[0]}")
    print(f"名称: {row[1]}")
    print("\nSQL代码:")
    print(row[2] if row[2] else "无")
    print("\nPython代码:")
    print(row[3] if row[3] else "无")
else:
    print("未找到ID为3的策略")

db.close() 