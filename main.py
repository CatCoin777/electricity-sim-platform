from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, admin, simulation, evaluation, classes, scenarios, bids

app = FastAPI(title="电力市场仿真平台")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议设置具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(simulation.router)
app.include_router(evaluation.router)
app.include_router(classes.router)
app.include_router(scenarios.router)
app.include_router(bids.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
