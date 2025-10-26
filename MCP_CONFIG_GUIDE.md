# MCP服务配置指南 / MCP Service Configuration Guide

本文档说明如何配置 Claude Desktop 使用本项目的 MCP 服务，包括七牛AI和地图导航服务的集成。

This document explains how to configure Claude Desktop to use the MCP services in this project, including Qiniu AI and map navigation service integration.

## 📋 概述 / Overview

本项目支持以下 MCP 服务：

This project supports the following MCP services:

- **地图导航服务 / Map Navigation Service**: 百度地图 (Baidu Maps) 和 高德地图 (Amap)
- **七牛AI服务 / Qiniu AI Service**: 七牛云AI能力集成 (准备中 / In preparation)

## 🔧 配置步骤 / Configuration Steps

### 1. 找到 Claude Desktop 配置文件 / Locate Claude Desktop Config File

根据你的操作系统，找到配置文件位置：

Locate the configuration file based on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. 配置地图导航MCP服务 / Configure Map Navigation MCP Service

#### 方式一：使用 Python 直接运行 / Method 1: Run with Python directly

编辑配置文件，添加以下内容：

Edit the config file and add the following:

```json
{
  "mcpServers": {
    "map-navigator": {
      "command": "python",
      "args": [
        "/absolute/path/to/qiniu-Hackathon/src/map_navigator_mcp.py"
      ]
    }
  }
}
```

**⚠️ 重要**: 将 `/absolute/path/to/qiniu-Hackathon` 替换为项目的实际绝对路径。

**⚠️ Important**: Replace `/absolute/path/to/qiniu-Hackathon` with the actual absolute path to the project.

#### 方式二：使用 uv 运行 / Method 2: Run with uv

```json
{
  "mcpServers": {
    "map-navigator": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/qiniu-Hackathon",
        "run",
        "src/map_navigator_mcp.py"
      ]
    }
  }
}
```

### 3. 配置七牛AI服务 / Configure Qiniu AI Service

七牛云提供多种AI能力，包括：

Qiniu Cloud provides various AI capabilities, including:

- **大语言模型 / Large Language Models**: 通过七牛AI平台访问各种LLM
- **图像处理 / Image Processing**: AI图像识别、处理等
- **语音服务 / Speech Services**: 语音识别、合成等

#### 添加七牛AI配置 / Add Qiniu AI Configuration

在配置文件中添加环境变量：

Add environment variables to the config file:

```json
{
  "mcpServers": {
    "map-navigator": {
      "command": "python",
      "args": ["/path/to/qiniu-Hackathon/src/map_navigator_mcp.py"]
    }
  },
  "env": {
    "QINIU_ACCESS_KEY": "your_qiniu_access_key",
    "QINIU_SECRET_KEY": "your_qiniu_secret_key",
    "QINIU_AI_ENDPOINT": "https://ai.qiniuapi.com"
  }
}
```

**获取七牛云密钥 / Get Qiniu Cloud Keys**:

