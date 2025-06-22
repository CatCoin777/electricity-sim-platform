#!/usr/bin/env python3
"""
电力市场仿真平台启动脚本
"""

import sys
import subprocess
import os
import threading
import time

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误：需要Python 3.7或更高版本")
        print(f"当前版本：{sys.version}")
        return False
    print(f"✅ Python版本检查通过：{sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 检查并安装依赖包...")
    
    try:
        # 检查是否已安装fastapi
        import fastapi
        print("✅ 依赖包已安装")
        return True
    except ImportError:
        print("⚠️  检测到缺少依赖包，正在安装...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ 依赖包安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖包安装失败：{e}")
            return False

def create_directories():
    """创建必要的目录"""
    directories = [
        "mock_data",
        "services/evaluation"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 创建目录：{directory}")

def create_sample_data():
    """创建示例数据文件"""
    import json
    
    # 创建示例场景
    scenarios_file = "mock_data/scenarios.json"
    if not os.path.exists(scenarios_file):
        sample_scenarios = {
            "lesson01": {
                "scenario_id": "lesson01",
                "demand": 3,
                "participants": ["alice", "bob", "charlie", "dave"],
                "enabled_mechanisms": ["uniform_price", "pay_as_bid"]
            },
            "lesson02": {
                "scenario_id": "lesson02",
                "demand": 5,
                "participants": ["alice", "bob", "charlie", "dave", "eve"],
                "enabled_mechanisms": ["uniform_price", "pay_as_bid", "fixed_cost_uniform"]
            }
        }
        
        with open(scenarios_file, 'w', encoding='utf-8') as f:
            json.dump(sample_scenarios, f, ensure_ascii=False, indent=2)
        print("📄 创建示例场景数据")

def start_backend_server():
    """启动后端服务器"""
    print("🚀 启动后端服务器...")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

def start_frontend_server():
    """启动前端服务器"""
    print("🌐 启动前端服务器...")
    time.sleep(2)  # 等待后端启动
    subprocess.run([sys.executable, "serve_frontend.py"])

def main():
    """主函数"""
    print("=" * 50)
    print("🔌 电力市场仿真平台启动器")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 无法安装依赖包，请手动运行：pip install -r requirements.txt")
        return
    
    # 创建示例数据
    create_sample_data()
    
    print("🚀 启动电力市场仿真平台...")
    print("📍 后端服务地址：http://localhost:8000")
    print("📍 API文档地址：http://localhost:8000/docs")
    print("📍 前端界面：http://localhost:3000")
    print("⏹️  按 Ctrl+C 停止所有服务")
    print("-" * 50)
    
    try:
        # 启动后端服务器（主线程）
        start_backend_server()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

if __name__ == "__main__":
    main() 