# AI导航助手 / AI Navigation Assistant

基于 MCP (Model Context Protocol) 和 REST API 的智能地图导航服务，支持通过 AI 助手控制百度地图和高德地图进行导航，并提供 HTTP API 接口。

An intelligent map navigation service based on MCP (Model Context Protocol) and REST API that enables AI assistants to control Baidu Maps and Amap for navigation, with HTTP API access.

> 💡 **无需 Claude Desktop!** 本项目提供独立的 REST API 服务器，可直接使用所有功能。  
> 💡 **No Claude Desktop Required!** This project provides a standalone REST API server that works independently.

## 📋 功能特性 / Features

- ✅ **支持双地图平台** / Support for dual map platforms (Baidu Maps & Amap)
- ✅ **智能导航** / Intelligent navigation from point A to point B
- ✅ **多目的地路线规划** / Multi-destination route planning with optimization
- ✅ **自然语言交互** / Natural language interaction via AI assistants
- ✅ **浏览器对话界面** 🆕 / Browser-based dialog interface for interactive conversations
- ✅ **HTTP REST API** / RESTful API for programmatic access
- ✅ **AI自然语言理解** / AI-powered natural language query parsing
- ✅ **多种交通方式** / Multiple transportation modes (driving, transit, walking, biking)
- ✅ **自动打开浏览器** / Automatic browser opening
- ✅ **OpenAPI文档** / Interactive API documentation with Swagger UI
- ✅ **旅游攻略规划** / Travel guide planning with itinerary and budget estimation
- ✅ **高可用部署** 🆕 / High availability deployment with Docker, K8S, and load balancing
- ✅ **性能监控系统** 🆕 / Real-time performance monitoring (CPU, memory, disk, requests)
- ✅ **异常自动处理** 🆕 / Automatic exception handling with retry and circuit breaker
- ✅ **智能扩缩容** 🆕 / Auto-scaling for Kubernetes and Docker Compose
- ✅ **SRE告警通知** 🆕 / Multi-channel alerting system for SRE teams

## 🏗️ 架构设计 / Architecture

```
┌─────────────────┐       ┌─────────────────┐
│   AI Assistant  │       │  HTTP Clients   │
│   (MCP Client)  │       │  (Apps, Web)    │
└────────┬────────┘       └────────┬────────┘
         │ MCP Protocol            │ HTTP REST API
         │                         │
         │        ┌────────────────▼────────────────┐
         └────────►   AI Navigation Assistant       │
                  │  ┌──────────┐  ┌─────────────┐ │
                  │  │   MCP    │  │  FastAPI    │ │
                  │  │  Server  │  │   Server    │ │
                  │  └──────────┘  └─────────────┘ │
                  │  ┌───────────────────────────┐ │
                  │  │  AI NL Understanding      │ │
                  │  │  Navigation Engine        │ │
                  │  └───────────────────────────┘ │
                  └────────────────┬────────────────┘
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

### ⚡ 一键启动（推荐）/ Quick Start (Recommended)

#### Linux/Mac 用户

```bash
./start.sh
```

#### Windows 用户

```bash
start.bat
```

启动脚本会自动完成：
The startup script will automatically:
- ✅ 检查 Python 版本 / Check Python version (>=3.10)
- ✅ 安装依赖包 / Install dependencies
- ✅ 启动 API 服务器 / Start API server

服务器将在 `http://localhost:8000` 启动。

Server will start at `http://localhost:8000`.

**🌐 访问方式 / Access Methods:**
- **浏览器对话界面**: `http://localhost:8000` (推荐 / Recommended)
- **API 文档**: `http://localhost:8000/docs`

---

### 方法一：使用 REST API 服务器（推荐，无需 Claude Desktop）

#### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

或者使用 uv 安装 / Or install with uv:

```bash
uv pip install -r requirements.txt
```

#### 2. 启动 API 服务器 / Start API Server

```bash
python src/ai_navigator_api.py
```

服务器将在 `http://localhost:8000` 启动。

Server will start at `http://localhost:8000`.

**🌐 访问方式 / Access Methods:**
- **浏览器对话界面**: `http://localhost:8000` (推荐 / Recommended)
- **API 文档**: `http://localhost:8000/docs`

或使用 uvicorn / Or use uvicorn:

