#!/usr/bin/env python3
import sys
import requests

API_BASE = "http://localhost:8000"

def test_transportation_recommendation():
    print("=" * 60)
    print("测试1: 基础交通工具推荐 (北京到上海)")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/transportation/recommend",
        json={
            "origin": "北京",
            "destination": "上海",
            "trip_purpose": "商务",
            "luggage": "少量",
            "budget": "标准",
            "time_sensitive": False
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 请求成功")
        print(f"消息: {data['message']}")
        rec = data['recommendation']
        print(f"\n推荐方式: {rec['recommended_mode']}")
        print(f"推荐理由: {rec['recommendation_reason']}")
        print(f"预计距离: {rec['estimated_distance']}")
        print(f"预计时间: {rec['estimated_duration']}")
        print(f"预估费用: {rec['cost_estimate']}")
        print(f"备选方案: {rec['alternative_modes']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 60)
    print("测试2: 自然语言交通推荐")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/transportation/recommend/ai",
        json={
            "query": "从广州到深圳通勤，行李多，怎么去最方便?"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 请求成功")
        print(f"消息: {data['message']}")
        rec = data['recommendation']
        print(f"\n推荐方式: {rec['recommended_mode']}")
        print(f"推荐理由: {rec['recommendation_reason']}")
        print(f"出行提示: {rec['tips'][:3]}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 60)
    print("测试3: 短距离出行推荐")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/transportation/recommend/ai",
        json={
            "query": "从天安门到西单，经济出行"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 请求成功")
        rec = data['recommendation']
        print(f"推荐方式: {rec['recommended_mode']}")
        print(f"推荐理由: {rec['recommendation_reason']}")
        print(f"预估费用: {rec['cost_estimate']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 60)
    print("测试4: 获取所有交通方式")
    print("=" * 60)
    
    response = requests.get(f"{API_BASE}/api/transportation/modes")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 请求成功")
        print(f"消息: {data['message']}")
        print(f"交通方式数量: {len(data['modes'])}")
        for mode in data['modes'][:3]:
            print(f"\n- {mode['name']}:")
            print(f"  描述: {mode['description']}")
            print(f"  速度: {mode['typical_speed']}")
            print(f"  费用: {mode['cost_range']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 60)
    print("测试5: 紧急出行推荐")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/transportation/recommend",
        json={
            "origin": "成都",
            "destination": "重庆",
            "trip_purpose": "紧急",
            "time_sensitive": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 请求成功")
        rec = data['recommendation']
        print(f"推荐方式: {rec['recommended_mode']}")
        print(f"推荐理由: {rec['recommendation_reason']}")
        print(f"预计时间: {rec['estimated_duration']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("\n🚀 交通工具推荐功能测试\n")
    print("请确保API服务器正在运行 (python src/ai_navigator_api.py)")
    print("如果服务器未运行，测试将失败\n")
    
    try:
        test_transportation_recommendation()
        print("\n✅ 所有测试完成!")
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到API服务器")
        print("请先启动服务器: python src/ai_navigator_api.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {str(e)}")
        sys.exit(1)
