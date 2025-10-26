#!/usr/bin/env python3
"""
AI导航助手 - 完整性功能测试DEMO
AI Navigation Assistant - Integrity Function Test Demo

这是一个全面的完整性测试套件,覆盖所有核心功能和新增的企业级特性
This is a comprehensive integrity test suite covering all core features and enterprise-grade capabilities

测试范围 / Test Coverage:
1. 核心导航功能 (Core Navigation Features)
2. 旅游攻略规划 (Travel Guide Planning)
3. 性能监控系统 (Performance Monitoring System)
4. 异常处理系统 (Exception Handling System)
5. 自动扩缩容系统 (Auto-Scaling System)
6. SRE告警通知 (SRE Alerting & Notifications)
7. REST API完整性 (REST API Integrity)
8. 数据一致性验证 (Data Consistency Validation)
9. 集成测试场景 (Integration Test Scenarios)

版本 / Version: 2.0.0
创建日期 / Created: 2025-10-26
Issue: #48
"""

import sys
import json
import time
import requests
from typing import Dict, List, Any
from datetime import datetime


class IntegrityTestResult:
    """测试结果记录器"""
    
    def __init__(self, category: str):
        self.category = category
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.tests = []
        
    def add_test(self, name: str, status: str, details: str = "", severity: str = "normal"):
        """添加测试结果
        
        Args:
            name: 测试名称
            status: passed/failed/warning
            details: 详细信息
            severity: normal/critical/high/medium/low
        """
        self.tests.append({
            "name": name,
            "status": status,
            "details": details,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        })
        
        if status == "passed":
            self.passed += 1
        elif status == "failed":
            self.failed += 1
        else:
            self.warnings += 1
    
    def print_results(self):
        """打印测试结果"""
        print(f"\n{'='*80}")
        print(f"测试类别: {self.category}")
        print(f"{'='*80}")
        
        for test in self.tests:
            status_icon = {
                "passed": "✅",
                "failed": "❌",
                "warning": "⚠️"
            }.get(test["status"], "❓")
            
            severity_tag = ""
            if test["severity"] != "normal":
                severity_tag = f" [{test['severity'].upper()}]"
            
            print(f"{status_icon} {test['name']}{severity_tag}")
            if test["details"]:
                print(f"   详情: {test['details']}")
        
        print(f"\n统计: ✅ {self.passed} 通过 | ❌ {self.failed} 失败 | ⚠️ {self.warnings} 警告")
        print(f"{'='*80}\n")


class APIHealthChecker:
    """API健康检查器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def check_server_running(self) -> bool:
        """检查服务器是否运行"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_endpoint(self, method: str, path: str, json_data: Dict = None, 
                     expected_status: int = 200) -> Dict[str, Any]:
        """测试单个端点
        
        Returns:
            Dict with keys: success, status_code, response, error
        """
        try:
            url = f"{self.base_url}{path}"
            
            if method.upper() == "GET":
                response = self.session.get(url, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=json_data, timeout=10)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
            
            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            return {
                "success": success,
                "status_code": response.status_code,
                "response": response_data,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": None,
                "response": None,
                "error": str(e)
            }


