#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import socket
import webbrowser
import os

# 设置端口
PORT = 8000

# 获取本机IP地址
def get_local_ip():
    try:
        # 连接到外部地址来获取本机IP
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

if __name__ == "__main__":
    # 确保在正确的目录中
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建服务器
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        local_ip = get_local_ip()
        print("=" * 50)
        print("🌐 可爱投票网页服务器已启动！")
        print("=" * 50)
        print(f"📱 本地访问: http://localhost:{PORT}")
        print(f"🌍 局域网访问: http://{local_ip}:{PORT}")
        print("=" * 50)
        print("💡 提示：")
        print("1. 在微信中分享 http://{local_ip}:{PORT} 链接")
        print("2. 确保手机和电脑在同一个WiFi网络下")
        print("3. 按 Ctrl+C 停止服务器")
        print("=" * 50)
        
        # 自动打开浏览器
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except:
            pass
        
        # 启动服务器
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止") 