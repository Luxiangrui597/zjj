#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import socket
import webbrowser
import os
import subprocess
import time
import requests
import json

# 设置端口
PORT = 8000

# 获取本机IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头，允许跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def check_ngrok_installed():
    """检查是否安装了ngrok"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok():
    """安装ngrok（Windows版本）"""
    print("正在下载ngrok...")
    try:
        # 下载ngrok
        import urllib.request
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        urllib.request.urlretrieve(url, "ngrok.zip")
        
        # 解压
        import zipfile
        with zipfile.ZipFile("ngrok.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # 删除zip文件
        os.remove("ngrok.zip")
        print("✅ ngrok安装成功！")
        return True
    except Exception as e:
        print(f"❌ 安装ngrok失败: {e}")
        return False

def start_ngrok():
    """启动ngrok隧道"""
    try:
        print("正在启动ngrok隧道...")
        # 启动ngrok（不需要认证的免费版本）
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', str(PORT), '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待一下让ngrok启动
        time.sleep(3)
        
        # 获取公网URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()['tunnels']
            if tunnels:
                public_url = tunnels[0]['public_url']
                return public_url, ngrok_process
        except:
            pass
        
        print("⚠️ 无法获取公网URL，请手动访问 http://localhost:4040 查看")
        return None, ngrok_process
        
    except Exception as e:
        print(f"❌ 启动ngrok失败: {e}")
        return None, None

if __name__ == "__main__":
    # 确保在正确的目录中
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("🌐 可爱投票网页 - 公网访问版本")
    print("=" * 60)
    
    # 检查ngrok
    if not check_ngrok_installed():
        print("📦 检测到未安装ngrok，正在自动安装...")
        if not install_ngrok():
            print("❌ 自动安装失败，请手动安装ngrok")
            print("💡 访问 https://ngrok.com/download 下载安装")
            exit(1)
    
    # 启动ngrok隧道
    public_url, ngrok_process = start_ngrok()
    
    # 创建服务器
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        local_ip = get_local_ip()
        
        print("=" * 60)
        print("🌐 服务器已启动！")
        print("=" * 60)
        print(f"📱 本地访问: http://localhost:{PORT}")
        print(f"🌍 局域网访问: http://{local_ip}:{PORT}")
        
        if public_url:
            print(f"🌐 公网访问: {public_url}")
            print("=" * 60)
            print("💡 提示：")
            print(f"1. 在微信中分享 {public_url} 链接")
            print("2. 任何人都可以访问，无需在同一网络")
            print("3. 按 Ctrl+C 停止服务器")
            print("=" * 60)
            
            # 自动打开浏览器
            try:
                webbrowser.open(public_url)
            except:
                pass
        else:
            print("=" * 60)
            print("💡 提示：")
            print("1. 访问 http://localhost:4040 查看公网链接")
            print("2. 复制显示的URL在微信中分享")
            print("3. 按 Ctrl+C 停止服务器")
            print("=" * 60)
        
        # 启动服务器
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")
            if ngrok_process:
                ngrok_process.terminate()
                print("🛑 ngrok隧道已关闭") 