```bash
uvicorn src.ai_navigator_api:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 测试 API / Test the API

```bash
# 基础导航测试 / Basic navigation test
curl -X POST "http://localhost:8000/api/navigate" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "北京天安门",
    "destination": "上海东方明珠",
    "mode": "driving",
    "map_type": "baidu"
  }'

# AI 自然语言导航测试 / AI natural language test
curl -X POST "http://localhost:8000/api/ai/navigate" \
  -H "Content-Type: application/json" \
  -d '{"query": "帮我从北京天安门导航到上海东方明珠"}'
```

---

### 方法二：使用 MCP 客户端（需要 Claude Desktop 或其他 MCP 客户端）

#### 1. 安装依赖（同上）

#### 2. 配置 MCP 客户端 / Configure MCP Client

##### Claude Desktop 配置

> 📖 **详细配置指南**: 请参阅 [MCP_CONFIG_GUIDE.md](./MCP_CONFIG_GUIDE.md) 获取完整的配置说明，包括七牛AI集成、调试方法和常见问题解答。

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

参考配置文件示例: [`claude_desktop_config.json`](./claude_desktop_config.json)

#### 3. 重启 Claude Desktop / Restart Claude Desktop

配置完成后重启 Claude Desktop，服务器将自动连接。

After configuration, restart Claude Desktop and the server will connect automatically.

##### 其他 MCP 客户端 / Other MCP-Compatible Clients

目前 MCP 协议主要在 Claude Desktop 上经过完整测试。理论上任何支持 MCP 协议的客户端都可以使用本项目。

Currently, the MCP protocol has been fully tested with Claude Desktop. Theoretically, any MCP-compatible client can use this project.

**如果 Claude Desktop 不可用：**
1. ✅ **强烈推荐使用上述 REST API 方法**（方法一），无需任何 AI 客户端即可使用所有功能
2. 等待其他 AI 平台发布支持 MCP 的桌面应用
3. 使用 MCP SDK 自行开发客户端

**If Claude Desktop is unavailable:**
1. ✅ **Strongly recommend using the REST API method** (Method 1) - all features work without any AI client
2. Wait for other AI platforms to release MCP-compatible desktop applications
3. Build your own client using the MCP SDKs

## 📖 使用方法 / Usage

### 方式一：浏览器对话界面（最简单，推荐）🌟

启动服务器后，直接在浏览器中访问 `http://localhost:8000` 即可使用智能对话界面。

After starting the server, simply visit `http://localhost:8000` in your browser to use the intelligent dialog interface.

**特点 / Features:**
- 💬 对话式交互，自然流畅
- 🎨 精美的现代化界面
- ⚡ 实时响应，无需刷新
- 📱 支持移动端访问

### 方式二：通过 HTTP REST API

可以通过任何 HTTP 客户端访问导航功能，无需 Claude Desktop。

Access navigation features via any HTTP client, without needing Claude Desktop.

详细的 API 文档请访问 `http://localhost:8000/docs` / For detailed API documentation, visit `http://localhost:8000/docs`

### 方式三：通过 MCP 与 AI 助手交互（需要 Claude Desktop）

配置完成后，你可以通过自然语言与 AI 助手对话来使用地图导航功能。

After configuration, you can use natural language to interact with the AI assistant for navigation.

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

### 示例 5: 多目的地导航 🆕

**用户**: 帮我规划一个路线，从北京出发，依次去上海、杭州、苏州，用百度地图

**AI助手**: 将调用 `navigate_baidu_map_multi` 工具，自动在浏览器中打开包含多个途经点的百度地图导航。

### 示例 6: 优化路线 🆕

**用户**: 我要从广州出发去深圳、东莞、佛山三个地方，帮我用高德地图规划最优路线

**AI助手**: 将调用 `navigate_amap_multi` 工具并启用路线优化，计算访问所有地点的最短路径。

### 示例 7: 旅游攻略规划 🎉

**用户**: 帮我规划北京3天游的攻略

**AI助手**: 将调用旅游攻略规划功能，生成包含景点推荐、每日行程、预算估算和旅行建议的完整攻略。

---

## 🔌 REST API 详细示例 / Detailed REST API Examples

#### API 示例 1: 基础导航

```bash
curl -X POST "http://localhost:8000/api/navigate" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "北京天安门",
    "destination": "上海东方明珠",
    "mode": "driving",
    "map_type": "baidu"
  }'
```

#### API 示例 2: 多目的地导航

