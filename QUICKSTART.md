# 🚀 快速开始指南

## 一键启动（推荐）

```bash
python start.py
```

这个脚本会自动：
- ✅ 检查Python版本
- 📦 安装所需依赖
- 📁 创建必要目录
- 📄 生成示例数据
- 🚀 启动后端服务器（端口8000）
- 🌐 启动前端服务器（端口3000）

## 分步启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动后端服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端服务（新开终端）
```bash
python serve_frontend.py
```

### 4. 访问应用
- **前端界面**：`http://localhost:3000`
- **后端API**：`http://localhost:8000`
- **API文档**：`http://localhost:8000/docs`

## 👥 测试账户

### 教师账户
- 用户名：`teacher1`
- 密码：`admin`
- 角色：教师

### 学生账户
- 用户名：`student1`
- 密码：`123456`
- 角色：学生

## 🎯 快速体验

### 1. 教师操作流程
1. 使用教师账户登录
2. 进入"管理面板"
3. 创建新场景
4. 创建班级并添加学生
5. 分配实验任务

### 2. 学生操作流程
1. 使用学生账户登录
2. 查看"实验场景"
3. 选择场景开始实验
4. 提交竞价数据
5. 查看结果分析

## 📊 示例实验

### 基础实验：统一价格机制
- **场景ID**：`lesson01`
- **需求量**：3 MW
- **参与者**：4名学生
- **机制**：统一价格

### 进阶实验：多种机制对比
- **场景ID**：`lesson02`
- **需求量**：5 MW
- **参与者**：5名学生
- **机制**：统一价格、按报价支付、固定成本

## 🔧 常见问题

### Q: 启动时提示缺少依赖？
A: 运行 `pip install -r requirements.txt`

### Q: 前端无法连接后端？
A: 确保两个服务都在运行：
- 后端：`http://localhost:8000`
- 前端：`http://localhost:3000`

### Q: 登录时出现CORS错误？
A: 确保使用 `http://localhost:3000` 访问前端，而不是直接打开HTML文件

### Q: 如何添加更多学生？
A: 在 `mock_data/mock_users.py` 中添加用户信息

### Q: 如何创建新场景？
A: 通过前端管理面板或直接编辑 `mock_data/scenarios.json`

### Q: 端口被占用怎么办？
A: 修改端口配置：
- 后端：修改 `uvicorn` 命令中的 `--port` 参数
- 前端：修改 `serve_frontend.py` 中的 `PORT` 变量

## 📈 功能演示

### 市场出清算法
- 8种不同的出清机制
- 实时计算和可视化
- 结果对比分析

### 评估系统
- 自动评分和排名
- 成绩分布统计
- 实验报告生成

### 班级管理
- 教师创建班级
- 学生管理
- 实验任务分配

## 🎨 界面预览

### 登录界面
- 用户身份验证
- 角色选择
- 注册功能

### 仪表板
- 统计概览
- 快速导航
- 状态监控

### 实验界面
- 竞价提交
- 实时计算
- 结果展示

### 管理面板
- 班级管理
- 场景配置
- 进度监控

## 🔧 故障排除

### 问题1：CORS错误
**症状**：浏览器控制台显示CORS错误
**解决**：
1. 确保使用 `http://localhost:3000` 访问前端
2. 检查后端服务是否在 `http://localhost:8000` 运行
3. 重启后端服务

### 问题2：端口冲突
**症状**：启动时提示端口被占用
**解决**：
```bash
# 查看端口占用
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 杀死占用进程
taskkill /PID <进程ID> /F
```

### 问题3：依赖安装失败
**症状**：pip安装时出错
**解决**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 强制重新安装
pip install -r requirements.txt --force-reinstall
```

### 问题4：前端页面空白
**症状**：页面加载但显示空白
**解决**：
1. 检查浏览器控制台错误
2. 确认前端服务器正常运行
3. 清除浏览器缓存

## 🚀 高级配置

### 修改端口
```python
# 修改 serve_frontend.py 中的端口
PORT = 3001  # 改为其他端口

# 修改后端端口
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 生产环境部署
```bash
# 使用Gunicorn启动后端
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 使用Nginx代理前端
# 配置Nginx指向前端静态文件
```

## 📱 移动端支持

平台支持移动端访问：
- 响应式设计
- 触摸友好的界面
- 适配不同屏幕尺寸

## 🔒 安全注意事项

### 开发环境
- CORS设置为允许所有来源（仅开发环境）
- 使用简单的JWT密钥

### 生产环境
- 限制CORS来源
- 使用强密钥
- 启用HTTPS
- 配置防火墙

---

**开始您的电力市场仿真之旅！** 🎓⚡ 