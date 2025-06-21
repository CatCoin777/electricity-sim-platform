from fastapi import FastAPI
from routers import auth, users, admin, simulation

app = FastAPI(title="电力市场仿真平台")

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(simulation.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
