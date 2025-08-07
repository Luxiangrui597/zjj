#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import webbrowser

def create_github_pages_files():
    """创建GitHub Pages所需的文件"""
    
    # 创建.github/workflows目录
    os.makedirs('.github/workflows', exist_ok=True)
    
    # 创建GitHub Actions工作流文件
    workflow_content = '''name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    - name: Setup Pages
      uses: actions/configure-pages@v4
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: '.'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
'''
    
    with open('.github/workflows/deploy.yml', 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    # 创建README文件
    readme_content = '''# 🐕 可爱投票网页

这是一个可爱的投票网页，可以在微信中分享使用。

## 🌐 在线访问

访问地址：https://你的用户名.github.io/仓库名/

## 📋 功能特点

- 🎨 可爱的粉色渐变设计
- 📱 完全适配手机屏幕
- 💕 可爱的动画效果
- 🐾 小狗主题装饰元素
- ⚡ 快速响应，无需数据库

## 🎯 投票问题

**问题：** 周佳佳是不是陆祥瑞的小狗？

**选项：**
- 🐕 是
- ❌ 不是

## 🎨 设计特色

- 粉色渐变背景
- 圆角卡片设计
- 可爱的emoji装饰
- 悬停动画效果
- 响应式布局

---

💕 享受这个可爱的投票体验吧！
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ GitHub Pages文件已创建！")

def init_git_repo():
    """初始化Git仓库"""
    try:
        # 初始化Git仓库
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git仓库已初始化")
        
        # 添加所有文件
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ 文件已添加到Git")
        
        # 提交
        subprocess.run(['git', 'commit', '-m', 'Initial commit: 可爱投票网页'], check=True)
        print("✅ 初始提交已完成")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 GitHub Pages 部署助手")
    print("=" * 60)
    
    # 创建GitHub Pages文件
    create_github_pages_files()
    
    # 初始化Git仓库
    if init_git_repo():
        print("\n📋 下一步操作：")
        print("1. 在GitHub上创建一个新的仓库")
        print("2. 运行以下命令推送代码：")
        print("   git remote add origin https://github.com/你的用户名/仓库名.git")
        print("   git branch -M main")
        print("   git push -u origin main")
        print("3. 在仓库设置中启用GitHub Pages")
        print("4. 等待几分钟后即可通过 https://你的用户名.github.io/仓库名/ 访问")
        
        # 打开GitHub
        try:
            webbrowser.open('https://github.com/new')
        except:
            pass
    else:
        print("❌ 部署准备失败")

if __name__ == "__main__":
    main() 