```bash
curl -X POST "http://localhost:8000/api/navigate/multi" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "北京天安门",
    "destinations": ["上海东方明珠", "杭州西湖", "苏州园林"],
    "mode": "driving",
    "optimize": false,
    "map_type": "baidu"
  }'
```

#### API 示例 3: AI 自然语言导航 🌟

```bash
curl -X POST "http://localhost:8000/api/ai/navigate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "帮我从北京天安门导航到上海东方明珠，用百度地图"
  }'
```

更多示例：

```bash
# 步行导航
curl -X POST "http://localhost:8000/api/ai/navigate" \
  -H "Content-Type: application/json" \
  -d '{"query": "从广州塔到深圳湾公园，步行路线，用高德地图"}'

# 多目的地路线
curl -X POST "http://localhost:8000/api/ai/navigate" \
  -H "Content-Type: application/json" \
  -d '{"query": "我要从杭州西湖出发，依次去苏州园林、南京夫子庙、扬州瘦西湖"}'
```

#### API 示例 4: 旅游攻略规划 🎉

```bash
# 创建基础旅游攻略
curl -X POST "http://localhost:8000/api/travel/guide" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "北京",
    "duration_days": 3,
    "travel_style": "经典游"
  }'

# AI自然语言创建旅游攻略
curl -X POST "http://localhost:8000/api/travel/guide/ai" \
  -H "Content-Type: application/json" \
  -d '{"query": "帮我规划杭州5天深度游"}'

# 获取支持的城市列表
curl -X GET "http://localhost:8000/api/travel/cities"
```

#### API 示例 5: Python 客户端

```python
import requests

response = requests.post(
    "http://localhost:8000/api/navigate",
    json={
        "origin": "北京天安门",
        "destination": "上海东方明珠",
        "mode": "driving",
        "map_type": "baidu"
    }
)
print(response.json())
```

运行示例代码：

```bash
python api_examples.py
python test_travel_guide.py
```

## 🛠️ 可用功能 / Available Features

### MCP 工具 (通过 AI 助手)

#### 1. `navigate_baidu_map`

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

### 5. `navigate_baidu_map_multi` 🆕

在百度地图中打开多目的地导航，支持顺序和优化路线规划。

**参数**:
- `origin` (string, 必需): 起点地址，例如 "北京天安门"
- `destinations` (array, 必需): 目的地列表(至少2个)，例如 ["上海东方明珠", "杭州西湖", "苏州园林"]
- `mode` (string, 可选): 导航模式
  - `driving` (默认): 驾车
  - `transit`: 公交
  - `walking`: 步行
  - `riding`: 骑行
- `optimize` (boolean, 可选): 是否优化路线顺序以获得最短总距离(默认: false)

#### 6. `navigate_amap_multi` 🆕

在高德地图中打开多目的地导航，支持顺序和优化路线规划。

**参数**:
- `origin` (string, 必需): 起点地址，例如 "北京天安门"
- `destinations` (array, 必需): 目的地列表(至少2个)，例如 ["上海东方明珠", "杭州西湖", "苏州园林"]
- `mode` (string, 可选): 导航模式
  - `car` (默认): 驾车
  - `bus`: 公交
  - `walk`: 步行
  - `bike`: 骑行
- `optimize` (boolean, 可选): 是否优化路线顺序以获得最短总距离(默认: false)

### REST API 端点 🆕

#### 导航相关

#### 1. `POST /api/navigate`

基础导航功能。

**请求体**:
```json
{
  "origin": "北京天安门",
  "destination": "上海东方明珠",
  "mode": "driving",
  "map_type": "baidu"
}
```

#### 2. `POST /api/navigate/multi`

多目的地导航。

**请求体**:
```json
{
  "origin": "北京天安门",
  "destinations": ["上海东方明珠", "杭州西湖", "苏州园林"],
  "mode": "driving",
  "optimize": false,
  "map_type": "baidu"
}
```

#### 3. `POST /api/location`

显示地图位置。

**请求体**:
```json
{
  "location": "北京故宫",
  "map_type": "baidu"
}
```

#### 4. `POST /api/ai/navigate` 🌟

AI 自然语言导航（智能解析用户查询）。

**请求体**:
```json
{
  "query": "帮我从北京天安门导航到上海东方明珠，用百度地图",
  "map_type": "baidu"
}
```

**支持的自然语言格式**:
- "从{起点}到{终点}"
- "从{起点}去{终点}，步行/骑行/公交"
- "用百度地图/高德地图导航到{终点}"
- "我要从{起点}出发，依次去{地点1}、{地点2}、{地点3}"

