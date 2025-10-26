#!/usr/bin/env python3
"""
Travel Itinerary API Usage Examples
Demonstrates how to use the travel itinerary endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def example_1_list_itineraries():
    """List all available itineraries"""
    print("=" * 80)
    print("示例 1: 获取所有可用的旅行攻略")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/api/itinerary/list")
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['success']:
        print(f"找到 {data['count']} 个旅行攻略:")
        for itinerary in data['itineraries']:
            print(f"\n路线代码: {itinerary['route_key']}")
            print(f"标题: {itinerary['title']}")
            print(f"描述: {itinerary['description']}")
            print(f"天数: {itinerary['duration_days']}天")
            print(f"起点: {itinerary['origin']} → 终点: {itinerary['destination']}")
            print(f"预计费用: {itinerary['estimated_cost']}")
    
    print()

def example_2_get_beijing_kunming_itinerary():
    """Get Beijing to Kunming 10-day itinerary"""
    print("=" * 80)
    print("示例 2: 获取北京到昆明10天旅行攻略")
    print("=" * 80)
    
    route_key = "北京-昆明-10天"
    response = requests.get(f"{BASE_URL}/api/itinerary/{route_key}")
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['success']:
        itinerary = data['itinerary']
        print(f"\n标题: {itinerary['title']}")
        print(f"描述: {itinerary['description']}")
        print(f"天数: {itinerary['duration_days']}天")
        print(f"预计费用: {itinerary['total_estimated_cost']}")
        
        print(f"\n交通方式:")
        trans = itinerary['transportation']
        print(f"去程: {trans['to_destination']['method']} ({trans['to_destination']['duration']})")
        print(f"返程: {trans['return']['method']} ({trans['return']['duration']})")
        
        print(f"\n每日行程概览:")
        for day in itinerary['days'][:3]:
            print(f"Day {day['day']}: {day['title']} - {day['location']}")
        print("...")
        
        print("\n格式化消息 (前500字符):")
        print(data['formatted_message'][:500])
        print("...")
    
    print()

def example_3_navigate_with_itinerary():
    """Get itinerary and open navigation"""
    print("=" * 80)
    print("示例 3: 获取旅行攻略并打开导航")
    print("=" * 80)
    
    request_data = {
        "origin": "北京",
        "destination": "昆明",
        "mode": "driving",
        "map_type": "baidu"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/itinerary/navigate",
        json=request_data
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['success']:
        print(f"\n导航已打开: {data['navigation_opened']}")
        print(f"导航URL: {data['navigation_url'][:80]}...")
        print(f"起点: {data['origin']}")
        print(f"终点: {data['destination']}")
        
        if data.get('has_itinerary'):
            print(f"\n找到旅行攻略!")
            print(f"路线代码: {data['route_key']}")
            itinerary = data['itinerary']
            print(f"标题: {itinerary['title']}")
            print(f"天数: {itinerary['duration_days']}天")
        else:
            print(f"\n{data.get('message', '暂无此路线的旅行攻略')}")
    
    print()

def example_4_get_destination_info():
    """Get weather and recommendations for destination"""
    print("=" * 80)
    print("示例 4: 获取目的地天气和旅游建议")
    print("=" * 80)
    
    location = "昆明"
    response = requests.get(f"{BASE_URL}/api/destination-info/{location}")
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['success']:
        print(f"\n地点: {data['location']}")
        
        if 'recommendations' in data:
            recs = data['recommendations']
            print(f"\n最佳旅游时间: {recs.get('best_time', 'N/A')}")
            
            if recs.get('attractions'):
                print(f"\n热门景点 (前3个):")
                for attraction in recs['attractions'][:3]:
                    print(f"  • {attraction}")
            
            if recs.get('cuisine'):
                print(f"\n特色美食 (前3个):")
                for food in recs['cuisine'][:3]:
                    print(f"  • {food}")
    
    print()

def run_all_examples():
    """Run all examples"""
    print("\n🚀 旅行攻略 API 使用示例\n")
    print("请确保 API 服务器正在运行: python src/ai_navigator_api.py\n")
    
    try:
        example_1_list_itineraries()
        example_2_get_beijing_kunming_itinerary()
        
        print("\n⚠️  以下示例会打开浏览器,按 Enter 继续或 Ctrl+C 退出...")
        input()
        
        example_3_navigate_with_itinerary()
        example_4_get_destination_info()
        
        print("=" * 80)
        print("✓ 所有示例执行完成!")
        print("=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到 API 服务器")
        print("请先启动服务器: python src/ai_navigator_api.py")
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_examples()
