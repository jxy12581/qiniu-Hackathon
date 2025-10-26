#!/usr/bin/env python3
"""
Test script for Beijing to Kunming 10-day travel itinerary
"""
import sys
sys.path.insert(0, 'src')

from travel_itinerary import TravelItinerary

def test_itinerary():
    print("=" * 80)
    print("测试北京到昆明10天旅行攻略")
    print("=" * 80)
    print()
    
    itinerary_service = TravelItinerary()
    
    print("1. 获取可用行程列表:")
    for key in itinerary_service.itineraries.keys():
        print(f"   - {key}")
    print()
    
    print("2. 获取北京-昆明-10天行程:")
    itinerary = itinerary_service.get_itinerary("北京-昆明-10天")
    
    if itinerary:
        print(f"   ✓ 行程标题: {itinerary['title']}")
        print(f"   ✓ 行程天数: {itinerary['duration_days']}天")
        print(f"   ✓ 起点: {itinerary['origin']}")
        print(f"   ✓ 终点: {itinerary['destination']}")
        print(f"   ✓ 预计费用: {itinerary['total_estimated_cost']}")
        print(f"   ✓ 每日行程数: {len(itinerary['days'])}天")
        print()
        
        print("3. 格式化输出行程 (前500字符预览):")
        message = itinerary_service.generate_itinerary_message(itinerary)
        print(message[:500])
        print("...")
        print()
        
        print("4. 导航信息:")
        nav_info = itinerary_service.get_navigation_info(
            itinerary['origin'], 
            itinerary['destination']
        )
        print(f"   起点: {nav_info['origin']}")
        print(f"   终点: {nav_info['destination']}")
        print(f"   百度地图: {nav_info['baidu_map_url'][:80]}...")
        print(f"   高德地图: {nav_info['amap_url'][:80]}...")
        print()
        
        print("5. 第1天行程详情:")
        day1 = itinerary['days'][0]
        print(f"   Day {day1['day']}: {day1['title']}")
        print(f"   地点: {day1['location']}")
        print(f"   活动数: {len(day1['activities'])}个")
        print(f"   住宿: {day1['accommodation']}")
        print(f"   预计花费: {day1['estimated_cost']}")
        print()
        
        print("✓ 所有测试通过!")
    else:
        print("   ✗ 未找到行程")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = test_itinerary()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