#### 5. `GET /health`

健康检查端点。

#### 6. `GET /docs`

交互式 API 文档（Swagger UI）。

#### 旅游攻略相关 🎉

#### 7. `POST /api/travel/guide`

创建完整的旅游攻略，包含景点推荐、行程安排、预算估算等。

**请求体**:
```json
{
  "destination": "北京",
  "duration_days": 3,
  "travel_style": "经典游",
  "start_date": "2025-05-01"
}
```

**参数说明**:
- `destination`: 目的地城市（当前支持：北京、上海、杭州、成都、西安）
- `duration_days`: 行程天数（1-30天）
- `travel_style`: 旅行风格
  - `深度游`: 慢节奏，每天2个景点，预算较高
  - `经典游`: 适中节奏，每天3个景点，标准预算（默认）
  - `打卡游`: 快节奏，每天4个景点，预算较低
- `start_date`: 出发日期（可选，格式：YYYY-MM-DD）

**响应示例**:
```json
{
  "success": true,
  "message": "成功创建北京3日游攻略",
  "guide": {
    "destination": "北京",
    "duration_days": 3,
    "travel_style": "经典游",
    "best_season": "春季(4-5月)和秋季(9-10月)，气候宜人，适合旅游",
    "itinerary": [
      {
        "day": 1,
        "date": "2025-05-01",
        "attractions": ["故宫博物院", "天坛公园", "天安门广场"],
        "activities": ["游览故宫博物院 (建议3-4小时)", "游览天坛公园 (建议2-3小时)", "游览天安门广场 (建议1-2小时)"],
        "notes": "根据经典游安排，适中节奏，游览主要景点"
      }
    ],
    "recommended_attractions": [
      {
        "name": "故宫博物院",
        "category": "历史文化",
        "description": "中国明清两代的皇家宫殿，世界文化遗产",
        "recommended_duration": "3-4小时",
        "best_time": "春秋季节，避开周一闭馆",
        "entrance_fee": "60元(旺季)/40元(淡季)"
      }
    ],
    "budget_estimate": {
      "transportation": 500.0,
      "accommodation": 1200.0,
      "food": 450.0,
      "tickets": 600.0,
      "shopping": 750.0,
      "total": 3500.0
    },
    "travel_tips": [
      "提前预订酒店和景点门票，可享受优惠",
      "故宫需要提前网上预约购票",
      "地铁是最方便的交通工具"
    ]
  }
}
```

#### 8. `POST /api/travel/guide/ai` 🌟

使用自然语言创建旅游攻略。

**请求体**:
```json
{
  "query": "帮我规划杭州5天深度游"
}
```

**支持的自然语言格式**:
- "帮我规划{城市}{X}天游"
- "我想去{城市}玩{X}天，深度游/打卡游"
- "{城市}{X}日游攻略"
- "{城市}{X}天{旅行风格}"

#### 9. `GET /api/travel/cities`

获取支持旅游攻略规划的城市列表。

**响应示例**:
```json
{
  "success": true,
  "cities": [
    {
      "name": "北京",
      "attractions_count": 5,
      "sample_attractions": ["故宫博物院", "长城(八达岭)", "天坛公园"]
    }
  ],
  "total": 5,
  "message": "当前支持5个城市的旅游攻略规划"
}
```

#### 监控与管理相关 🆕

#### 10. `GET /api/health/detailed`