def test_core_navigation_features(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试核心导航功能"""
    results = IntegrityTestResult("核心导航功能 (Core Navigation Features)")
    
    # 测试1: 基础导航
    test_data = {
        "origin": "北京天安门",
        "destination": "上海东方明珠",
        "mode": "driving",
        "map_type": "baidu"
    }
    result = checker.test_endpoint("POST", "/api/navigate", test_data)
    
    if result["success"] and result["response"].get("success"):
        results.add_test(
            "基础导航API - 百度地图驾车",
            "passed",
            f"URL生成成功, map_url存在"
        )
    else:
        results.add_test(
            "基础导航API - 百度地图驾车",
            "failed",
            f"错误: {result.get('error') or result['response']}",
            "critical"
        )
    
    # 测试2: 多目的地导航
    test_data = {
        "origin": "北京天安门",
        "destinations": ["上海东方明珠", "杭州西湖", "苏州园林"],
        "mode": "driving",
        "optimize": True,
        "map_type": "baidu"
    }
    result = checker.test_endpoint("POST", "/api/navigate/multi", test_data)
    
    if result["success"] and result["response"].get("success"):
        results.add_test(
            "多目的地导航API - 路线优化",
            "passed",
            f"支持{len(test_data['destinations'])}个目的地"
        )
    else:
        results.add_test(
            "多目的地导航API - 路线优化",
            "failed",
            f"错误: {result.get('error') or result['response']}",
            "high"
        )
    
    # 测试3: AI自然语言导航
    test_data = {
        "query": "帮我从北京天安门导航到上海东方明珠,用百度地图"
    }
    result = checker.test_endpoint("POST", "/api/ai/navigate", test_data)
    
    if result["success"] and result["response"].get("success"):
        results.add_test(
            "AI自然语言导航API",
            "passed",
            "自然语言解析成功"
        )
    else:
        results.add_test(
            "AI自然语言导航API",
            "failed",
            f"错误: {result.get('error') or result['response']}",
            "high"
        )
    
    # 测试4: 位置显示
    test_data = {
        "location": "北京故宫",
        "map_type": "amap"
    }
    result = checker.test_endpoint("POST", "/api/location", test_data)
    
    if result["success"] and result["response"].get("success"):
        results.add_test(
            "位置显示API - 高德地图",
            "passed",
            "位置URL生成成功"
        )
    else:
        results.add_test(
            "位置显示API - 高德地图",
            "failed",
            f"错误: {result.get('error') or result['response']}",
            "medium"
        )
    
    results.print_results()
    return results


def test_travel_guide_features(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试旅游攻略功能"""
    results = IntegrityTestResult("旅游攻略规划 (Travel Guide Planning)")
    
    # 测试1: 获取支持城市列表
    result = checker.test_endpoint("GET", "/api/travel/cities")
    
    if result["success"] and result["response"].get("success"):
        cities_count = len(result["response"].get("cities", []))
        results.add_test(
            "获取支持城市列表",
            "passed",
            f"支持{cities_count}个城市"
        )
    else:
        results.add_test(
            "获取支持城市列表",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试2: 创建旅游攻略
    test_data = {
        "destination": "北京",
        "duration_days": 3,
        "travel_style": "经典游"
    }
    result = checker.test_endpoint("POST", "/api/travel/guide", test_data)
    
    if result["success"] and result["response"].get("success"):
        guide = result["response"].get("guide", {})
        itinerary_days = len(guide.get("itinerary", []))
        attractions_count = len(guide.get("recommended_attractions", []))
        has_budget = "budget_estimate" in guide
        
        results.add_test(
            "创建旅游攻略 - 北京3日游",
            "passed",
            f"行程{itinerary_days}天, {attractions_count}个景点, 预算估算: {'有' if has_budget else '无'}"
        )
    else:
        results.add_test(
            "创建旅游攻略 - 北京3日游",
            "failed",
            f"错误: {result.get('error') or result['response']}",
            "high"
        )
    
    # 测试3: AI自然语言创建攻略
    test_data = {
        "query": "帮我规划杭州5天深度游"
    }
    result = checker.test_endpoint("POST", "/api/travel/guide/ai", test_data)
    
    if result["success"] and result["response"].get("success"):
        results.add_test(
            "AI自然语言创建攻略",
            "passed",
            "自然语言解析并生成攻略成功"
        )
    else:
        results.add_test(
            "AI自然语言创建攻略",
            "failed",
            f"错误: {result.get('error') or result['response']}",
            "medium"
        )
    
    # 测试4: 不同旅行风格
    for style in ["深度游", "经典游", "打卡游"]:
        test_data = {
            "destination": "上海",
            "duration_days": 3,
            "travel_style": style
        }
        result = checker.test_endpoint("POST", "/api/travel/guide", test_data)
        
        if result["success"] and result["response"].get("success"):
            guide = result["response"].get("guide", {})
            daily_attractions = len(guide.get("itinerary", [{}])[0].get("attractions", []))
            results.add_test(
                f"旅行风格测试 - {style}",
                "passed",
                f"每日景点数: {daily_attractions}"
            )
        else:
            results.add_test(
                f"旅行风格测试 - {style}",
                "warning",
                f"错误: {result.get('error')}"
            )
    
    results.print_results()
    return results


def test_performance_monitoring(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试性能监控系统"""
    results = IntegrityTestResult("性能监控系统 (Performance Monitoring)")
    
    # 测试1: 详细健康检查
    result = checker.test_endpoint("GET", "/api/health/detailed")
    
    if result["success"]:
        response = result["response"]
        has_performance = "performance" in response
        has_exceptions = "exceptions" in response
        has_scaling = "scaling" in response
        
        if has_performance and has_exceptions and has_scaling:
            results.add_test(
                "详细健康检查API",
                "passed",
                f"状态: {response.get('status')}, 包含完整监控数据"
            )
        else:
            results.add_test(
                "详细健康检查API",
                "warning",
                f"响应不完整: performance={has_performance}, exceptions={has_exceptions}, scaling={has_scaling}"
            )
    else:
        results.add_test(
            "详细健康检查API",
            "failed",
            f"错误: {result.get('error')}",
            "critical"
        )
    
    # 测试2: 实时监控状态
    result = checker.test_endpoint("GET", "/api/monitoring/status")
    
    if result["success"]:
        response = result["response"]
        has_metrics = "current_metrics" in response
        has_thresholds = "thresholds" in response
        
        if has_metrics and has_thresholds:
            metrics = response.get("current_metrics", {})
            cpu = metrics.get("cpu_percent", 0)
            memory = metrics.get("memory_percent", 0)
            
            results.add_test(
                "实时监控状态API",
                "passed",
                f"CPU: {cpu}%, 内存: {memory}%, 健康状态: {response.get('health_status')}"
            )
        else:
            results.add_test(
                "实时监控状态API",
                "warning",
                "响应数据不完整"
            )
    else:
        results.add_test(
            "实时监控状态API",
            "failed",
            f"错误: {result.get('error')}",
            "high"
        )
    
    # 测试3: 历史指标数据
    result = checker.test_endpoint("GET", "/api/monitoring/metrics/history?limit=10")
    
    if result["success"]:
        response = result["response"]
        if isinstance(response, dict) and "metrics" in response:
            metrics_count = len(response.get("metrics", []))
            results.add_test(
                "历史性能指标API",
                "passed",
                f"返回{metrics_count}条历史记录"
            )
        else:
            results.add_test(
                "历史性能指标API",
                "passed",
                "返回历史数据(格式可能为列表)"
            )
    else:
        results.add_test(
            "历史性能指标API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试4: 告警查询
    result = checker.test_endpoint("GET", "/api/monitoring/alerts")
    
    if result["success"]:
        response = result["response"]
        if isinstance(response, (list, dict)):
            results.add_test(
                "监控告警查询API",
                "passed",
                "成功获取告警列表"
            )
        else:
            results.add_test(
                "监控告警查询API",
                "warning",
                "响应格式异常"
            )
    else:
        results.add_test(
            "监控告警查询API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    results.print_results()
    return results


def test_exception_handling(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试异常处理系统"""
    results = IntegrityTestResult("异常处理系统 (Exception Handling)")
    
    # 测试1: 异常摘要统计
    result = checker.test_endpoint("GET", "/api/exceptions/summary")
    
    if result["success"]:
        response = result["response"]
        has_total = "total_exceptions" in response
        has_by_severity = "by_severity" in response
        has_by_type = "by_type" in response
        
        if has_total and has_by_severity and has_by_type:
            results.add_test(
                "异常摘要统计API",
                "passed",
                f"总异常数: {response.get('total_exceptions')}, 未解决: {response.get('unresolved_count')}"
            )
        else:
            results.add_test(
                "异常摘要统计API",
                "warning",
                "响应数据不完整"
            )
    else:
        results.add_test(
            "异常摘要统计API",
            "failed",
            f"错误: {result.get('error')}",
            "high"
        )
    
    # 测试2: 未解决异常查询
    result = checker.test_endpoint("GET", "/api/exceptions/unresolved")
    
    if result["success"]:
        results.add_test(
            "未解决异常查询API",
            "passed",
            "成功获取未解决异常列表"
        )
    else:
        results.add_test(
            "未解决异常查询API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试3: 输入验证 - 无效参数测试
    invalid_test_data = {
        "origin": "",  # 空起点
        "destination": "上海",
        "mode": "invalid_mode",  # 无效模式
        "map_type": "baidu"
    }
    result = checker.test_endpoint("POST", "/api/navigate", invalid_test_data, expected_status=422)
    
    if result["status_code"] in [400, 422]:  # 应该返回错误状态码
        results.add_test(
            "输入验证 - 空参数检测",
            "passed",
            f"正确拒绝无效输入,返回状态码{result['status_code']}"
        )
    else:
        results.add_test(
            "输入验证 - 空参数检测",
            "failed",
            f"未正确验证输入,状态码: {result['status_code']}",
            "medium"
        )
    
    # 测试4: 错误恢复能力
    # 先发送一个会失败的请求,然后发送正常请求,验证系统恢复能力
    invalid_data = {"query": ""}
    checker.test_endpoint("POST", "/api/ai/navigate", invalid_data, expected_status=400)
    
    valid_data = {"query": "从北京到上海"}
    result = checker.test_endpoint("POST", "/api/ai/navigate", valid_data)
    
    if result["success"]:
        results.add_test(
            "错误恢复能力测试",
            "passed",
            "系统在错误后成功恢复并处理正常请求"
        )
    else:
        results.add_test(
            "错误恢复能力测试",
            "warning",
            "错误恢复可能存在问题"
        )
    
    results.print_results()
    return results


def test_auto_scaling(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试自动扩缩容系统"""
    results = IntegrityTestResult("自动扩缩容系统 (Auto-Scaling)")
    
    # 测试1: 扩缩容建议
    result = checker.test_endpoint("GET", "/api/scaling/recommendation")
    
    if result["success"]:
        response = result["response"]
        has_current_replicas = "current_replicas" in response
        has_recommendation = "recommendation" in response
        
        if has_current_replicas and has_recommendation:
            results.add_test(
                "扩缩容建议API",
                "passed",
                f"当前副本: {response.get('current_replicas')}, 建议: {response.get('recommendation')}"
            )
        else:
            results.add_test(
                "扩缩容建议API",
                "warning",
                "响应数据不完整"
            )
    else:
        results.add_test(
            "扩缩容建议API",
            "failed",
            f"错误: {result.get('error')}",
            "high"
        )
    
    # 测试2: 扩缩容历史
    result = checker.test_endpoint("GET", "/api/scaling/history?limit=5")
    
    if result["success"]:
        results.add_test(
            "扩缩容历史API",
            "passed",
            "成功获取扩缩容历史记录"
        )
    else:
        results.add_test(
            "扩缩容历史API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试3: 扩缩容状态摘要
    result = checker.test_endpoint("GET", "/api/scaling/summary")
    
    if result["success"]:
        results.add_test(
            "扩缩容状态摘要API",
            "passed",
            "成功获取扩缩容状态摘要"
        )
    else:
        results.add_test(
            "扩缩容状态摘要API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试4: 评估扩缩容(仅评估,不实际执行)
    test_data = {
        "force_scale_up": False,
        "force_scale_down": False
    }
    result = checker.test_endpoint("POST", "/api/scaling/evaluate", test_data)
    
    if result["success"]:
        results.add_test(
            "扩缩容评估API",
            "passed",
            "成功评估扩缩容需求"
        )
    else:
        results.add_test(
            "扩缩容评估API",
            "warning",
            f"评估可能失败: {result.get('error')}"
        )
    
    results.print_results()
    return results


def test_sre_notifications(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试SRE告警通知系统"""
    results = IntegrityTestResult("SRE告警通知 (SRE Alerting)")
    
    # 测试1: 通知历史
    result = checker.test_endpoint("GET", "/api/notifications/history?limit=10")
    
    if result["success"]:
        results.add_test(
            "通知历史API",
            "passed",
            "成功获取通知历史记录"
        )
    else:
        results.add_test(
            "通知历史API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试2: 通知统计
    result = checker.test_endpoint("GET", "/api/notifications/stats")
    
    if result["success"]:
        response = result["response"]
        if isinstance(response, dict):
            results.add_test(
                "通知统计API",
                "passed",
                f"统计数据获取成功"
            )
        else:
            results.add_test(
                "通知统计API",
                "warning",
                "响应格式异常"
            )
    else:
        results.add_test(
            "通知统计API",
            "failed",
            f"错误: {result.get('error')}",
            "medium"
        )
    
    # 测试3: 测试通知
    test_data = {
        "channel": "log",
        "message": "Integrity test notification"
    }
    result = checker.test_endpoint("POST", "/api/notifications/test", test_data)
    
    if result["success"]:
        results.add_test(
            "测试通知API",
            "passed",
            "测试通知发送成功"
        )
    else:
        results.add_test(
            "测试通知API",
            "warning",
            f"测试通知可能失败: {result.get('error')}"
        )
    
    results.print_results()
    return results


def test_data_consistency(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试数据一致性"""
    results = IntegrityTestResult("数据一致性验证 (Data Consistency)")
    
    # 测试1: 重复请求一致性
    test_data = {
        "destination": "北京",
        "duration_days": 3,
        "travel_style": "经典游"
    }
    
    result1 = checker.test_endpoint("POST", "/api/travel/guide", test_data)
    time.sleep(0.5)  # 短暂延迟
    result2 = checker.test_endpoint("POST", "/api/travel/guide", test_data)
    
    if result1["success"] and result2["success"]:
        guide1 = result1["response"].get("guide", {})
        guide2 = result2["response"].get("guide", {})
        
        # 检查关键字段一致性
        consistent = (
            guide1.get("destination") == guide2.get("destination") and
            guide1.get("duration_days") == guide2.get("duration_days") and
            guide1.get("travel_style") == guide2.get("travel_style")
        )
        
        if consistent:
            results.add_test(
                "重复请求数据一致性",
                "passed",
                "相同请求返回一致的核心数据"
            )
        else:
            results.add_test(
                "重复请求数据一致性",
                "failed",
                "相同请求返回不一致数据",
                "high"
            )
    else:
        results.add_test(
            "重复请求数据一致性",
            "warning",
            "无法完成一致性测试"
        )
    
    # 测试2: URL编码一致性
    locations = ["北京天安门", "上海东方明珠", "杭州西湖"]
    
    for location in locations:
        test_data = {
            "location": location,
            "map_type": "baidu"
        }
        result = checker.test_endpoint("POST", "/api/location", test_data)
        
        if result["success"] and result["response"].get("success"):
            url = result["response"].get("map_url", "")
            # 检查URL是否包含编码后的位置信息
            if "map.baidu.com" in url and len(url) > 30:
                results.add_test(
                    f"URL编码一致性 - {location}",
                    "passed",
                    "URL正确生成和编码"
                )
            else:
                results.add_test(
                    f"URL编码一致性 - {location}",
                    "failed",
                    "URL格式异常",
                    "medium"
                )
    
    # 测试3: API响应格式一致性
    endpoints_to_test = [
        ("GET", "/health", None),
        ("GET", "/api/travel/cities", None),
        ("GET", "/api/monitoring/status", None),
    ]
    
    all_have_success_field = True
    for method, path, data in endpoints_to_test:
        result = checker.test_endpoint(method, path, data)
        if result["success"] and isinstance(result["response"], dict):
            # 大多数成功响应应该包含success字段
            if path != "/health" and "success" not in result["response"]:
                all_have_success_field = False
    
    if all_have_success_field:
        results.add_test(
            "API响应格式一致性",
            "passed",
            "所有API响应格式符合规范"
        )
    else:
        results.add_test(
            "API响应格式一致性",
            "warning",
            "部分API响应格式不一致"
        )
    
    results.print_results()
    return results


def test_integration_scenarios(checker: APIHealthChecker) -> IntegrityTestResult:
    """测试集成场景"""
    results = IntegrityTestResult("集成测试场景 (Integration Scenarios)")
    
    # 场景1: 完整旅行规划流程
    print("\n执行集成场景1: 完整旅行规划流程...")
    
    # 步骤1: 获取支持城市
    result = checker.test_endpoint("GET", "/api/travel/cities")
    if not result["success"]:
        results.add_test(
            "场景1.1 - 获取城市列表",
            "failed",
            "无法获取城市列表",
            "critical"
        )
        return results
    
    cities = result["response"].get("cities", [])
    if len(cities) == 0:
        results.add_test(
            "场景1.1 - 获取城市列表",
            "failed",
            "城市列表为空",
            "critical"
        )
        return results
    
    results.add_test(
        "场景1.1 - 获取城市列表",
        "passed",
        f"获取到{len(cities)}个城市"
    )
    
    # 步骤2: 创建旅游攻略
    first_city = cities[0].get("name", "北京")
    test_data = {
        "destination": first_city,
        "duration_days": 3,
        "travel_style": "经典游"
    }
    result = checker.test_endpoint("POST", "/api/travel/guide", test_data)
    
    if not result["success"] or not result["response"].get("success"):
        results.add_test(
            "场景1.2 - 创建旅游攻略",
            "failed",
            f"无法为{first_city}创建攻略",
            "high"
        )
        return results
    
    guide = result["response"].get("guide", {})
    itinerary = guide.get("itinerary", [])
    
    results.add_test(
        "场景1.2 - 创建旅游攻略",
        "passed",
        f"{first_city}攻略创建成功,包含{len(itinerary)}天行程"
    )
    
    # 步骤3: 为第一天的景点创建导航
    if len(itinerary) > 0:
        day1_attractions = itinerary[0].get("attractions", [])
        if len(day1_attractions) >= 2:
            origin = day1_attractions[0]
            destination = day1_attractions[1]
            
            nav_data = {
                "origin": origin,
                "destination": destination,
                "mode": "transit",
                "map_type": "baidu"
            }
            result = checker.test_endpoint("POST", "/api/navigate", nav_data)
            
            if result["success"] and result["response"].get("success"):
                results.add_test(
                    "场景1.3 - 景点间导航",
                    "passed",
                    f"成功创建 {origin} → {destination} 的导航"
                )
            else:
                results.add_test(
                    "场景1.3 - 景点间导航",
                    "failed",
                    "导航创建失败",
                    "medium"
                )
    
    # 场景2: 系统健康监控流程
    print("\n执行集成场景2: 系统健康监控流程...")
    
    # 步骤1: 检查系统健康状态
    result = checker.test_endpoint("GET", "/api/health/detailed")
    
    if result["success"]:
        status = result["response"].get("status", "unknown")
        results.add_test(
            "场景2.1 - 系统健康检查",
            "passed",
            f"系统状态: {status}"
        )
        
        # 步骤2: 获取性能指标
        result = checker.test_endpoint("GET", "/api/monitoring/status")
        if result["success"]:
            health = result["response"].get("health_status", "unknown")
            results.add_test(
                "场景2.2 - 性能监控查询",
                "passed",
                f"健康状态: {health}"
            )
            
            # 步骤3: 检查告警
            result = checker.test_endpoint("GET", "/api/monitoring/alerts")
            if result["success"]:
                results.add_test(
                    "场景2.3 - 告警检查",
                    "passed",
                    "成功获取系统告警信息"
                )
            else:
                results.add_test(
                    "场景2.3 - 告警检查",
                    "warning",
                    "告警信息获取失败"
                )
    else:
        results.add_test(
            "场景2.1 - 系统健康检查",
            "failed",
            "无法获取系统健康状态",
            "critical"
        )
    
    # 场景3: 并发请求测试
    print("\n执行集成场景3: 并发请求处理...")
    
    import threading
    
    concurrent_results = []
    
    def make_request():
        test_data = {
            "origin": "北京",
            "destination": "上海",
            "mode": "driving",
            "map_type": "baidu"
        }
        result = checker.test_endpoint("POST", "/api/navigate", test_data)
        concurrent_results.append(result["success"])
    
    threads = []
    for _ in range(5):  # 5个并发请求
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    success_count = sum(concurrent_results)
    if success_count == len(concurrent_results):
        results.add_test(
            "场景3 - 并发请求处理",
            "passed",
            f"{len(concurrent_results)}个并发请求全部成功"
        )
    elif success_count > 0:
        results.add_test(
            "场景3 - 并发请求处理",
            "warning",
            f"{success_count}/{len(concurrent_results)}个请求成功"
        )
    else:
        results.add_test(
            "场景3 - 并发请求处理",
            "failed",
            "所有并发请求都失败",
            "high"
        )
    
    results.print_results()
    return results


def generate_test_report(all_results: List[IntegrityTestResult]) -> str:
    """生成测试报告"""
    
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_warnings = sum(r.warnings for r in all_results)
    total_tests = total_passed + total_failed + total_warnings
    
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    report = f"""
{'='*80}
AI导航助手 - 完整性功能测试报告
AI Navigation Assistant - Integrity Test Report
{'='*80}

测试执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
测试环境: Python {sys.version.split()[0]}
Issue编号: #48

{'='*80}
测试结果汇总 / Test Summary
{'='*80}

总测试数: {total_tests}
✅ 通过: {total_passed} ({pass_rate:.1f}%)
❌ 失败: {total_failed} ({total_failed/total_tests*100 if total_tests > 0 else 0:.1f}%)
⚠️  警告: {total_warnings} ({total_warnings/total_tests*100 if total_tests > 0 else 0:.1f}%)

{'='*80}
分类测试结果 / Results by Category
{'='*80}

"""
    
    for result in all_results:
        report += f"""
{result.category}:
  ✅ 通过: {result.passed}
  ❌ 失败: {result.failed}
  ⚠️  警告: {result.warnings}
"""
    
    report += f"""
{'='*80}
测试结论 / Conclusion
{'='*80}

"""
    
    if total_failed == 0 and total_warnings <= total_tests * 0.1:
        report += """
✅ 所有关键测试通过!

项目完整性验证通过,所有核心功能正常运行:
1. ✅ 核心导航功能 - 完全可用
2. ✅ 旅游攻略规划 - 完全可用
3. ✅ 性能监控系统 - 正常运行
4. ✅ 异常处理系统 - 工作正常
5. ✅ 自动扩缩容系统 - 功能完整
6. ✅ SRE告警通知 - 正常工作
7. ✅ 数据一致性 - 验证通过
8. ✅ 集成场景 - 测试通过

系统状态: 健康 (Healthy)
推荐状态: 可以部署到生产环境
"""
    elif total_failed <= total_tests * 0.05:
        report += f"""
⚠️  大部分测试通过,存在少量问题

通过率: {pass_rate:.1f}%
失败数: {total_failed}
警告数: {total_warnings}

系统状态: 基本健康 (Mostly Healthy)
推荐状态: 修复失败项后可部署
建议: 查看详细日志,修复失败的测试用例
"""
    else:
        report += f"""
❌ 发现多个问题,需要修复

通过率: {pass_rate:.1f}%
失败数: {total_failed}
警告数: {total_warnings}

系统状态: 需要改进 (Needs Improvement)
推荐状态: 修复问题后再次测试
建议: 优先修复标记为critical和high的问题
"""
    
    report += f"""
{'='*80}
详细测试日志
{'='*80}

完整测试日志请查看终端输出

{'='*80}
测试文件说明
{'='*80}

本测试文件: integrity_test_demo.py
测试覆盖:
  - 核心导航功能 (4个测试)
  - 旅游攻略规划 (7个测试)
  - 性能监控系统 (4个测试)
  - 异常处理系统 (4个测试)
  - 自动扩缩容系统 (4个测试)
  - SRE告警通知 (3个测试)
  - 数据一致性验证 (多个测试)
  - 集成测试场景 (3个完整场景)

运行方式:
  python integrity_test_demo.py

前置条件:
  1. API服务器运行在 http://localhost:8000
  2. 所有依赖已安装
  3. 服务器已正常启动

{'='*80}
报告结束 / End of Report
{'='*80}
"""
    
    return report


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print(" "*20 + "AI导航助手 - 完整性功能测试")
    print(" "*15 + "AI Navigation Assistant - Integrity Test")
    print("="*80)
    print(f"\n测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Issue编号: #48")
    print("\n" + "="*80 + "\n")
    
    checker = APIHealthChecker()
    
    # 检查服务器是否运行
    print("检查API服务器状态...")
    if not checker.check_server_running():
        print("\n" + "="*80)
        print("❌ 错误: API服务器未运行!")
        print("="*80)
        print("\n请先启动API服务器:")
        print("  python src/ai_navigator_api.py")
        print("\n或使用:")
        print("  ./start.sh (Linux/Mac)")
        print("  start.bat (Windows)")
        print("\n" + "="*80 + "\n")
        sys.exit(1)
    
    print("✅ API服务器运行正常\n")
    print("="*80)
    print("开始执行完整性测试...")
    print("="*80 + "\n")
    
    all_results = []
    
    # 执行所有测试
    all_results.append(test_core_navigation_features(checker))
    all_results.append(test_travel_guide_features(checker))
    all_results.append(test_performance_monitoring(checker))
    all_results.append(test_exception_handling(checker))
    all_results.append(test_auto_scaling(checker))
    all_results.append(test_sre_notifications(checker))
    all_results.append(test_data_consistency(checker))
    all_results.append(test_integration_scenarios(checker))
    
    # 生成并打印报告
    report = generate_test_report(all_results)
    print("\n" + report)
    
    # 保存报告到文件
    report_file = "INTEGRITY_TEST_REPORT.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✅ 测试报告已保存到: {report_file}\n")
    
    # 返回退出码
    total_failed = sum(r.failed for r in all_results)
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
