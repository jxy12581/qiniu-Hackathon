#!/bin/bash

set -e

echo "========================================="
echo "   AI导航助手 - 一键启动脚本"
echo "   AI Navigator - Quick Start Script"
echo "========================================="
echo ""

check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "❌ 错误: 未找到 Python 3"
        echo "❌ Error: Python 3 not found"
        echo "请安装 Python 3.10 或更高版本"
        echo "Please install Python 3.10 or higher"
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "✓ 检测到 Python $python_version"
    
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 10) else 1)'; then
        echo "✓ Python 版本符合要求 (>=3.10)"
    else
        echo "❌ 错误: Python 版本过低"
        echo "❌ Error: Python version too low"
        echo "需要 Python 3.10 或更高版本，当前版本: $python_version"
        echo "Required: Python 3.10+, Current: $python_version"
        exit 1
    fi
}

install_dependencies() {
    echo ""
    echo "========================================="
    echo "📦 检查并安装依赖..."
    echo "📦 Checking and installing dependencies..."
    echo "========================================="
    
    if [ ! -f "requirements.txt" ]; then
        echo "❌ 错误: 未找到 requirements.txt"
        echo "❌ Error: requirements.txt not found"
        exit 1
    fi
    
    if command -v pip3 &> /dev/null; then
        echo "正在使用 pip3 安装依赖包..."
        pip3 install -q -r requirements.txt
        echo "✓ 依赖安装完成"
    elif command -v pip &> /dev/null; then
        echo "正在使用 pip 安装依赖包..."
        pip install -q -r requirements.txt
        echo "✓ 依赖安装完成"
    elif python3 -m pip --version &> /dev/null; then
        echo "正在使用 python3 -m pip 安装依赖包..."
        python3 -m pip install -q -r requirements.txt
        echo "✓ 依赖安装完成"
    else
        echo "⚠️  警告: 未找到 pip，跳过依赖安装"
        echo "⚠️  Warning: pip not found, skipping dependency installation"
        echo "请手动安装依赖: pip install -r requirements.txt"
        echo "Please install dependencies manually: pip install -r requirements.txt"
    fi
}

start_service() {
    echo ""
    echo "========================================="
    echo "🚀 启动服务..."
    echo "🚀 Starting service..."
    echo "========================================="
    echo ""
    
    if [ ! -f "src/ai_navigator_api.py" ]; then
        echo "❌ 错误: 未找到 src/ai_navigator_api.py"
        echo "❌ Error: src/ai_navigator_api.py not found"
        exit 1
    fi
    
    echo "正在启动 AI 导航助手服务器..."
    echo "Starting AI Navigator API server..."
    echo ""
    echo "服务将在以下地址启动:"
    echo "Service will start at:"
    echo "  - API 地址: http://localhost:8000"
    echo "  - API 文档: http://localhost:8000/docs"
    echo ""
    echo "按 Ctrl+C 停止服务"
    echo "Press Ctrl+C to stop the service"
    echo ""
    echo "========================================="
    echo ""
    
    python3 src/ai_navigator_api.py
}

main() {
    check_python
    install_dependencies
    start_service
}

main