获取详细的系统健康状态，包括性能指标、异常统计、扩缩容状态等。

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-26T09:00:00Z",
  "performance": {
    "cpu_percent": 45.2,
    "memory_percent": 62.8,
    "disk_percent": 35.1,
    "request_count": 1523,
    "error_count": 3,
    "avg_response_time_ms": 156.7
  },
  "exceptions": {
    "total_count": 12,
    "unresolved_count": 1,
    "recent_exceptions": []
  },
  "scaling": {
    "current_replicas": 3,
    "recommendation": "maintain"
  }
}
```

#### 11. `GET /api/monitoring/status`

获取实时性能监控状态。

**响应示例**:
```json
{
  "current_metrics": {
    "cpu_percent": 45.2,
    "memory_percent": 62.8,
    "disk_percent": 35.1,
    "request_count": 1523,
    "error_count": 3,
    "avg_response_time_ms": 156.7
  },
  "thresholds": {
    "cpu_threshold": 80.0,
    "memory_threshold": 85.0,
    "disk_threshold": 90.0
  },
  "health_status": "healthy"
}
```

#### 12. `GET /api/monitoring/metrics/history`

获取历史性能指标数据（最近60分钟）。

**查询参数**:
- `limit` (可选): 返回的记录数量，默认60

#### 13. `GET /api/monitoring/alerts`

获取所有监控告警。

**查询参数**:
- `unresolved_only` (可选): 仅返回未解决的告警，默认false

#### 14. `POST /api/monitoring/alerts/{metric_type}/resolve`

解决特定类型的告警。

**路径参数**:
- `metric_type`: 指标类型 (cpu, memory, disk, error_rate, response_time)

#### 15. `GET /api/exceptions/summary`

获取异常处理摘要统计。

**响应示例**:
```json
{
  "total_exceptions": 12,
  "unresolved_count": 1,
  "by_severity": {
    "critical": 0,
    "high": 1,
    "medium": 5,
    "low": 6
  },
  "by_type": {
    "ValueError": 5,
    "ConnectionError": 4,
    "TimeoutError": 3
  }
}
```

#### 16. `GET /api/exceptions/unresolved`

获取所有未解决的异常。

#### 17. `POST /api/exceptions/{exception_type}/resolve`

标记特定类型的异常为已解决。

#### 18. `GET /api/scaling/recommendation`

获取智能扩缩容建议。

**响应示例**:
```json
{
  "current_replicas": 3,
  "should_scale_up": false,
  "should_scale_down": false,
  "recommendation": "maintain",
  "reason": ["所有指标正常"],
  "current_metrics": {
    "cpu_percent": 45.2,
    "memory_percent": 62.8
  }
}
```

#### 19. `POST /api/scaling/evaluate`

评估并执行扩缩容操作。

**请求体**:
```json
{
  "force_scale_up": false,
  "force_scale_down": false
}
```

#### 20. `POST /api/scaling/manual`

手动设置副本数量。

**请求体**:
```json
{
  "replicas": 5
}
```

#### 21. `GET /api/scaling/history`

获取扩缩容历史记录。

**查询参数**:
- `limit` (可选): 返回的记录数量，默认20

#### 22. `GET /api/scaling/summary`

获取扩缩容状态摘要。

#### 23. `GET /api/notifications/history`

获取SRE告警通知历史。

**查询参数**:
- `limit` (可选): 返回的记录数量，默认50

#### 24. `GET /api/notifications/stats`

获取通知统计信息。

#### 25. `POST /api/notifications/test`

发送测试通知。

**请求体**:
```json
{
  "channel": "log",
  "message": "Test notification"
}
```

## 🔧 技术实现 / Technical Implementation

### MCP 协议

本项目基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 实现，这是 Anthropic 开发的开放协议，用于 AI 助手与外部工具的标准化通信。

### 核心技术栈

- **Python 3.10+**: 主要编程语言
- **mcp**: MCP 协议 Python SDK
- **FastAPI**: 现代高性能 Web 框架
- **Pydantic**: 数据验证和设置管理
- **uvicorn**: ASGI 服务器
- **webbrowser**: 标准库，用于打开浏览器
- **urllib**: URL 编码处理
- **psutil**: 系统性能监控
- **asyncio**: 异步任务处理

### AI 自然语言理解

API 服务集成了自然语言处理能力，可以理解多种中文表达方式：

- **起点识别**: "从...出发", "起点是...", "...到..." 等
- **终点识别**: "到...", "去...", "导航到...", "终点是..." 等
- **多目的地识别**: "依次去...", "先后去...", "去...、...、..." 等
- **交通方式识别**: "步行", "骑行", "公交", "驾车" 等
- **地图平台识别**: "百度地图", "高德地图", "用百度" 等

### 地图 URL 构造

**百度地图**:
```
https://map.baidu.com/direction?origin={起点}&destination={终点}&mode={模式}
```

**高德地图**:
```
https://uri.amap.com/navigation?to={终点}&mode={模式}
```

### 性能监控与异常处理系统 🆕

本项目集成了企业级的性能监控和异常自动处理系统：

#### 1. **结构化日志系统** (`structured_logger.py`)
- JSON 格式日志输出，便于日志分析
- 支持多级别日志（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 自动记录请求上下文和性能指标

#### 2. **实时性能监控** (`performance_monitor.py`)
- **CPU 监控**: 实时跟踪 CPU 使用率，超过阈值(80%)自动告警
- **内存监控**: 监控内存使用情况，超过阈值(85%)自动告警
- **磁盘监控**: 跟踪磁盘空间使用，超过阈值(90%)自动告警
- **请求统计**: 记录请求数量、错误率、平均响应时间
- **历史数据**: 保留最近60分钟的性能指标历史
- **智能告警**: 自动检测异常并生成告警

#### 3. **异常自动处理** (`exception_handler.py`)
- **自动重试机制**: 最多重试3次，支持指数退避
- **熔断器模式**: 连续失败5次后自动熔断60秒，防止雪崩
- **异常分级**: LOW、MEDIUM、HIGH、CRITICAL 四个级别
- **异常追踪**: 完整记录异常堆栈和上下文信息
- **自动恢复**: 异常解决后自动记录恢复时间

#### 4. **智能扩缩容** (`auto_scaler.py`)
- **多平台支持**: Kubernetes、Docker Compose、Systemd
- **自动扩容**: CPU/内存/磁盘/错误率超标时自动扩容
- **自动缩容**: 负载降低时自动缩容，节省资源
- **安全限制**: 最小3个副本，最大10个副本
- **扩缩容历史**: 记录所有扩缩容操作和原因

#### 5. **SRE 告警通知** (`sre_notifier.py`)
- **多渠道支持**: 日志、邮件、Webhook、PagerDuty 等
- **智能降噪**: 同类型告警5分钟内只发送一次
- **告警历史**: 完整记录所有告警通知
- **测试功能**: 支持发送测试通知验证配置

#### 系统特性
- ✅ **实时监控**: 每10秒采集一次性能指标
- ✅ **自动告警**: 超过阈值自动发送告警通知
- ✅ **自动恢复**: 异常自动重试，失败自动熔断
- ✅ **智能扩缩容**: 根据负载自动调整实例数量
- ✅ **零停机运维**: 支持滚动更新和健康检查

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

## 🚀 高可用部署 / High Availability Deployment

本项目支持多种高可用部署方案，避免单点故障。详细部署指南请参阅 [HIGH_AVAILABILITY_DEPLOYMENT.md](./HIGH_AVAILABILITY_DEPLOYMENT.md)。

This project supports various high availability deployment options to eliminate single points of failure. For detailed deployment instructions, see [HIGH_AVAILABILITY_DEPLOYMENT.md](./HIGH_AVAILABILITY_DEPLOYMENT.md).

### 部署选项 / Deployment Options

#### 1. Docker 容器化 / Docker Containerization

```bash
# 构建镜像 / Build image
docker build -t ai-navigator:latest .

