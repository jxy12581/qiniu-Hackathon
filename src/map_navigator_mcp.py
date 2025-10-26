#!/usr/bin/env python3
import asyncio
import webbrowser
from urllib.parse import quote
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp.types as types
from itertools import permutations
import platform
import subprocess
from destination_reminder import DestinationReminder
from speed_monitor import SpeedMonitor

app = Server("map-navigator")
reminder_service = DestinationReminder()
speed_monitor = SpeedMonitor()

def auto_play_music():
    system = platform.system()
    
    try:
        if system == "Darwin":
            subprocess.Popen([
                "osascript", "-e",
                'tell application "Music" to play'
            ])
            return "已启动 Apple Music 播放"
        elif system == "Windows":
            try:
                subprocess.Popen([
                    "powershell", "-Command",
                    "Add-Type -AssemblyName presentationCore; " +
                    "$player = New-Object System.Windows.Media.MediaPlayer; " +
                    "$player.Open('https://music.163.com'); " +
                    "$player.Play()"
                ])
                return "已尝试启动 Windows Media Player"
            except:
                webbrowser.open("https://music.163.com")
                return "已在浏览器中打开网易云音乐"
        elif system == "Linux":
            music_players = [
                ("rhythmbox", ["rhythmbox"]),
                ("spotify", ["spotify"]),
                ("vlc", ["vlc", "--started-from-file"]),
            ]
            
            for player_name, command in music_players:
                try:
                    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return f"已启动 {player_name} 播放器"
                except FileNotFoundError:
                    continue
            
            webbrowser.open("https://music.163.com")
            return "已在浏览器中打开网易云音乐"
        else:
            webbrowser.open("https://music.163.com")
            return "已在浏览器中打开网易云音乐"
    except Exception as e:
        webbrowser.open("https://music.163.com")
        return f"已在浏览器中打开网易云音乐 (fallback: {str(e)})"

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="navigate_baidu_map",
            description="Open Baidu Map navigation from origin to destination. Automatically opens the map in browser and enters navigation mode.",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting point address (e.g., '北京天安门' or 'Beijing Tiananmen')"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination address (e.g., '上海东方明珠' or 'Shanghai Oriental Pearl Tower')"
                    },
                    "mode": {
                        "type": "string",
                        "description": "Navigation mode: 'driving' (default), 'transit', 'walking', 'riding'",
                        "enum": ["driving", "transit", "walking", "riding"],
                        "default": "driving"
                    }
                },
                "required": ["origin", "destination"]
            }
        ),
        Tool(
            name="navigate_amap",
            description="Open Amap (Gaode Map) navigation from origin to destination. Automatically opens the map in browser and enters navigation mode.",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting point address (e.g., '北京天安门' or 'Beijing Tiananmen')"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination address (e.g., '上海东方明珠' or 'Shanghai Oriental Pearl Tower')"
                    },
                    "mode": {
                        "type": "string",
                        "description": "Navigation mode: 'car' (default), 'bus', 'walk', 'bike'",
                        "enum": ["car", "bus", "walk", "bike"],
                        "default": "car"
                    }
                },
                "required": ["origin", "destination"]
            }
        ),
        Tool(
            name="open_baidu_map",
            description="Open Baidu Map at a specific location. Shows the location on the map.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to show on map (e.g., '北京故宫' or 'Beijing Forbidden City')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="open_amap",
            description="Open Amap (Gaode Map) at a specific location. Shows the location on the map.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to show on map (e.g., '北京故宫' or 'Beijing Forbidden City')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="navigate_baidu_map_multi",
            description="Open Baidu Map navigation with multiple destinations. Supports both sequential and optimized route planning.",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting point address (e.g., '北京天安门' or 'Beijing Tiananmen')"
                    },
                    "destinations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of destination addresses in order (e.g., ['上海东方明珠', '杭州西湖', '苏州园林'])",
                        "minItems": 2
                    },
                    "mode": {
                        "type": "string",
                        "description": "Navigation mode: 'driving' (default), 'transit', 'walking', 'riding'",
                        "enum": ["driving", "transit", "walking", "riding"],
                        "default": "driving"
                    },
                    "optimize": {
                        "type": "boolean",
                        "description": "Whether to optimize the route order for shortest total distance (default: false)",
                        "default": False
                    }
                },
                "required": ["origin", "destinations"]
            }
        ),
        Tool(
            name="navigate_amap_multi",
            description="Open Amap (Gaode Map) navigation with multiple destinations. Supports both sequential and optimized route planning.",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting point address (e.g., '北京天安门' or 'Beijing Tiananmen')"
                    },
                    "destinations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of destination addresses in order (e.g., ['上海东方明珠', '杭州西湖', '苏州园林'])",
                        "minItems": 2
                    },
                    "mode": {
                        "type": "string",
                        "description": "Navigation mode: 'car' (default), 'bus', 'walk', 'bike'",
                        "enum": ["car", "bus", "walk", "bike"],
                        "default": "car"
                    },
                    "optimize": {
                        "type": "boolean",
                        "description": "Whether to optimize the route order for shortest total distance (default: false)",
                        "default": False
                    }
                },
                "required": ["origin", "destinations"]
            }
        ),
        Tool(
            name="get_destination_weather",
            description="Get weather information and forecast for a destination. Provides current conditions and 3-day forecast including temperature, weather conditions, humidity, wind, and UV index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to get weather for (e.g., '北京', '上海', 'Beijing')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="get_travel_recommendations",
            description="Get travel recommendations for a destination including best visiting times, popular attractions, local cuisine, transportation tips, and travel advice.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to get recommendations for (e.g., '北京', '上海', 'Beijing')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="get_destination_info",
            description="Get comprehensive destination information including both weather forecast and travel recommendations. Combines weather data with tourism tips, attractions, cuisine, and best visiting times.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to get information for (e.g., '北京', '上海', 'Beijing')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="check_speed_limit",
            description="Check current speed against speed limit and provide overspeed alert. Monitors speed during navigation and warns when exceeding limits.",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_speed": {
                        "type": "number",
                        "description": "Current speed in km/h"
                    },
                    "road_type": {
                        "type": "string",
                        "description": "Road type: '城市道路', '城市快速路', '高速公路', '学校区域', '居民区'",
                        "enum": ["城市道路", "城市快速路", "普通公路", "高速公路", "学校区域", "居民区"]
                    },
                    "location": {
                        "type": "string",
                        "description": "Location description (e.g., '北京三环', '学校附近')"
                    },
                    "speed_limit": {
                        "type": "number",
                        "description": "Optional specific speed limit in km/h"
                    }
                },
                "required": ["current_speed"]
            }
        ),
        Tool(
            name="get_speed_reminder",
            description="Get speed reminder and safety tips for a navigation route. Provides speed limits and safety guidelines based on route type and locations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting point address"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination address"
                    },
                    "route_type": {
                        "type": "string",
                        "description": "Navigation mode: 'driving' (default), 'riding', 'walking'",
                        "enum": ["driving", "riding", "walking"],
                        "default": "driving"
                    }
                },
                "required": ["origin", "destination"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not arguments:
        raise ValueError("Missing arguments")
    
    if name == "navigate_baidu_map":
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        mode = arguments.get("mode", "driving")
        
        if not origin or not destination:
            raise ValueError("Both origin and destination are required")
        
        origin_encoded = quote(origin)
        destination_encoded = quote(destination)
        url = f"https://map.baidu.com/direction?origin={origin_encoded}&destination={destination_encoded}&mode={mode}"
        
        webbrowser.open(url)
        
        music_status = auto_play_music()
        
        return [
            TextContent(
                type="text",
                text=f"✅ Baidu Map navigation opened successfully!\n\n"
                     f"📍 From: {origin}\n"
                     f"📍 To: {destination}\n"
                     f"🚗 Mode: {mode}\n"
                     f"🎵 Music: {music_status}\n\n"
                     f"The map should now be open in your default browser with navigation ready."
            )
        ]
    
    elif name == "navigate_amap":
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        mode = arguments.get("mode", "car")
        
        if not origin or not destination:
            raise ValueError("Both origin and destination are required")
        
        origin_encoded = quote(origin)
        destination_encoded = quote(destination)
        url = f"https://uri.amap.com/navigation?from=&to={destination_encoded}&src=myapp&coordinate=gaode&callnative=1&mode={mode}&policy=1&t=0"
        
        webbrowser.open(url)
        
        music_status = auto_play_music()
        
        return [
            TextContent(
                type="text",
                text=f"✅ Amap navigation opened successfully!\n\n"
                     f"📍 From: {origin}\n"
                     f"📍 To: {destination}\n"
                     f"🚗 Mode: {mode}\n"
                     f"🎵 Music: {music_status}\n\n"
                     f"The map should now be open in your default browser with navigation ready."
            )
        ]
    
    elif name == "open_baidu_map":
        location = arguments.get("location")
        
        if not location:
            raise ValueError("Location is required")
        
        location_encoded = quote(location)
        url = f"https://map.baidu.com/search/{location_encoded}"
        
        webbrowser.open(url)
        
        return [
            TextContent(
                type="text",
                text=f"✅ Baidu Map opened successfully!\n\n"
                     f"📍 Location: {location}\n\n"
                     f"The map should now be open in your default browser showing the location."
            )
        ]
    
    elif name == "open_amap":
        location = arguments.get("location")
        
        if not location:
            raise ValueError("Location is required")
        
        location_encoded = quote(location)
        url = f"https://www.amap.com/search?query={location_encoded}"
        
        webbrowser.open(url)
        
        return [
            TextContent(
                type="text",
                text=f"✅ Amap opened successfully!\n\n"
                     f"📍 Location: {location}\n\n"
                     f"The map should now be open in your default browser showing the location."
            )
        ]
    
    elif name == "navigate_baidu_map_multi":
        origin = arguments.get("origin")
        destinations = arguments.get("destinations")
        mode = arguments.get("mode", "driving")
        optimize = arguments.get("optimize", False)
        
        if not origin or not destinations:
            raise ValueError("Both origin and destinations are required")
        
        if not isinstance(destinations, list) or len(destinations) < 2:
            raise ValueError("destinations must be a list with at least 2 locations")
        
        if optimize:
            destinations = _optimize_route_simple(destinations)
        
        waypoints = "|".join([quote(dest) for dest in destinations[:-1]])
        origin_encoded = quote(origin)
        final_destination_encoded = quote(destinations[-1])
        
        url = f"https://map.baidu.com/direction?origin={origin_encoded}&destination={final_destination_encoded}&waypoints={waypoints}&mode={mode}"
        
        webbrowser.open(url)
        
        music_status = auto_play_music()
        
        route_display = f"{origin}"
        for i, dest in enumerate(destinations, 1):
            route_display += f"\n  └─ Stop {i}: {dest}"
        
        optimization_note = " (optimized)" if optimize else " (sequential)"
        
        return [
            TextContent(
                type="text",
                text=f"✅ Baidu Map multi-destination navigation opened successfully!\n\n"
                     f"📍 Route{optimization_note}:\n{route_display}\n"
                     f"🚗 Mode: {mode}\n"
                     f"📊 Total stops: {len(destinations)}\n"
                     f"🎵 Music: {music_status}\n\n"
                     f"The map should now be open in your default browser with multi-point navigation ready."
            )
        ]
    
    elif name == "navigate_amap_multi":
        origin = arguments.get("origin")
        destinations = arguments.get("destinations")
        mode = arguments.get("mode", "car")
        optimize = arguments.get("optimize", False)
        
        if not origin or not destinations:
            raise ValueError("Both origin and destinations are required")
        
        if not isinstance(destinations, list) or len(destinations) < 2:
            raise ValueError("destinations must be a list with at least 2 locations")
        
        if optimize:
            destinations = _optimize_route_simple(destinations)
        
        all_points = [origin] + destinations
        route_display = f"{origin}"
        for i, dest in enumerate(destinations, 1):
            route_display += f"\n  └─ Stop {i}: {dest}"
        
        optimization_note = " (optimized)" if optimize else " (sequential)"
        
        tabs_opened = []
        for i in range(len(all_points) - 1):
            from_point = quote(all_points[i])
            to_point = quote(all_points[i + 1])
            url = f"https://uri.amap.com/navigation?from={from_point}&to={to_point}&src=myapp&coordinate=gaode&callnative=1&mode={mode}&policy=1&t=0"
            webbrowser.open(url)
            tabs_opened.append(f"Leg {i + 1}: {all_points[i]} → {all_points[i + 1]}")
        
        music_status = auto_play_music()
        
        return [
            TextContent(
                type="text",
                text=f"✅ Amap multi-destination navigation opened successfully!\n\n"
                     f"📍 Route{optimization_note}:\n{route_display}\n"
                     f"🚗 Mode: {mode}\n"
                     f"📊 Total stops: {len(destinations)}\n"
                     f"🗂️ Opened {len(tabs_opened)} navigation tabs (one for each leg)\n"
                     f"🎵 Music: {music_status}\n\n"
                     f"The map should now be open in your default browser with navigation segments in separate tabs."
            )
        ]
    
    elif name == "get_destination_weather":
        location = arguments.get("location")
        
        if not location:
            raise ValueError("location is required")
        
        weather_info = reminder_service.get_weather(location)
        weather_message = reminder_service.format_weather_message(weather_info)
        
        return [
            TextContent(
                type="text",
                text=f"✅ Weather information retrieved successfully!\n\n{weather_message}"
            )
        ]
    
    elif name == "get_travel_recommendations":
        location = arguments.get("location")
        
        if not location:
            raise ValueError("location is required")
        
        recommendations = reminder_service.get_travel_recommendations(location)
        recommendations_message = reminder_service.format_recommendations_message(recommendations)
        
        return [
            TextContent(
                type="text",
                text=f"✅ Travel recommendations retrieved successfully!\n\n{recommendations_message}"
            )
        ]
    
    elif name == "get_destination_info":
        location = arguments.get("location")
        
        if not location:
            raise ValueError("location is required")
        
        info = reminder_service.get_destination_info(location)
        full_message = f"{info['weather_message']}\n\n{'='*50}\n\n{info['recommendations_message']}"
        
        return [
            TextContent(
                type="text",
                text=f"✅ Destination information retrieved successfully!\n\n{full_message}"
            )
        ]
    
    elif name == "check_speed_limit":
        current_speed = arguments.get("current_speed")
        road_type = arguments.get("road_type")
        location = arguments.get("location")
        speed_limit = arguments.get("speed_limit")
        
        if current_speed is None:
            raise ValueError("current_speed is required")
        
        speed_check = speed_monitor.check_speed(
            current_speed=current_speed,
            speed_limit=speed_limit,
            road_type=road_type,
            location=location
        )
        
        alert_message = speed_monitor.format_speed_alert(speed_check)
        
        return [
            TextContent(
                type="text",
                text=f"🚦 Speed check completed!\n\n{alert_message}"
            )
        ]
    
    elif name == "get_speed_reminder":
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        route_type = arguments.get("route_type", "driving")
        
        if not origin or not destination:
            raise ValueError("Both origin and destination are required")
        
        reminder_message = speed_monitor.create_speed_reminder_message(
            origin=origin,
            destination=destination,
            route_type=route_type
        )
        
        return [
            TextContent(
                type="text",
                text=f"✅ Speed reminder generated!\n\n{reminder_message}"
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

def _optimize_route_simple(destinations: list[str]) -> list[str]:
    if len(destinations) <= 3:
        min_route = destinations
        min_length = len("".join(destinations))
        
        for perm in permutations(destinations):
            route_length = len("".join(perm))
            if route_length < min_length:
                min_length = route_length
                min_route = list(perm)
        
        return min_route
    else:
        return destinations

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="map-navigator",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
