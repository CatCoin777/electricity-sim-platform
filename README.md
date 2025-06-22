# 电力市场仿真平台

一个基于FastAPI和Vue.js的电力市场交易机制教学仿真平台，支持多种市场出清算法和实验评估功能。

## 🎯 项目特色

### ✅ 已完成的算法模块
- **A1** 统一价市场（Uniform Pricing）✅
- **A2** Pay-as-bid 出清机制 ✅
- **A3** 固定成本 + 统一价 ✅
- **A4** 固定成本 + Pay-as-bid ✅
- **A5** 分区限制（区域出清 + 网络约束）✅
- **A6** 补偿机制（Constrained-on Payments）✅
- **A7** 风险模型（不确定性处理）✅
- **A8** 二阶段市场（日前 + 实时）✅

### 🚀 新增功能
- **前端可视化界面** - Vue.js + ECharts
- **实验评估系统** - 自动评分和排名
- **班级管理系统** - 教师创建班级，分配实验
- **成绩导出功能** - 支持JSON和CSV格式
- **实时进度监控** - 教师查看学生提交进度

## 📁 项目结构

```
electricity-sim-platform/
├── main.py                 # FastAPI主应用
├── security.py            # JWT认证
├── frontend/              # 前端界面
│   └── index.html         # Vue.js单页应用
├── routers/               # API路由
│   ├── auth.py           # 用户认证
│   ├── users.py          # 用户管理
│   ├── admin.py          # 管理员功能
│   ├── simulation.py     # 仿真计算
│   ├── evaluation.py     # 评估系统
│   └── classes.py        # 班级管理
├── schemas/              # 数据模型
│   ├── auths.py         # 认证模型
│   ├── simulation.py    # 仿真模型
│   ├── evaluation.py    # 评估模型
│   └── classes.py       # 班级模型
├── services/            # 业务逻辑
│   ├── market_clear/    # 市场出清算法
│   │   ├── uniform_price.py
│   │   ├── pay_as_bid.py
│   │   ├── fixed_cost_uniform.py
│   │   ├── fixed_cost_pay_as_bid.py
│   │   ├── zone_limit_uniform.py
│   │   ├── constrained_on.py
│   │   ├── risk_adjusted_uniform.py
│   │   └── two_stage_market.py
│   └── evaluation/      # 评估服务
│       └── score_calculator.py
└── mock_data/          # 模拟数据
    ├── scenarios.json  # 场景配置
    ├── bids.json       # 竞价数据
    ├── mock_users.py   # 用户数据
    └── file_storage.py # 文件存储
```

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代Python Web框架
- **Pydantic** - 数据验证和序列化
- **JWT** - 用户认证
- **JSON文件存储** - 轻量级数据存储

### 前端
- **Vue.js 3** - 响应式前端框架
- **ECharts** - 数据可视化图表
- **Bootstrap 5** - UI组件库
- **Axios** - HTTP客户端

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install fastapi uvicorn python-jose[cryptography] python-multipart
```

### 2. 启动后端服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问前端界面
打开浏览器访问 `frontend/index.html`

### 4. 访问API文档
访问 `http://localhost:8000/docs` 查看Swagger API文档

## 👥 用户角色

### 教师功能
- 创建和管理班级
- 分配实验任务
- 设置评估标准
- 查看学生进度
- 生成实验报告
- 导出成绩数据

### 学生功能
- 查看实验任务
- 提交竞价数据
- 查看个人成绩
- 分析实验结果

## 📊 市场机制说明

### 1. 统一价格机制 (Uniform Pricing)
- 所有中标者按统一价格结算
- 价格由边际出清价格决定
- 适合竞争性市场环境

### 2. 按报价支付机制 (Pay-as-bid)
- 每个中标者按自己的报价结算
- 鼓励真实报价
- 减少市场操纵风险

### 3. 固定成本机制
- 考虑发电厂的固定成本
- 更贴近实际运营情况
- 支持成本回收

### 4. 区域限制机制
- 考虑网络约束
- 分区出清价格
- 模拟实际电力系统

### 5. 补偿机制
- 强制运行机组的补偿
- 系统安全约束
- 平衡市场效率与安全

### 6. 风险调整机制
- 考虑不确定性因素
- 概率性出清
- 风险管理

### 7. 二阶段市场
- 日前市场 + 实时市场
- 分时优化
- 更精确的调度

## 📈 评估系统

### 评分标准
- **价格得分** (50%) - 基于报价与出清价格的接近程度
- **利润得分** (50%) - 基于实际获得的利润

### 评估功能
- 自动计算学生成绩
- 班级排名统计
- 成绩分布分析
- 实验报告生成
- 数据导出功能

## 🔧 API接口

### 认证相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/users/me` - 获取用户信息

### 仿真相关
- `POST /simulation/bid` - 提交竞价
- `GET /simulation/result/{scenario_id}` - 获取出清结果

### 评估相关
- `POST /evaluation/criteria` - 设置评估标准
- `POST /evaluation/calculate/{scenario_id}` - 计算成绩
- `GET /evaluation/scores/{scenario_id}` - 获取成绩
- `GET /evaluation/report/{scenario_id}` - 生成报告
- `GET /evaluation/export/{scenario_id}` - 导出成绩

### 班级管理
- `POST /classes/create` - 创建班级
- `GET /classes/my-classes` - 获取我的班级
- `POST /classes/{class_id}/add-students` - 添加学生
- `POST /classes/{class_id}/assign-experiment` - 分配实验
- `GET /classes/{class_id}/progress` - 查看进度

## 📝 使用示例

### 1. 教师创建实验
```bash
# 1. 登录教师账户
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "teacher1", "password": "admin", "role": "teacher"}'

# 2. 创建班级
curl -X POST "http://localhost:8000/classes/create" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"class_name": "电力市场实验班", "description": "2024年春季学期"}'

# 3. 分配实验任务
curl -X POST "http://localhost:8000/classes/{class_id}/assign-experiment" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "lesson01", "mechanism_type": "uniform_price", "duration_hours": 24}'
```

### 2. 学生参与实验
```bash
# 1. 学生登录
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "123456", "role": "student"}'

# 2. 提交竞价
curl -X POST "http://localhost:8000/simulation/bid" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "lesson01", "student_id": "student1", "bid": {"offer": 50.0, "cost": 30.0, "fixed_cost": 10.0}}'

# 3. 查看结果
curl -X GET "http://localhost:8000/simulation/result/lesson01?type=uniform_price" \
  -H "Authorization: Bearer {token}"
```

## 🎨 前端界面

### 主要功能页面
1. **登录/注册** - 用户身份验证
2. **仪表板** - 概览统计信息
3. **实验场景** - 查看可用实验
4. **竞价提交** - 学生提交竞价
5. **结果分析** - 图表化结果展示
6. **管理面板** - 教师管理功能

### 可视化图表
- 出清价格分析柱状图
- 参与者收益饼图
- 成绩分布统计图
- 提交进度进度条

## 🔒 安全特性

- JWT Token认证
- 角色权限控制
- 输入数据验证
- 错误处理机制

## 📊 数据存储

- JSON文件存储（开发环境）
- 支持扩展为数据库存储
- 数据备份和恢复

## 🚀 部署建议

### 开发环境
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用Docker
docker build -t electricity-sim .
docker run -p 8000:8000 electricity-sim
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues
- 邮箱：[your-email@example.com]

---

**电力市场仿真平台** - 让电力市场教学更直观、更有效！ 