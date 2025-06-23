# 电力市场仿真平台（Electricity Market Simulation Platform）

一个基于 FastAPI + Vue.js 的电力市场教学仿真平台，支持多种市场出清机制、实验评估、班级管理、可视化分析，适合国际化教学与实验。

---

## 🎯 项目特色
- 多种市场出清算法（统一价、pay-as-bid、固定成本、分区、补偿、风险、二阶段市场等）
- 现代化前端界面（Vue3 + Vue Router + ECharts）
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
├── start_platform.bat      # Windows一键启动脚本
├── start_platform.sh       # Linux/Mac一键启动脚本
├── frontend/               # Vue.js前端项目
│   ├── src/
│   │   ├── components/     # 可复用组件
│   │   │   └── Layout.vue  # 主布局组件
│   │   ├── views/          # 页面组件
│   │   │   ├── Login.vue   # 登录注册
│   │   │   ├── Dashboard.vue # 仪表板
│   │   │   ├── Scenarios.vue # 场景管理
│   │   │   ├── Bidding.vue # 竞价界面
│   │   │   ├── Results.vue # 结果分析
│   │   │   ├── Profile.vue # 个人信息
│   │   │   ├── AdminPanel.vue # 教师管理
│   │   │   └── ClassManagement.vue # 班级管理
│   │   ├── services/       # API服务
│   │   │   └── api.js      # HTTP客户端
│   │   ├── router/         # 路由配置
│   │   │   └── index.js    # 路由定义
│   │   ├── assets/         # 静态资源
│   │   │   └── main.css    # 全局样式
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 应用入口
│   ├── index.html          # HTML模板
│   ├── package.json        # 前端依赖
│   ├── vite.config.js      # Vite配置
│   └── README.md           # 前端说明
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
├── requirements.txt        # 后端依赖
├── README.md               # 项目说明（本文件）
└── ...
```

---

## 🛠️ 技术栈
- **后端**：FastAPI、Pydantic、JWT、CORS、JSON 文件存储
- **前端**：Vue.js 3、Vue Router 4、ECharts、Bootstrap 5、Axios、Vite

---

## 🚀 快速启动

### 推荐：一键启动

**Windows:**
```bash
start_platform.bat
```

**Linux/Mac:**
```bash
chmod +x start_platform.sh
./start_platform.sh
```

### 手动启动

1. **启动后端:**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **启动前端 (新开终端):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **访问平台:**
   - 前端界面：http://localhost:3000
   - 后端API：http://localhost:8000
   - API文档：http://localhost:8000/docs

---

## 👥 用户角色

### 教师账户
- 创建和管理实验场景
- 管理班级和学生
- 查看所有仿真结果
- 启动/结束实验

### 学生账户
- 加入实验场景
- 提交竞价
- 查看个人结果
- 管理个人信息

---

## 📋 使用指南

### 1. 注册/登录
- 访问 http://localhost:3000
- 注册为教师或学生
- 使用凭据登录

### 2. 教师操作

#### 创建班级
1. 进入"班级管理"
2. 点击"创建新班级"
3. 填写班级详情
4. 通过用户名添加学生

#### 创建场景
1. 进入"管理面板"
2. 填写场景详情：
   - 名称和描述
   - 需求量（最少1 MW）
   - 实验类型（开放或班级限制）
   - 持续时间
3. 点击"创建场景"

#### 启动实验
1. 在"管理面板"中找到场景
2. 点击"开始"激活
3. 学生现在可以加入和竞价

### 3. 学生操作

#### 加入场景
1. 进入"实验场景"
2. 找到活跃场景
3. 点击"加入场景"

#### 提交竞价
1. 进入"提交竞价"
2. 选择场景
3. 输入竞价价格和数量
4. 选择竞价类型（供应/需求）
5. 点击"提交竞价"

#### 查看结果
1. 进入"结果分析"
2. 选择已完成的场景
3. 查看市场出清结果和图表

---

## 🔧 核心功能

### 实时竞价
- 每个场景可提交多个竞价
- 实时价格和数量更新
- 竞价状态跟踪

### 数据可视化
- 供需曲线
- 市场出清价格分析
- 参与者表现图表

### 班级管理
- 创建和管理班级
- 添加/移除学生
- 跟踪学生参与情况

### 个人信息管理
- 更新个人信息
- 修改密码
- 查看统计信息

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
- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册
- `GET /users/profile` - 获取用户信息
- `PUT /users/profile` - 更新用户信息
- `PUT /users/change-password` - 修改密码

### 场景相关
- `GET /scenarios/` - 获取场景列表
- `POST /scenarios/` - 创建场景（教师）
- `POST /scenarios/{id}/join` - 加入场景
- `POST /scenarios/{id}/start` - 启动场景（教师）
- `POST /scenarios/{id}/end` - 结束场景（教师）

### 竞价相关
- `POST /bids/submit` - 提交竞价
- `GET /bids/my-bids` - 获取用户竞价
- `GET /bids/scenario/{id}` - 获取场景竞价

### 仿真相关
- `GET /simulation/results/{scenario_id}` - 获取出清结果

### 班级管理
- `GET /classes/` - 获取班级列表（教师）
- `POST /classes/` - 创建班级（教师）
- `GET /classes/{id}` - 获取班级详情
- `POST /classes/{id}/add-student` - 添加学生
- `DELETE /classes/{id}/remove-student/{student_id}` - 移除学生

---

## 🛠️ 故障排除

### 常见问题

**前端无法启动:**
- 检查Node.js版本（v16+）
- 在frontend目录运行`npm install`
- 检查端口3000是否可用

**后端无法启动:**
- 检查Python版本（3.8+）
- 安装依赖：`pip install -r requirements.txt`
- 检查端口8000是否可用

**CORS错误:**
- 确保后端运行在端口8000
- 检查浏览器控制台具体错误

**认证问题:**
- 清除浏览器localStorage
- 检查JWT令牌有效期
- 验证用户名/密码

### 开发提示

- 使用Vue DevTools进行调试
- 检查浏览器控制台API错误
- 监控网络标签页的请求/响应详情
- 使用localStorage检查认证状态

---

## 📊 实验流程

1. **教师创建场景** → 场景待启动
2. **教师启动场景** → 学生可以加入
3. **学生加入并竞价** → 实时竞价
4. **教师结束场景** → 市场出清
5. **结果可用** → 分析和图表

---

## 🎯 最佳实践

### 教师
- 创建具有现实需求值的场景
- 设置适当的实验持续时间
- 监控学生参与情况
- 审查学习成果结果

### 学生
- 提交多个竞价测试策略
- 监控市场条件
- 分析结果学习
- 与同学合作

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
- 前端：`vite.config.js` 的 `server.port` 配置

### Q: 前端页面空白？
A: 检查浏览器控制台错误，确认前端服务正常运行，清除浏览器缓存

### Q: 依赖安装失败？
A: 检查网络连接，尝试使用国内镜像源

---

## 📞 支持

遇到技术问题：
1. 检查浏览器控制台错误
2. 验证后端API响应
3. 检查网络连接
4. 查看本文档

---

## 🔄 更新

平台支持：
- 实时场景更新
- 实时竞价界面
- 动态结果计算
- 自动数据刷新

**开始您的电力市场仿真之旅！** 🎓⚡ 