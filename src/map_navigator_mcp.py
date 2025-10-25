#!/usr/bin/env python3
import asyncio
import webbrowser
from urllib.parse import quote
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp.types as types

app = Server("map-navigator")

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
        
        return [
            TextContent(
                type="text",
                text=f"✅ Baidu Map navigation opened successfully!\n\n"
                     f"📍 From: {origin}\n"
                     f"📍 To: {destination}\n"
                     f"🚗 Mode: {mode}\n\n"
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
        
        return [
            TextContent(
                type="text",
                text=f"✅ Amap navigation opened successfully!\n\n"
                     f"📍 From: {origin}\n"
                     f"📍 To: {destination}\n"
                     f"🚗 Mode: {mode}\n\n"
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
    
    else:
        raise ValueError(f"Unknown tool: {name}")

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
