#!/usr/bin/env python3
"""
Test script for destination reminder functionality
"""
import sys
sys.path.insert(0, 'src')

from destination_reminder import DestinationReminder

def test_weather():
    print("=" * 60)
    print("Testing Weather Information")
    print("=" * 60)
    
    reminder = DestinationReminder()
    
    locations = ["北京", "上海"]
    
    for location in locations:
        print(f"\n{'='*60}")
        print(f"Location: {location}")
        print('='*60)
        
        weather = reminder.get_weather(location)
        message = reminder.format_weather_message(weather)
        print(message)

def test_recommendations():
    print("\n\n" + "=" * 60)
    print("Testing Travel Recommendations")
    print("=" * 60)
    
    reminder = DestinationReminder()
    
    locations = ["北京", "杭州", "成都"]
    
    for location in locations:
        print(f"\n{'='*60}")
        print(f"Location: {location}")
        print('='*60)
        
        recommendations = reminder.get_travel_recommendations(location)
        message = reminder.format_recommendations_message(recommendations)
        print(message)

def test_full_info():
    print("\n\n" + "=" * 60)
    print("Testing Full Destination Information")
    print("=" * 60)
    
    reminder = DestinationReminder()
    
    location = "北京"
    print(f"\n{'='*60}")
    print(f"Location: {location}")
    print('='*60)
    
    info = reminder.get_destination_info(location)
    print(info['weather_message'])
    print("\n" + "="*60 + "\n")
    print(info['recommendations_message'])

if __name__ == "__main__":
    print("Testing Destination Reminder Module\n")
    
    test_weather()
    
    test_recommendations()
    
    test_full_info()
    
    print("\n\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