# 运行容器 / Run container
docker run -d -p 8000:8000 --restart unless-stopped ai-navigator:latest
```

#### 2. Docker Compose（推荐用于开发和小规模生产）

```bash
# 启动3个应用实例 + Nginx 负载均衡器
docker-compose up -d

# 访问 / Access
curl http://localhost/health
```

特性:
- 3个应用副本 + Nginx 负载均衡
- 自动健康检查和重启
- 轮询负载均衡算法

#### 3. Kubernetes（推荐用于生产环境）

```bash
# 快速部署 / Quick deployment
kubectl apply -k k8s/

# 查看状态 / Check status
kubectl get pods,svc,hpa
```

特性:
- 最少3个副本，最多10个副本（HPA 自动扩缩容）
- 滚动更新（零停机）
- Pod 反亲和性（跨节点分布）
- 完整的健康检查（Liveness, Readiness, Startup）
- 资源限制和请求
- Ingress 路由

#### 4. 物理机/虚拟机 + Systemd

```bash
# 创建多个 Systemd 服务实例
sudo systemctl enable ai-navigator@8000
sudo systemctl enable ai-navigator@8001
sudo systemctl start ai-navigator@{8000,8001}

# 配置 Nginx 负载均衡
sudo systemctl reload nginx
```

### 高可用特性 / HA Features

✅ **无单点故障** - 多副本部署  
✅ **自动故障恢复** - 失败实例自动重启  
✅ **负载均衡** - Nginx/K8S Service 自动分发流量  
✅ **健康检查** - 主动监控和故障检测  
✅ **水平扩展** - 根据负载自动增减实例  
✅ **滚动更新** - 零停机部署新版本  

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
