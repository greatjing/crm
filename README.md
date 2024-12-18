# 信贷风险策略测试平台

一个用于测试和评估信贷风险评估策略的Web应用平台。该平台允许用户创建、编辑和测试信贷风险评估策略，支持批量测试和可视化分析。

## 功能特点

- 策略管理
  - 创建和编辑风险评估策略
  - 支持SQL和Python代码编辑
  - 代码编辑器支持语法高亮和自动完成
  - 内置代码模板

- 测试功能
  - 自动生成测试数据
  - 支持批量测试
  - 实时测试进度监控
  - 边界值测试支持

- 结果分析
  - 测试结果可视化
  - 详细的统计信息
  - 多维度图表展示
  - 测试报告导出

## 技术栈

### 前端
- Vue 3
- Element Plus
- Monaco Editor
- Axios
- Vue Router

### 后端
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pandas
- Matplotlib
- Seaborn

## 快速开始

### 环境要求
- Node.js 14+
- Python 3.8+
- PostgreSQL 12+

### 安装步骤

1. 克隆仓库
```bash
git clone [repository-url]
cd crm
```

2. 安装后端依赖
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. 配置数据库
```bash
# 在 backend/.env 文件中配置数据库连接
DATABASE_URL=postgresql://postgres:postgres@localhost/credit_risk_test
```

4. 初始化数据库
```bash
python init_db.py
```

5. 启动后端服务
```bash
python run.py
```

6. 安装前端依赖
```bash
cd ../frontend
npm install
```

7. 启动前端服务
```bash
npm run serve
```

8. 访问应用
打开浏览器访问 http://localhost:8080

## 使用指南

### 创建策略
1. 点击"新建策略"按钮
2. 填写策略名称和描述
3. 编写SQL代码（用于数据查询）
4. 编写Python代码（用于风险评估）
5. 点击保存

### 运行测试
1. 在策略列表中选择要测试的策略
2. 点击"测试"按钮
3. 配置测试数据生成参数
4. 点击"生成测试数据"
5. 预览测试数据
6. 点击"运行测试"
7. 等待测试完成
8. 查看测试报告

### 查看结果
- 测试完成后可以查看：
  - 测试统计信息
  - 结果分布图
  - 风险等级分布
  - 执行时间分析
  - 详细的测试用例结果

## 项目结构

```
crm/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   ���── requirements.txt
│   └── run.py
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── views/
    │   ├── router/
    │   └── App.vue
    └── package.json
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档。

## 开发指南

### 添加新的策略模板
1. 在 `frontend/src/views/strategy/StrategyEdit.vue` 中添加模板
2. 在 `sqlTemplate` 或 `pythonTemplate` 中定义模板内容

### 自定义测试数据生成
1. 在 `backend/app/schemas/test.py` 中修改 `TestDataGenerator` 类
2. 在 `backend/app/services/test.py` 中更新 `generate_test_data` 函数

### 添加新的图表
1. 在 `backend/app/services/test.py` 中的 `generate_test_report` 函数中添加新的图表生成代码
2. 在前端 `StrategyTest.vue` 中添加对应的图表显示组件

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。 