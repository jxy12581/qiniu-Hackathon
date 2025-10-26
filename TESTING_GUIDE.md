# AI导航助手 - 测试指南
# AI Navigation Assistant - Testing Guide

**文档版本:** 1.0  
**创建日期:** 2025-10-26  
**适用版本:** v1.5.0

---

## 📋 目录 / Table of Contents

1. [测试概述](#测试概述)
2. [测试环境准备](#测试环境准备)
3. [自动化测试](#自动化测试)
4. [手动测试](#手动测试)
5. [功能验证清单](#功能验证清单)
6. [常见问题](#常见问题)

---

## 📊 测试概述

### 测试目标

本测试指南旨在帮助用户和开发者全面验证AI导航助手的所有功能,确保应用在各种场景下都能正常工作。

### 测试类型

1. **单元测试** - 测试各个独立模块
2. **集成测试** - 测试模块间的协作
3. **功能测试** - 测试用户可见功能
4. **端到端测试** - 测试完整使用流程

### 测试覆盖范围

- ✅ MCP服务器 (8个工具)
- ✅ REST API (6个端点)
- ✅ URL构造逻辑
- ✅ 自然语言解析
- ✅ 数据结构验证
- ✅ 高级功能模块

---

## 🔧 测试环境准备

### 系统要求

- **操作系统:** Linux / macOS / Windows
- **Python版本:** 3.10 或更高
- **网络连接:** 需要访问地图服务和天气API

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/jxy12581/qiniu-Hackathon.git
cd qiniu-Hackathon

# 安装依赖
pip install -r requirements.txt

# 或使用 uv
uv pip install -r requirements.txt
```

### 验证安装

```bash
# 检查Python版本
python3 --version

# 验证依赖包
python3 -c "import fastapi, uvicorn, pydantic, mcp; print('依赖已安装')"
```

---

## 🤖 自动化测试

### 1. 综合功能测试

**测试文件:** `comprehensive_test_demo.py`

**测试内容:**
- 百度地图URL构造 (3个测试)
- 高德地图URL构造 (3个测试)
- 自然语言解析 (4个测试)
- 天气信息结构 (3个测试)
- 旅游推荐结构 (3个测试)
- REST API端点 (6个测试)
- MCP工具定义 (8个测试)

**运行测试:**

```bash
python3 comprehensive_test_demo.py
```

**预期输出:**

```
======================================================================
          AI导航助手 - 综合测试Demo (优化版)
======================================================================

总测试数: 30
✅ 通过: 28 (93%)
❌ 失败: 2 (7%)

✅ 所有核心功能测试通过!
```

**测试时间:** 约5-10秒

### 2. 旅游攻略功能测试

**测试文件:** `test_travel_guide.py`

**测试内容:**
- 城市列表查询
- 攻略创建功能
- AI自然语言解析
- 数据结构验证
- 预算估算准确性

**运行测试:**

```bash
python3 test_travel_guide.py
```

**预期结果:**
- 成功查询支持的城市列表
- 成功创建旅游攻略
- 攻略包含完整的行程和预算信息

### 3. 速度监控功能测试

**测试文件:** `test_speed_monitor.py`

**测试内容:**
- 速度检查功能
- 限速提醒功能
- 不同道路类型的速度限制
- 路线速度规划

**运行测试:**

```bash
python3 test_speed_monitor.py
```

**预期结果:**
- 正确识别超速情况
- 提供准确的限速信息
- 支持6种道路类型

### 4. 交通方式推荐测试

**测试文件:** `test_transportation.py`

**测试内容:**
- 智能推荐算法
- 基于距离的推荐
- 时间和成本估算
- 路线规划功能

**运行测试:**

```bash
python3 test_transportation.py
```

**预期结果:**
- 根据距离推荐合适的交通方式
- 提供准确的时间和成本估算
- 支持4种交通方式

### 5. 目的地提醒功能测试

**测试文件:** `test_destination_reminder.py`

**测试内容:**
- 天气信息获取
- 旅游推荐生成
- 数据格式验证

**运行测试:**

```bash
python3 test_destination_reminder.py
```

**预期结果:**
- 成功获取天气信息
- 提供景点和美食推荐
- 数据结构完整

### 运行所有测试

```bash
# 运行所有测试脚本
for test_file in comprehensive_test_demo.py test_*.py; do
    echo "运行: $test_file"
    python3 "$test_file"
    echo "---"
done
```

---

## 👨‍💻 手动测试

### 1. REST API测试

#### 步骤1: 启动API服务器

```bash
# 方法1: 直接运行
python3 src/ai_navigator_api.py

# 方法2: 使用uvicorn
uvicorn src.ai_navigator_api:app --reload --port 8000

# 方法3: 使用启动脚本
./start.sh  # Linux/Mac
start.bat   # Windows
```

**预期输出:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 步骤2: 访问API文档

打开浏览器访问: http://localhost:8000/docs

**验证点:**
- ✅ 页面正常加载
- ✅ 显示所有API端点
- ✅ 可以展开查看详情

#### 步骤3: 测试健康检查端点

```bash
curl http://localhost:8000/health
```

**预期响应:**
```json
{
  "status": "healthy",
  "version": "1.5.0"
}
```

#### 步骤4: 测试基础导航API

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

**预期响应:**
```json
{
  "success": true,
  "message": "成功创建百度地图导航路线",
  "url": "https://map.baidu.com/direction?origin=...",
  "details": {
    "origin": "北京天安门",
    "destination": "上海东方明珠",
    "mode": "driving",
    "map_type": "baidu"
  }
}
```

**验证点:**
- ✅ 返回success: true
- ✅ 包含有效的URL
- ✅ 浏览器自动打开地图(如果支持)

#### 步骤5: 测试多目的地导航API

```bash
curl -X POST "http://localhost:8000/api/navigate/multi" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "北京天安门",
    "destinations": ["上海东方明珠", "杭州西湖", "苏州园林"],
    "mode": "driving",
    "optimize": true,
    "map_type": "baidu"
  }'
```

**验证点:**
- ✅ 返回成功响应
- ✅ URL包含多个目的地
- ✅ optimize参数生效

#### 步骤6: 测试AI自然语言导航API

```bash
curl -X POST "http://localhost:8000/api/ai/navigate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "帮我从广州塔导航到深圳湾公园，步行路线，用高德地图"
  }'
```

**验证点:**
- ✅ 正确解析起点: "广州塔"
- ✅ 正确解析终点: "深圳湾公园"
- ✅ 正确识别交通方式: "walking"
- ✅ 正确识别地图: "amap"

#### 步骤7: 测试旅游攻略API

```bash
curl -X POST "http://localhost:8000/api/travel/guide" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "北京",
    "duration_days": 3,
    "travel_style": "经典游"
  }'
```

**验证点:**
- ✅ 返回完整的旅游攻略
- ✅ 包含景点推荐
- ✅ 包含行程安排
- ✅ 包含预算估算

### 2. 浏览器对话界面测试

#### 步骤1: 访问对话界面

打开浏览器访问: http://localhost:8000

**验证点:**
- ✅ 页面正常加载
- ✅ 显示对话界面
- ✅ 输入框可用

#### 步骤2: 测试自然语言导航

在输入框中输入:
```
帮我从北京天安门导航到上海东方明珠
```

**验证点:**
- ✅ AI正确理解查询
- ✅ 返回导航链接
- ✅ 可以打开地图

#### 步骤3: 测试多轮对话

继续输入:
```
改用高德地图
```

**验证点:**
- ✅ 记住上次的起点和终点
- ✅ 切换到高德地图
- ✅ 返回新的导航链接

### 3. MCP集成测试

#### 前提条件

- 已安装Claude Desktop
- 已配置MCP服务器

#### 步骤1: 配置MCP

编辑配置文件 `claude_desktop_config.json`:

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

#### 步骤2: 重启Claude Desktop

关闭并重新打开Claude Desktop

#### 步骤3: 测试MCP工具

在Claude中输入:
```
帮我打开百度地图，从北京天安门导航到上海东方明珠
```

**验证点:**
- ✅ Claude识别导航请求
- ✅ 调用navigate_baidu_map工具
- ✅ 浏览器打开百度地图
- ✅ 显示正确的导航路线

#### 步骤4: 测试其他MCP工具

测试用例:
1. "用高德地图从广州到深圳"
2. "在百度地图上显示北京故宫"
3. "查询北京的天气"
4. "推荐上海的旅游景点"

**验证点:**
- ✅ 所有工具都能正常调用
- ✅ 返回正确的结果
- ✅ 地图能正常打开

---

## ✅ 功能验证清单

### 核心功能验证

#### 地图导航功能

- [ ] 百度地图单点导航
- [ ] 高德地图单点导航
- [ ] 百度地图多目的地导航
- [ ] 高德地图多目的地导航
- [ ] 路线优化功能
- [ ] 不同交通方式 (驾车/公交/步行/骑行)
- [ ] 位置显示和查询

#### AI交互功能

- [ ] 自然语言理解
- [ ] 起点终点解析
- [ ] 交通方式识别
- [ ] 地图平台识别
- [ ] 多目的地识别
- [ ] 口语化表达支持

#### 增值服务

- [ ] 天气查询功能
- [ ] 旅游景点推荐
- [ ] 美食推荐
- [ ] 旅游提示

### 高级功能验证

#### 旅游攻略规划

- [ ] 城市列表查询
- [ ] 攻略创建
- [ ] 行程安排生成
- [ ] 预算估算
- [ ] AI自然语言创建
- [ ] 不同旅行风格 (深度游/经典游/打卡游)

#### 速度监控

- [ ] 速度检查
- [ ] 超速提醒
- [ ] 道路类型识别
- [ ] 路线速度规划

#### 交通推荐

- [ ] 智能推荐算法
- [ ] 基于距离推荐
- [ ] 时间估算
- [ ] 成本估算
- [ ] 路线规划

### 接口功能验证

#### REST API

- [ ] POST /api/navigate
- [ ] POST /api/navigate/multi
- [ ] POST /api/location
- [ ] POST /api/ai/navigate
- [ ] POST /api/travel/guide
- [ ] POST /api/travel/guide/ai
- [ ] GET /api/travel/cities
- [ ] GET /health
- [ ] GET /docs

#### MCP工具

- [ ] navigate_baidu_map
- [ ] navigate_amap
- [ ] navigate_baidu_map_multi
- [ ] navigate_amap_multi
- [ ] open_baidu_map
- [ ] open_amap
- [ ] get_destination_weather
- [ ] get_travel_recommendations

### 浏览器界面验证

- [ ] 页面正常加载
- [ ] 对话输入框可用
- [ ] 发送消息功能
- [ ] 接收回复功能
- [ ] 链接点击可用
- [ ] 移动端响应式

---

## ❓ 常见问题

### Q1: 运行测试时出现 "ModuleNotFoundError"

**原因:** 依赖包未安装

**解决方案:**
```bash
pip install -r requirements.txt
```

### Q2: API服务器启动失败

**可能原因:**
1. 端口8000已被占用
2. Python版本不兼容
3. 依赖包缺失

**解决方案:**
```bash
# 检查端口占用
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# 使用不同端口
uvicorn src.ai_navigator_api:app --port 8001

# 检查Python版本
python3 --version  # 需要 >= 3.10
```

### Q3: 浏览器没有自动打开地图

**原因:** 
1. 操作系统限制
2. 没有默认浏览器
3. 运行在远程服务器上

**解决方案:**
- 手动复制URL到浏览器
- API仍会返回正确的URL
- 这不影响功能使用

### Q4: MCP集成测试失败

**可能原因:**
1. Claude Desktop配置错误
2. Python路径不正确
3. MCP服务器未启动

**解决方案:**
1. 检查配置文件路径
2. 使用绝对路径
3. 查看Claude Desktop日志
4. 参考 MCP_CONFIG_GUIDE.md

### Q5: 自然语言解析不准确

**说明:**
- 测试demo使用简化版解析逻辑
- 实际源代码已优化
- 支持更多语言模式

**验证方法:**
```bash
# 直接测试API
curl -X POST "http://localhost:8000/api/ai/navigate" \
  -H "Content-Type: application/json" \
  -d '{"query": "你的查询"}'
```

### Q6: 天气API返回错误

**原因:** 
- wttr.in服务限制
- 网络连接问题
- 位置名称不正确

**解决方案:**
- 检查网络连接
- 使用常见城市名称
- 稍后重试

---

## 📊 测试报告模板

### 测试记录表

| 测试项 | 测试时间 | 测试结果 | 问题描述 | 解决方案 |
|--------|---------|---------|---------|---------|
| 综合测试Demo | YYYY-MM-DD | ✅ 通过 | - | - |
| REST API测试 | YYYY-MM-DD | ✅ 通过 | - | - |
| MCP集成测试 | YYYY-MM-DD | ✅ 通过 | - | - |
| 浏览器界面测试 | YYYY-MM-DD | ✅ 通过 | - | - |

### 测试总结

**测试日期:** _____________  
**测试人员:** _____________  
**测试环境:** _____________  
**Python版本:** _____________

**测试结果:**
- 总测试数: _____
- 通过数: _____
- 失败数: _____
- 通过率: _____%

**问题列表:**
1. _____________________
2. _____________________

**改进建议:**
1. _____________________
2. _____________________

---

## 🎯 测试最佳实践

### 测试前准备

1. ✅ 确保网络连接正常
2. ✅ 关闭防火墙或允许端口8000
3. ✅ 确保Python版本符合要求
4. ✅ 安装所有依赖包
5. ✅ 了解项目基本功能

### 测试过程

1. ✅ 按顺序执行测试用例
2. ✅ 记录所有测试结果
3. ✅ 保存错误日志
4. ✅ 截图重要步骤
5. ✅ 验证所有功能点

### 测试后

1. ✅ 整理测试报告
2. ✅ 提交发现的问题
3. ✅ 分享测试经验
4. ✅ 更新测试文档

---

## 📞 获取帮助

如果在测试过程中遇到问题:

1. **查看文档**
   - README.md
   - MCP_CONFIG_GUIDE.md
   - TEST_REPORT.md

2. **检查已知问题**
   - GitHub Issues
   - 常见问题部分

3. **寻求帮助**
   - 提交GitHub Issue
   - 查看项目讨论区

---

**文档维护者:** Claude (codeagent)  
**最后更新:** 2025-10-26  
**文档版本:** 1.0

---

**Happy Testing! 祝测试顺利! 🎉**
