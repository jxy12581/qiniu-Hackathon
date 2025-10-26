@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo =========================================
echo    AI导航助手 - 一键启动脚本
echo    AI Navigator - Quick Start Script
echo =========================================
echo.

:check_python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    echo ❌ Error: Python not found
    echo 请安装 Python 3.10 或更高版本
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"') do set python_version=%%i
echo ✓ 检测到 Python %python_version%

python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
if %errorlevel% neq 0 (
    echo ❌ 错误: Python 版本过低
    echo ❌ Error: Python version too low
    echo 需要 Python 3.10 或更高版本，当前版本: %python_version%
    echo Required: Python 3.10+, Current: %python_version%
    pause
    exit /b 1
)
echo ✓ Python 版本符合要求 (^>=3.10)

:install_dependencies
echo.
echo =========================================
echo 📦 检查并安装依赖...
echo 📦 Checking and installing dependencies...
echo =========================================

if not exist "requirements.txt" (
    echo ❌ 错误: 未找到 requirements.txt
    echo ❌ Error: requirements.txt not found
    pause
    exit /b 1
)

echo 正在安装依赖包...
python -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ 依赖安装完成

:start_service
echo.
echo =========================================
echo 🚀 启动服务...
echo 🚀 Starting service...
echo =========================================
echo.

if not exist "src\ai_navigator_api.py" (
    echo ❌ 错误: 未找到 src\ai_navigator_api.py
    echo ❌ Error: src\ai_navigator_api.py not found
    pause
    exit /b 1
)

echo 正在启动 AI 导航助手服务器...
echo Starting AI Navigator API server...
echo.
echo 服务将在以下地址启动:
echo Service will start at:
echo   - API 地址: http://localhost:8000
echo   - API 文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo Press Ctrl+C to stop the service
echo.
echo =========================================
echo.

python src\ai_navigator_api.py

pause
