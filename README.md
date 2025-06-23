# 电力市场仿真平台（Electricity Market Simulation Platform）

一个基于 FastAPI + Vue.js 的电力市场教学仿真平台，支持多种市场出清机制、实验评估、班级管理、可视化分析，适合国际化教学与实验。

---

## 🎯 项目特色
- 多种市场出清算法（统一价、pay-as-bid、固定成本、分区、补偿、风险、二阶段市场等）
- 前端可视化（Vue3 + ECharts）
- 实验评估系统（自动评分、排名、分布分析）
- 班级/用户/权限管理
- 成绩导出、实验报告生成
- 完善的 API 文档与开发者支持
- 支持 CORS，前后端分离

---

## 📁 目录结构
```
electricity-sim-platform/
├── main.py                 # FastAPI主应用
├── security.py             # JWT认证
├── start.py                # 一键启动脚本
├── serve_frontend.py       # 前端服务器
├── frontend/               # 前端界面（index.html）
├── routers/                # API路由
│   ├── auth.py             # 用户认证
│   ├── users.py            # 用户管理
│   ├── admin.py            # 管理员功能
│   ├── simulation.py       # 仿真计算
│   ├── evaluation.py       # 评估系统
│   └── classes.py          # 班级管理
├── schemas/                # 数据模型
│   ├── auths.py
│   ├── simulation.py
│   ├── evaluation.py
│   └── classes.py
├── services/               # 业务逻辑
│   ├── market_clear/       # 市场出清算法
│   └── evaluation/         # 评估服务
├── mock_data/              # 模拟数据
│   ├── scenarios.json      # 场景配置
│   ├── bids.json           # 竞价数据
│   ├── mock_users.py       # 用户数据
│   └── file_storage.py     # 文件存储
├── requirements.txt        # 依赖
├── README.md               # 项目说明（本文件）
└── ...
```

---

## 🛠️ 技术栈
- **后端**：FastAPI、Pydantic、JWT、CORS、JSON 文件存储
- **前端**：Vue.js 3、ECharts、Bootstrap 5、Axios

---

## 🚀 快速启动

### 推荐：一键启动
```bash
python start.py
```
- 自动检查/安装依赖
- 启动后端（8000端口）
- 启动前端（3000端口）
- 生成示例数据

### 手动启动
1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
2. 启动后端
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. 启动前端（新开终端）
   ```bash
   python serve_frontend.py
   ```

### 访问地址
- 前端界面：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

---

## 👤 账号说明与体验流程

### 测试账号
- 教师账号：
  - 用户名：teacher1
  - 密码：admin
  - 角色：teacher
- 学生账号：
  - 用户名：student1
  - 密码：123456
  - 角色：student

### 教师操作流程
1. 登录教师账号
2. 进入"管理面板"
3. 创建新场景
4. 创建班级并添加学生
5. 分配实验任务

### 学生操作流程
1. 登录学生账号
2. 查看"实验场景"
3. 选择场景开始实验
4. 提交竞价数据
5. 查看结果分析

---

## 🏷️ 功能说明

### 市场机制
- 统一价格（Uniform Pricing）
- Pay-as-bid
- 固定成本机制
- 区域限制机制
- 补偿机制
- 风险调整机制
- 二阶段市场

### 评估系统
- 价格得分（50%）：基于报价与出清价格的接近程度
- 利润得分（50%）：基于实际获得的利润
- 自动计算成绩、班级排名、分布分析、实验报告生成、成绩导出

### 班级与用户管理
- 教师创建/管理班级，分配实验
- 学生班级变更、个人信息维护、密码修改
- 进度监控、成绩导出

### 前端可视化
- 实时竞价、结果展示、分布图表
- 响应式设计，移动端支持

---

## 🔗 API接口（部分）

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

---

## ❓ 常见问题与高级配置

### Q: 启动时提示缺少依赖？
A: 运行 `pip install -r requirements.txt`

### Q: 前端无法连接后端？
A: 确保两个服务都在运行：
- 后端：http://localhost:8000
- 前端：http://localhost:3000

### Q: 登录出现CORS错误？
A: 用 `http://localhost:3000` 访问前端，不要直接打开HTML文件

### Q: 如何添加更多学生？
A: 编辑 `mock_data/mock_users.py` 添加用户信息

### Q: 如何创建新场景？
A: 前端管理面板或编辑 `mock_data/scenarios.json`

### Q: 端口被占用怎么办？
A: 修改端口配置：
- 后端：`uvicorn` 命令的 `--port` 参数
- 前端：`serve_frontend.py` 的 `PORT` 变量

### Q: 前端页面空白？
A: 检查浏览器控制台错误，确认前端服务正常运行，清除浏览器缓存

### Q: 依赖安装失败？
A: 升级pip，或用 `pip install -r requirements.txt --force-reinstall`

### Q: 停止服务？
A: 两个终端分别按 `Ctrl+C` 停止服务

### 高级配置
- 修改端口：
  ```python
  # serve_frontend.py
  PORT = 3001
  # 后端
  uvicorn main:app --reload --host 0.0.0.0 --port 8001
  ```
- 生产部署：
  ```bash
  pip install gunicorn
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  # Nginx 代理前端
  ```

---

## 📝 其他说明
- 支持移动端访问，响应式设计
- CORS 默认开发环境全开放，生产环境请限制来源
- 所有页面已英文化，适合国际用户
- 如需自定义功能、二次开发请参考 API 文档

---

**开始您的电力市场仿真之旅！** 🎓⚡ 