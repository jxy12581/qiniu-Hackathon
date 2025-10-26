#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000"


def test_get_supported_cities():
    print("\n" + "="*60)
    print("测试 1: 获取支持的城市列表")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/travel/cities")
    result = response.json()
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert response.status_code == 200
    assert result["success"] == True
    assert len(result["cities"]) > 0
    print("✓ 测试通过")


def test_create_travel_guide_basic():
    print("\n" + "="*60)
    print("测试 2: 创建基础旅游攻略 (北京3日游)")
    print("="*60)
    
    request_data = {
        "destination": "北京",
        "duration_days": 3,
        "travel_style": "经典游"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/travel/guide",
        json=request_data
    )
    result = response.json()
    
    print(f"状态码: {response.status_code}")
    print(f"消息: {result.get('message')}")
    
    if response.status_code == 200:
        guide = result["guide"]
        print(f"\n目的地: {guide['destination']}")
        print(f"行程天数: {guide['duration_days']}")
        print(f"旅行风格: {guide['travel_style']}")
        print(f"最佳季节: {guide['best_season']}")
        
        print(f"\n推荐景点 ({len(guide['recommended_attractions'])}个):")
        for attr in guide['recommended_attractions']:
            print(f"  • {attr['name']} - {attr['category']}")
            print(f"    {attr['description']}")
            print(f"    建议游览时间: {attr['recommended_duration']}")
            print(f"    门票: {attr['entrance_fee']}")
        
        print(f"\n每日行程:")
        for day in guide['itinerary']:
            print(f"\n  第{day['day']}天 ({day['date']}):")
            for activity in day['activities']:
                print(f"    - {activity}")
            print(f"    备注: {day['notes']}")
        
        print(f"\n预算估算:")
        budget = guide['budget_estimate']
        print(f"  交通: ¥{budget['transportation']}")
        print(f"  住宿: ¥{budget['accommodation']}")
        print(f"  餐饮: ¥{budget['food']}")
        print(f"  门票: ¥{budget['tickets']}")
        print(f"  购物: ¥{budget['shopping']}")
        print(f"  总计: ¥{budget['total']}")
        
        print(f"\n旅行建议:")
        for tip in guide['travel_tips']:
            print(f"  • {tip}")
        
        assert result["success"] == True
        assert guide["duration_days"] == 3
        assert len(guide["itinerary"]) == 3
        print("\n✓ 测试通过")
    else:
        print(f"错误: {result}")


def test_create_travel_guide_with_date():
    print("\n" + "="*60)
    print("测试 3: 创建带日期的旅游攻略 (上海5日深度游)")
    print("="*60)
    
    request_data = {
        "destination": "上海",
        "duration_days": 5,
        "travel_style": "深度游",
        "start_date": "2025-05-01"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/travel/guide",
        json=request_data
    )
    result = response.json()
    
    print(f"状态码: {response.status_code}")
    print(f"消息: {result.get('message')}")
    
    if response.status_code == 200:
        guide = result["guide"]
        print(f"\n目的地: {guide['destination']}")
        print(f"行程天数: {guide['duration_days']}")
        print(f"旅行风格: {guide['travel_style']}")
        
        print(f"\n每日行程:")
        for day in guide['itinerary']:
            print(f"  第{day['day']}天 ({day['date']}): {', '.join(day['attractions'])}")
        
        print(f"\n总预算: ¥{guide['budget_estimate']['total']}")
        
        assert result["success"] == True
        assert guide["duration_days"] == 5
        assert guide["travel_style"] == "深度游"
        print("\n✓ 测试通过")
    else:
        print(f"错误: {result}")


def test_ai_travel_guide():
    print("\n" + "="*60)
    print("测试 4: AI自然语言创建旅游攻略")
    print("="*60)
    
    test_queries = [
        "帮我规划杭州3天游",
        "我想去成都玩5天，深度游",
        "西安4日游攻略",
        "北京7天打卡游"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        
        request_data = {"query": query}
        response = requests.post(
            f"{BASE_URL}/api/travel/guide/ai",
            json=request_data
        )
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            guide = result["guide"]
            print(f"✓ 成功创建: {guide['destination']} {guide['duration_days']}日游 ({guide['travel_style']})")
            print(f"  预算总计: ¥{guide['budget_estimate']['total']}")
            print(f"  景点数量: {len(guide['recommended_attractions'])}个")
        else:
            print(f"✗ 错误: {result.get('detail', 'Unknown error')}")


def test_different_travel_styles():
    print("\n" + "="*60)
    print("测试 5: 不同旅行风格对比")
    print("="*60)
    
    styles = ["深度游", "经典游", "打卡游"]
    
    for style in styles:
        request_data = {
            "destination": "北京",
            "duration_days": 3,
            "travel_style": style
        }
        
        response = requests.post(
            f"{BASE_URL}/api/travel/guide",
            json=request_data
        )
        result = response.json()
        
        if response.status_code == 200:
            guide = result["guide"]
            print(f"\n{style}:")
            print(f"  每日景点数: {len(guide['itinerary'][0]['attractions'])}个")
            print(f"  总预算: ¥{guide['budget_estimate']['total']}")
        else:
            print(f"{style}: 错误 - {result.get('detail')}")


def test_invalid_city():
    print("\n" + "="*60)
    print("测试 6: 测试不支持的城市")
    print("="*60)
    
    request_data = {
        "destination": "火星",
        "duration_days": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/api/travel/guide",
        json=request_data
    )
    result = response.json()
    
    print(f"状态码: {response.status_code}")
    print(f"错误信息: {result.get('detail')}")
    
    assert response.status_code == 400
    print("✓ 正确处理了无效城市")


def run_all_tests():
    print("\n" + "="*60)
    print("旅游攻略功能测试")
    print("="*60)
    print("确保API服务器正在运行: python src/ai_navigator_api.py")
    
    try:
        test_get_supported_cities()
        test_create_travel_guide_basic()
        test_create_travel_guide_with_date()
        test_ai_travel_guide()
        test_different_travel_styles()
        test_invalid_city()
        
        print("\n" + "="*60)
        print("所有测试完成!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n错误: 无法连接到API服务器")
        print("请先启动服务器: python src/ai_navigator_api.py")
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
