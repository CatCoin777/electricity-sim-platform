#!/usr/bin/env python3
"""
前端服务器 - 解决CORS问题
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def serve_frontend():
    """启动前端服务器"""
    # 设置端口
    PORT = 3000
    
    # 切换到frontend目录
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ 错误：找不到frontend目录")
        return
    
    os.chdir(frontend_dir)
    
    # 创建HTTP服务器
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 前端服务器启动成功！")
        print(f"📍 地址：http://localhost:{PORT}")
        print(f"📍 自动打开浏览器...")
        print(f"⏹️  按 Ctrl+C 停止服务")
        print("-" * 50)
        
        # 自动打开浏览器
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 前端服务器已停止")

if __name__ == "__main__":
    serve_frontend() 