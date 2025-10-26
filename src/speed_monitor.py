#!/usr/bin/env python3
"""
Speed Monitor Module
Provides speed monitoring and overspeed alert functionality for navigation
"""
from typing import Dict, List, Optional
from datetime import datetime


class SpeedMonitor:
    """Handle speed monitoring and overspeed alerts during navigation"""
    
    def __init__(self):
        self.speed_limits = {
            "城市道路": 60,
            "城市快速路": 80,
            "普通公路": 80,
            "高速公路": 120,
            "学校区域": 30,
            "居民区": 30,
            "default": 60
        }
        
        self.road_types_keywords = {
            "高速": "高速公路",
            "快速路": "城市快速路",
            "快速": "城市快速路",
            "学校": "学校区域",
            "校园": "学校区域",
            "小区": "居民区",
            "居民区": "居民区"
        }
    
    def get_speed_limit(self, road_type: str = None, location: str = None) -> int:
        """
        Get speed limit for a road type or location
        
        Args:
            road_type: Road type (e.g., "高速公路", "城市道路")
            location: Location description (e.g., "北京三环", "学校附近")
            
        Returns:
            Speed limit in km/h
        """
        if road_type and road_type in self.speed_limits:
            return self.speed_limits[road_type]
        
        if location:
            for keyword, road_type_key in self.road_types_keywords.items():
                if keyword in location:
                    return self.speed_limits[road_type_key]
        
        return self.speed_limits["default"]
    
    def check_speed(self, current_speed: float, speed_limit: int = None, 
                   road_type: str = None, location: str = None) -> Dict:
        """
        Check if current speed exceeds the speed limit
        
        Args:
            current_speed: Current speed in km/h
            speed_limit: Optional specific speed limit
            road_type: Road type
            location: Location description
            
        Returns:
            Dictionary containing check result
        """
        if speed_limit is None:
            speed_limit = self.get_speed_limit(road_type, location)
        
        is_overspeeding = current_speed > speed_limit
        speed_diff = current_speed - speed_limit
        
        severity = "正常"
        if is_overspeeding:
            if speed_diff <= 10:
                severity = "轻微超速"
            elif speed_diff <= 20:
                severity = "中度超速"
            else:
                severity = "严重超速"
        
        return {
            "current_speed": current_speed,
            "speed_limit": speed_limit,
            "is_overspeeding": is_overspeeding,
            "speed_difference": speed_diff if is_overspeeding else 0,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
    
    def format_speed_alert(self, speed_check: Dict) -> str:
        """
        Format speed check result into an alert message
        
        Args:
            speed_check: Speed check result dictionary
            
        Returns:
            Formatted alert message
        """
        if not speed_check["is_overspeeding"]:
            return f"✅ 当前速度: {speed_check['current_speed']} km/h\n限速: {speed_check['speed_limit']} km/h\n状态: 速度正常"
        
        message = f"⚠️ 超速警告!\n\n"
        message += f"当前速度: {speed_check['current_speed']} km/h\n"
        message += f"限速标准: {speed_check['speed_limit']} km/h\n"
        message += f"超速: {speed_check['speed_difference']} km/h\n"
        message += f"级别: {speed_check['severity']}\n\n"
        
        if speed_check['severity'] == "轻微超速":
            message += "💡 建议: 请适当降低车速"
        elif speed_check['severity'] == "中度超速":
            message += "⚠️ 警告: 请立即降低车速,注意安全!"
        else:
            message += "🚨 严重警告: 请立即大幅降低车速!危险!"
        
        return message
    
    def get_navigation_speed_info(self, route_type: str = "driving") -> Dict:
        """
        Get speed-related information for navigation
        
        Args:
            route_type: Navigation type (driving, walking, etc.)
            
        Returns:
            Dictionary containing speed information
        """
        speed_info = {
            "route_type": route_type,
            "monitoring_enabled": False,
            "recommended_speed": 0,
            "max_speed": 0
        }
        
        if route_type == "driving":
            speed_info["monitoring_enabled"] = True
            speed_info["recommended_speed"] = 60
            speed_info["max_speed"] = 120
        elif route_type == "riding":
            speed_info["monitoring_enabled"] = True
            speed_info["recommended_speed"] = 15
            speed_info["max_speed"] = 25
        elif route_type == "walking":
            speed_info["monitoring_enabled"] = False
            speed_info["recommended_speed"] = 5
            speed_info["max_speed"] = 10
        
        return speed_info
    
    def get_speed_limit_by_city(self, city: str) -> Dict[str, int]:
        """
        Get speed limits for different road types in a specific city
        
        Args:
            city: City name
            
        Returns:
            Dictionary of road types and their speed limits
        """
        city_limits = {
            "北京": {
                "环路": 80,
                "快速路": 80,
                "普通道路": 60,
                "高速公路": 120
            },
            "上海": {
                "高架路": 80,
                "快速路": 80,
                "普通道路": 60,
                "高速公路": 120
            },
            "广州": {
                "快速路": 80,
                "普通道路": 60,
                "高速公路": 120
            },
            "深圳": {
                "快速路": 80,
                "普通道路": 60,
                "高速公路": 120
            }
        }
        
        for city_name, limits in city_limits.items():
            if city_name in city or city in city_name:
                return limits
        
        return {
            "普通道路": 60,
            "快速路": 80,
            "高速公路": 120
        }
    
    def create_speed_reminder_message(self, origin: str, destination: str, 
                                     route_type: str = "driving") -> str:
        """
        Create a comprehensive speed reminder message for a route
        
        Args:
            origin: Starting point
            destination: Destination
            route_type: Navigation mode
            
        Returns:
            Formatted reminder message
        """
        speed_info = self.get_navigation_speed_info(route_type)
        
        message = f"🚗 行程速度提醒\n\n"
        message += f"📍 起点: {origin}\n"
        message += f"📍 终点: {destination}\n"
        message += f"🚦 导航模式: {route_type}\n\n"
        
        if speed_info["monitoring_enabled"]:
            message += "⚠️ 超速监控已启用\n\n"
            message += f"💡 建议速度: {speed_info['recommended_speed']} km/h\n"
            message += f"⚡ 最高限速: {speed_info['max_speed']} km/h\n\n"
            message += "📋 安全提示:\n"
            message += "  • 请遵守交通规则和限速标志\n"
            message += "  • 注意路况变化,及时调整车速\n"
            message += "  • 学校和居民区限速30 km/h\n"
            message += "  • 高速公路最高限速120 km/h\n"
            message += "  • 超速行驶将影响行车安全\n"
        else:
            message += "ℹ️ 当前导航模式无需超速监控\n"
            message += f"💡 建议速度: {speed_info['recommended_speed']} km/h\n"
        
        return message
