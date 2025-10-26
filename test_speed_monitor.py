#!/usr/bin/env python3
"""
Test script for Speed Monitor functionality
"""
import sys
sys.path.insert(0, 'src')

from speed_monitor import SpeedMonitor


def test_speed_monitor():
    print("\n" + "="*70)
    print("超速监控功能测试 / Speed Monitor Test")
    print("="*70 + "\n")
    
    monitor = SpeedMonitor()
    
    print("测试 1: 正常速度检测")
    print("-" * 70)
    result = monitor.check_speed(current_speed=50, road_type="城市道路")
    print(monitor.format_speed_alert(result))
    print("\n")
    
    print("测试 2: 轻微超速检测")
    print("-" * 70)
    result = monitor.check_speed(current_speed=68, road_type="城市道路")
    print(monitor.format_speed_alert(result))
    print("\n")
    
    print("测试 3: 中度超速检测")
    print("-" * 70)
    result = monitor.check_speed(current_speed=78, road_type="城市道路")
    print(monitor.format_speed_alert(result))
    print("\n")
    
    print("测试 4: 严重超速检测")
    print("-" * 70)
    result = monitor.check_speed(current_speed=95, road_type="城市道路")
    print(monitor.format_speed_alert(result))
    print("\n")
    
    print("测试 5: 高速公路速度检测")
    print("-" * 70)
    result = monitor.check_speed(current_speed=110, road_type="高速公路")
    print(monitor.format_speed_alert(result))
    print("\n")
    
    print("测试 6: 学校区域超速检测")
    print("-" * 70)
    result = monitor.check_speed(current_speed=40, location="学校附近")
    print(monitor.format_speed_alert(result))
    print("\n")
    
    print("测试 7: 行程速度提醒")
    print("-" * 70)
    reminder = monitor.create_speed_reminder_message(
        origin="北京天安门",
        destination="上海东方明珠",
        route_type="driving"
    )
    print(reminder)
    print("\n")
    
    print("测试 8: 获取导航速度信息")
    print("-" * 70)
    info = monitor.get_navigation_speed_info("driving")
    print(f"导航类型: {info['route_type']}")
    print(f"监控启用: {info['monitoring_enabled']}")
    print(f"推荐速度: {info['recommended_speed']} km/h")
    print(f"最高速度: {info['max_speed']} km/h")
    print("\n")
    
    print("测试 9: 城市限速查询 - 北京")
    print("-" * 70)
    limits = monitor.get_speed_limit_by_city("北京")
    for road_type, limit in limits.items():
        print(f"{road_type}: {limit} km/h")
    print("\n")
    
    print("测试 10: 城市限速查询 - 上海")
    print("-" * 70)
    limits = monitor.get_speed_limit_by_city("上海")
    for road_type, limit in limits.items():
        print(f"{road_type}: {limit} km/h")
    print("\n")
    
    print("="*70)
    print("✅ 所有测试完成!")
    print("="*70 + "\n")


def test_api_examples():
    print("\n" + "="*70)
    print("API 调用示例 / API Usage Examples")
    print("="*70 + "\n")
    
    print("示例 1: 检查当前速度")
    print("-" * 70)
    print("""
curl -X POST "http://localhost:8000/api/speed/check" \\
  -H "Content-Type: application/json" \\
  -d '{
    "current_speed": 75,
    "road_type": "城市道路"
  }'
""")
    
    print("\n示例 2: 获取行程速度提醒")
    print("-" * 70)
    print("""
curl -X POST "http://localhost:8000/api/speed/reminder" \\
  -H "Content-Type: application/json" \\
  -d '{
    "origin": "北京天安门",
    "destination": "上海东方明珠",
    "route_type": "driving"
  }'
""")
    
    print("\n示例 3: 查询城市限速信息")
    print("-" * 70)
    print("""
curl -X GET "http://localhost:8000/api/speed/limits/北京"
""")
    
    print("\n示例 4: MCP 工具调用 - 检查速度")
    print("-" * 70)
    print("""
check_speed_limit(
    current_speed=75,
    road_type="城市道路"
)
""")
    
    print("\n示例 5: MCP 工具调用 - 获取速度提醒")
    print("-" * 70)
    print("""
get_speed_reminder(
    origin="北京天安门",
    destination="上海东方明珠",
    route_type="driving"
)
""")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n🚗 超速监控功能测试程序")
    print("Speed Monitoring Feature Test Program\n")
    
    test_speed_monitor()
    
    test_api_examples()
    
    print("📝 使用说明:")
    print("1. 启动API服务器: python src/ai_navigator_api.py")
    print("2. 访问API文档: http://localhost:8000/docs")
    print("3. 测试速度检查API: 使用上述curl命令")
    print("4. 在MCP客户端中使用相应工具\n")