1. 访问 [七牛云控制台](https://portal.qiniu.com/)
2. 登录后进入「密钥管理」
3. 获取 AccessKey 和 SecretKey
4. 将密钥填入配置文件

### 4. 完整配置示例 / Complete Configuration Example

```json
{
  "mcpServers": {
    "map-navigator": {
      "command": "python",
      "args": [
        "/Users/username/projects/qiniu-Hackathon/src/map_navigator_mcp.py"
      ],
      "env": {
        "QINIU_ACCESS_KEY": "your_access_key_here",
        "QINIU_SECRET_KEY": "your_secret_key_here"
      }
    }
  },
  "globalShortcut": "Ctrl+Space"
}
```

### 5. 重启 Claude Desktop / Restart Claude Desktop

配置完成后，完全退出并重新启动 Claude Desktop。

After configuration, completely quit and restart Claude Desktop.

## 🧪 测试配置 / Test Configuration

### 测试地图导航 / Test Map Navigation

在 Claude Desktop 中尝试以下指令：

Try the following commands in Claude Desktop:

1. **基础导航 / Basic Navigation**:
   - "帮我打开百度地图，从北京天安门导航到上海东方明珠"
   - "用高德地图规划从杭州西湖到深圳腾讯大厦的路线"

2. **多目的地导航 / Multi-destination Navigation**:
   - "我要从北京出发，依次去上海、杭州、苏州，用百度地图"
   - "帮我规划最优路线，从广州到深圳、东莞、佛山"

3. **查看位置 / View Location**:
   - "在百度地图上显示北京故宫的位置"
   - "用高德地图显示上海迪士尼的位置"

### 测试七牛AI集成 / Test Qiniu AI Integration

七牛AI功能可以通过以下方式使用：

Qiniu AI features can be accessed through:

1. **通过 REST API**: 使用 `src/ai_navigator_api.py` 提供的API接口
2. **通过 MCP**: 在 Claude Desktop 中直接调用（需要实现七牛AI MCP工具）

## 📚 可用的 MCP 工具 / Available MCP Tools

配置成功后，Claude Desktop 将可以访问以下工具：

After successful configuration, Claude Desktop will have access to these tools:

### 地图导航工具 / Map Navigation Tools

1. **`navigate_baidu_map`**: 百度地图单点导航
2. **`navigate_amap`**: 高德地图单点导航
3. **`open_baidu_map`**: 在百度地图显示位置
4. **`open_amap`**: 在高德地图显示位置
5. **`navigate_baidu_map_multi`**: 百度地图多点导航（支持路线优化）
6. **`navigate_amap_multi`**: 高德地图多点导航（支持路线优化）

## 🔍 调试配置 / Debug Configuration

### 使用 MCP Inspector

如果遇到问题，可以使用 MCP Inspector 进行调试：

If you encounter issues, use MCP Inspector for debugging:

```bash
npx @modelcontextprotocol/inspector python src/map_navigator_mcp.py
```

### 查看日志 / View Logs

Claude Desktop 的日志位置：

Claude Desktop log locations:

- **macOS**: `~/Library/Logs/Claude/`
- **Windows**: `%APPDATA%\Claude\logs\`
- **Linux**: `~/.config/Claude/logs/`

## 🎯 七牛AI能力集成规划 / Qiniu AI Integration Roadmap

### 已实现 / Implemented

- ✅ 地图导航 MCP 服务
- ✅ REST API 服务接口
- ✅ 自然语言理解

### 计划实现 / Planned

- 🔄 七牛AI大模型集成
- 🔄 图像识别服务
- 🔄 语音处理服务
- 🔄 文档分析能力

## 💡 使用建议 / Usage Tips

1. **首次使用**: 建议先测试简单的地图导航功能，确保 MCP 服务正常工作
2. **环境变量**: 七牛云密钥应当保密，不要提交到版本控制系统
3. **路径配置**: 使用绝对路径可以避免路径解析问题
4. **依赖安装**: 确保已安装 `requirements.txt` 中列出的所有依赖

## 🔗 相关资源 / Related Resources

- [七牛云官网](https://www.qiniu.com/)
- [七牛云AI平台](https://www.qiniu.com/products/qiniuai)
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Desktop 使用指南](https://claude.ai/desktop)

## ❓ 常见问题 / FAQ

### Q1: MCP 服务无法连接？

**A**: 检查以下几点：
1. 配置文件路径是否正确
2. Python 环境是否正确安装
3. 依赖包是否都已安装
4. Claude Desktop 是否已重启

### Q2: 如何验证七牛云密钥是否正确？

**A**: 可以使用七牛云 SDK 编写简单的测试脚本验证：

```python
from qiniu import Auth

access_key = 'your_access_key'
secret_key = 'your_secret_key'
q = Auth(access_key, secret_key)

# 如果密钥正确，这不会抛出异常
token = q.token()
print("密钥验证成功！")
```

### Q3: 支持哪些操作系统？

**A**: 支持 macOS、Windows 和 Linux。地图导航功能通过浏览器打开，具有良好的跨平台兼容性。

---

**项目仓库**: https://github.com/jxy12581/qiniu-Hackathon

**问题反馈**: 请在 GitHub Issues 中提出
