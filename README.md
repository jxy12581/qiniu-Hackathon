# 地图导航 MCP 服务器 / Map Navigator MCP Server

基于 MCP (Model Context Protocol) 的智能地图导航服务，支持通过 AI 助手控制百度地图和高德地图进行导航。

An intelligent map navigation service based on MCP (Model Context Protocol) that enables AI assistants to control Baidu Maps and Amap for navigation.

## 📋 功能特性 / Features

- ✅ **支持双地图平台** / Support for dual map platforms (Baidu Maps & Amap)
- ✅ **智能导航** / Intelligent navigation from point A to point B
- ✅ **自然语言交互** / Natural language interaction via AI assistants
- ✅ **多种交通方式** / Multiple transportation modes (driving, transit, walking, biking)
- ✅ **自动打开浏览器** / Automatic browser opening
- ✅ **无需硬编码** / No hardcoded logic - fully MCP-based

## 🏗️ 架构设计 / Architecture

```
┌─────────────────┐
│   AI Assistant  │  (Claude, GPT, etc.)
│   (MCP Client)  │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│   MCP Server    │
│  (Map Control)  │
├─────────────────┤
│  Tools:         │
│  - navigate     │
│  - open_map     │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Browser │
    └─────────┘
         │
    ┌────▼────────────┐
    │ 百度地图 / 高德 │
    └─────────────────┘
```

## 🚀 快速开始 / Quick Start

### 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

或者使用 uv 安装:

```bash
uv pip install -r requirements.txt
```

### 配置 MCP 客户端 / Configure MCP Client

#### Claude Desktop 配置

编辑 Claude Desktop 配置文件:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置:

```json
{
  "mcpServers": {
    "map-navigator": {
      "command": "python",
      "args": ["/path/to/qiniu-Hackathon/src/map_navigator_mcp.py"]
    }
  }
}
```

或者使用 uv:

```json
{
  "mcpServers": {
    "map-navigator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/qiniu-Hackathon",
        "run",
        "src/map_navigator_mcp.py"
      ]
    }
  }
}
```

### 重启 Claude Desktop

配置完成后重启 Claude Desktop，服务器将自动连接。

## 📖 使用方法 / Usage

配置完成后，你可以通过自然语言与 AI 助手对话来使用地图导航功能。

### 示例 1: 百度地图导航

**用户**: 帮我打开百度地图，从北京天安门导航到上海东方明珠

**AI助手**: 将调用 `navigate_baidu_map` 工具，自动在浏览器中打开百度地图导航页面。

### 示例 2: 高德地图导航

**用户**: 用高德地图规划一条从杭州西湖到深圳腾讯大厦的路线

**AI助手**: 将调用 `navigate_amap` 工具，自动在浏览器中打开高德地图导航页面。

### 示例 3: 查看地图位置

**用户**: 在百度地图上显示北京故宫的位置

**AI助手**: 将调用 `open_baidu_map` 工具，在浏览器中打开百度地图并定位到故宫。

### 示例 4: 语音输入支持

由于使用 AI 助手作为中间层，自然支持语音输入。用户可以通过语音说出起点和终点，AI 助手会理解并调用相应的地图导航工具。

**语音输入**: "帮我从广州塔导航到深圳湾公园，用高德地图"

**AI助手**: 理解语音内容后，调用 `navigate_amap` 工具完成导航。

## 🛠️ 可用工具 / Available Tools

### 1. `navigate_baidu_map`

在百度地图中打开从起点到终点的导航。

**参数**:
- `origin` (string, 必需): 起点地址，例如 "北京天安门"
- `destination` (string, 必需): 终点地址，例如 "上海东方明珠"
- `mode` (string, 可选): 导航模式
  - `driving` (默认): 驾车
  - `transit`: 公交
  - `walking`: 步行
  - `riding`: 骑行

### 2. `navigate_amap`

在高德地图中打开从起点到终点的导航。

**参数**:
- `origin` (string, 必需): 起点地址，例如 "北京天安门"
- `destination` (string, 必需): 终点地址，例如 "上海东方明珠"
- `mode` (string, 可选): 导航模式
  - `car` (默认): 驾车
  - `bus`: 公交
  - `walk`: 步行
  - `bike`: 骑行

### 3. `open_baidu_map`

在百度地图中显示指定位置。

**参数**:
- `location` (string, 必需): 要显示的位置，例如 "北京故宫"

### 4. `open_amap`

在高德地图中显示指定位置。

**参数**:
- `location` (string, 必需): 要显示的位置，例如 "北京故宫"

## 🔧 技术实现 / Technical Implementation

### MCP 协议

本项目基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 实现，这是 Anthropic 开发的开放协议，用于 AI 助手与外部工具的标准化通信。

### 核心技术栈

- **Python 3.10+**: 主要编程语言
- **mcp**: MCP 协议 Python SDK
- **webbrowser**: 标准库，用于打开浏览器
- **urllib**: URL 编码处理

### 地图 URL 构造

**百度地图**:
```
https://map.baidu.com/direction?origin={起点}&destination={终点}&mode={模式}
```

**高德地图**:
```
https://uri.amap.com/navigation?to={终点}&mode={模式}
```

## 🎯 设计优势 / Design Advantages

1. **无硬编码**: 所有逻辑通过 MCP 工具动态调用，易于扩展和维护
2. **自然交互**: 支持自然语言和语音输入，用户体验友好
3. **平台无关**: 通过标准浏览器打开，支持所有操作系统
4. **可扩展性**: 易于添加新的地图服务或功能
5. **AI 驱动**: 充分利用 AI 理解用户意图，智能选择最合适的工具

## 📝 开发说明 / Development Notes

### 添加新的地图服务

要添加新的地图服务（如 Google Maps），只需:

1. 在 `handle_list_tools()` 中添加新的工具定义
2. 在 `handle_call_tool()` 中实现工具逻辑
3. 构造对应的地图 URL

示例:

```python
Tool(
    name="navigate_google_maps",
    description="Open Google Maps navigation",
    inputSchema={
        "type": "object",
        "properties": {
            "origin": {"type": "string"},
            "destination": {"type": "string"}
        },
        "required": ["origin", "destination"]
    }
)
```

### 调试 MCP 服务器

使用 MCP Inspector 进行调试:

```bash
npx @modelcontextprotocol/inspector python src/map_navigator_mcp.py
```

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

## 📄 许可证 / License

MIT License

## 🔗 相关链接 / Links

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [百度地图开放平台](https://lbsyun.baidu.com/)
- [高德开放平台](https://lbs.amap.com/)

---

**项目说明**: 本项目为七牛云 Hackathon 参赛作品，展示了如何使用 MCP 协议实现 AI 控制计算机的实际应用场景。
