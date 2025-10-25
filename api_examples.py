#!/usr/bin/env python3
import requests
import json

API_BASE_URL = "http://localhost:8000"

def example_basic_navigation():
    print("\n=== Example 1: Basic Navigation ===")
    response = requests.post(
        f"{API_BASE_URL}/api/navigate",
        json={
            "origin": "北京天安门",
            "destination": "上海东方明珠",
            "mode": "driving",
            "map_type": "baidu"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def example_multi_destination():
    print("\n=== Example 2: Multi-destination Navigation ===")
    response = requests.post(
        f"{API_BASE_URL}/api/navigate/multi",
        json={
            "origin": "北京天安门",
            "destinations": ["上海东方明珠", "杭州西湖", "苏州园林"],
            "mode": "driving",
            "optimize": False,
            "map_type": "baidu"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def example_show_location():
    print("\n=== Example 3: Show Location ===")
    response = requests.post(
        f"{API_BASE_URL}/api/location",
        json={
            "location": "北京故宫",
            "map_type": "baidu"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def example_ai_natural_language():
    print("\n=== Example 4: AI Natural Language Navigation ===")
    
    queries = [
        "帮我从北京天安门导航到上海东方明珠，用百度地图",
        "从广州塔到深圳湾公园，步行路线，用高德地图",
        "我要从杭州西湖出发，依次去苏州园林、南京夫子庙、扬州瘦西湖",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = requests.post(
            f"{API_BASE_URL}/api/ai/navigate",
            json={"query": query}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def example_health_check():
    print("\n=== Example 5: Health Check ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("AI Navigation Assistant API Examples")
    print("=" * 50)
    print("Make sure the API server is running on http://localhost:8000")
    print("Start server with: python src/ai_navigator_api.py")
    print("=" * 50)
    
    try:
        example_health_check()
        
        choice = input("\nRun navigation examples? (y/n): ")
        if choice.lower() == 'y':
            example_basic_navigation()
            example_multi_destination()
            example_show_location()
            example_ai_natural_language()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API server.")
        print("Please start the server first: python src/ai_navigator_api.py")
    except Exception as e:
        print(f"\nError: {e}")
