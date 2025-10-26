#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import webbrowser
from urllib.parse import quote
import platform
import subprocess
import re
import uvicorn
from destination_reminder import DestinationReminder

app = FastAPI(
    title="AI Navigation Assistant API",
    description="AI-powered navigation assistant supporting Baidu Maps and Amap with natural language interface, weather reminders, and travel recommendations",
    version="1.1.0"
)

reminder_service = DestinationReminder()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NavigationRequest(BaseModel):
    origin: str = Field(..., description="Starting point address")
    destination: str = Field(..., description="Destination address")
    mode: Optional[Literal["driving", "transit", "walking", "riding"]] = Field(
        "driving", 
        description="Navigation mode for Baidu Map"
    )
    map_type: Optional[Literal["baidu", "amap"]] = Field(
        "baidu", 
        description="Map service to use"
    )

class MultiNavigationRequest(BaseModel):
    origin: str = Field(..., description="Starting point address")
    destinations: List[str] = Field(..., min_items=2, description="List of destination addresses")
    mode: Optional[Literal["driving", "transit", "walking", "riding"]] = Field(
        "driving", 
        description="Navigation mode"
    )
    optimize: Optional[bool] = Field(False, description="Optimize route order")
    map_type: Optional[Literal["baidu", "amap"]] = Field(
        "baidu", 
        description="Map service to use"
    )

class LocationRequest(BaseModel):
    location: str = Field(..., description="Location to display on map")
    map_type: Optional[Literal["baidu", "amap"]] = Field(
        "baidu", 
        description="Map service to use"
    )

class NaturalLanguageRequest(BaseModel):
    query: str = Field(..., description="Natural language navigation query")
    map_type: Optional[Literal["baidu", "amap"]] = Field(
        None, 
        description="Preferred map service (auto-detect if not specified)"
    )

class NavigationResponse(BaseModel):
    success: bool
    message: str
    url: str
    details: dict

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

def parse_natural_language(query: str) -> dict:
    """
    Parse natural language query to extract navigation parameters.
    
    Supports patterns like:
    - "从A到B" (from A to B)
    - "我要从A出发" (I want to start from A)
    - "帮我从A导航到B" (help me navigate from A to B)
    - "A到B" (A to B)
    
    Args:
        query: Natural language query string
        
    Returns:
        dict: Parsed navigation parameters including origin, destination, mode, map_type
    """
    query_lower = query.lower()
    
    result = {
        "origin": None,
        "destination": None,
        "destinations": [],
        "mode": "driving",
        "map_type": "baidu",
        "is_multi": False
    }
    
    if "高德" in query or "amap" in query_lower or "gaode" in query_lower:
        result["map_type"] = "amap"
    
    if "步行" in query or "walk" in query_lower:
        result["mode"] = "walking"
    elif "骑行" in query or "bike" in query_lower or "riding" in query_lower:
        result["mode"] = "riding"
    elif "公交" in query or "transit" in query_lower or "bus" in query_lower:
        result["mode"] = "transit"
    
    from_patterns = [
        r'(?:我要从|我从|从|出发自|起点是?|start from|from)\s*([^到去至导航,，]+?)(?=到|去|至|导航|出发|,|，|$)',
    ]
    
    for pattern in from_patterns:
        from_match = re.search(pattern, query)
        if from_match:
            origin_text = from_match.group(1).strip()
            origin_text = re.sub(r'(导航|地图|帮我|请)$', '', origin_text).strip()
            if origin_text:
                result["origin"] = origin_text
                break
    
    multi_dest_patterns = [
        r'(?:依次|先后|顺序)(?:去|到|经过)\s*([^,，]+(?:[,，][^,，]+)+)',
        r'(?:去|到)\s*([^,，]+(?:[,，][^,，]+)+?)(?:等地|这些地方|几个地方)',
    ]
    
    for pattern in multi_dest_patterns:
        multi_match = re.search(pattern, query)
        if multi_match:
            dest_str = multi_match.group(1)
            destinations = [d.strip() for d in re.split(r'[,，、]', dest_str) if d.strip()]
            if len(destinations) >= 2:
                result["destinations"] = destinations
                result["is_multi"] = True
                break
    
    if not result["is_multi"]:
        to_patterns = [
            r'(?:到|去|至|导航到|navigate to|to)\s*([^,，。\n用]+?)(?=,|，|。|用|$)',
            r'(?:终点|目的地|destination)\s*(?:是|为|:)?\s*([^,，。\n用]+?)(?=,|，|。|用|$)',
        ]
        
        for pattern in to_patterns:
            to_match = re.search(pattern, query)
            if to_match:
                dest_text = to_match.group(1).strip()
                dest_text = re.sub(r'(,|，|用|。).*$', '', dest_text).strip()
                if dest_text:
                    result["destination"] = dest_text
                    break
    
    if not result["origin"]:
        origin_patterns = [
            r'^([^从到去至帮我请]+?)(?:到|去|至)',
            r'([^,，]+?)(?:出发)',
        ]
        for pattern in origin_patterns:
            origin_match = re.search(pattern, query)
            if origin_match:
                origin_text = origin_match.group(1).strip()
                origin_text = re.sub(r'^(帮我|请|我要)', '', origin_text).strip()
                if origin_text:
                    result["origin"] = origin_text
                    break
    
    return result

@app.get("/", tags=["Info"])
async def root():
    return {
        "name": "AI Navigation Assistant API",
        "version": "1.0.0",
        "description": "AI-powered navigation assistant with natural language support",
        "endpoints": {
            "navigate": "/api/navigate - Basic navigation",
            "navigate_multi": "/api/navigate/multi - Multi-destination navigation",
            "location": "/api/location - Show location on map",
            "ai_navigate": "/api/ai/navigate - Natural language navigation",
            "docs": "/docs - API documentation"
        }
    }

@app.post("/api/navigate", response_model=NavigationResponse, tags=["Navigation"])
async def navigate(request: NavigationRequest):
    """
    Navigate from origin to destination using specified map service.
    
    Args:
        request: NavigationRequest containing origin, destination, mode, and map_type
        
    Returns:
        NavigationResponse with success status, message, URL, and details
    """
    try:
        if not request.origin or not request.origin.strip():
            raise HTTPException(status_code=400, detail="起点地址不能为空")
        if not request.destination or not request.destination.strip():
            raise HTTPException(status_code=400, detail="终点地址不能为空")
        
        origin_encoded = quote(request.origin.strip())
        destination_encoded = quote(request.destination.strip())
        
        if request.map_type == "baidu":
            url = f"https://map.baidu.com/direction?origin={origin_encoded}&destination={destination_encoded}&mode={request.mode}"
        else:
            mode_map = {
                "driving": "car",
                "transit": "bus",
                "walking": "walk",
                "riding": "bike"
            }
            amap_mode = mode_map.get(request.mode, "car")
            url = f"https://uri.amap.com/navigation?from=&to={destination_encoded}&src=myapp&coordinate=gaode&callnative=1&mode={amap_mode}&policy=1&t=0"
        
        webbrowser.open(url)
        music_status = auto_play_music()
        
        return NavigationResponse(
            success=True,
            message=f"Navigation opened successfully on {request.map_type.upper()}",
            url=url,
            details={
                "origin": request.origin,
                "destination": request.destination,
                "mode": request.mode,
                "map_type": request.map_type,
                "music_status": music_status
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/navigate/multi", response_model=NavigationResponse, tags=["Navigation"])
async def navigate_multi(request: MultiNavigationRequest):
    """
    Navigate through multiple destinations using specified map service.
    
    Args:
        request: MultiNavigationRequest with origin, destinations list, mode, and map_type
        
    Returns:
        NavigationResponse with success status, message, URL, and details
    """
    try:
        if not request.origin or not request.origin.strip():
            raise HTTPException(status_code=400, detail="起点地址不能为空")
        if len(request.destinations) < 2:
            raise HTTPException(status_code=400, detail="至少需要2个目的地")
        
        for i, dest in enumerate(request.destinations):
            if not dest or not dest.strip():
                raise HTTPException(status_code=400, detail=f"第{i+1}个目的地地址不能为空")
        
        if request.map_type == "baidu":
            waypoints = "|".join([quote(dest) for dest in request.destinations[:-1]])
            origin_encoded = quote(request.origin)
            final_destination_encoded = quote(request.destinations[-1])
            url = f"https://map.baidu.com/direction?origin={origin_encoded}&destination={final_destination_encoded}&waypoints={waypoints}&mode={request.mode}"
            webbrowser.open(url)
        else:
            all_points = [request.origin] + request.destinations
            urls = []
            for i in range(len(all_points) - 1):
                from_point = quote(all_points[i])
                to_point = quote(all_points[i + 1])
                mode_map = {
                    "driving": "car",
                    "transit": "bus",
                    "walking": "walk",
                    "riding": "bike"
                }
                amap_mode = mode_map.get(request.mode, "car")
                segment_url = f"https://uri.amap.com/navigation?from={from_point}&to={to_point}&src=myapp&coordinate=gaode&callnative=1&mode={amap_mode}&policy=1&t=0"
                webbrowser.open(segment_url)
                urls.append(segment_url)
            url = urls[0]
        
        music_status = auto_play_music()
        
        return NavigationResponse(
            success=True,
            message=f"Multi-destination navigation opened on {request.map_type.upper()}",
            url=url,
            details={
                "origin": request.origin,
                "destinations": request.destinations,
                "mode": request.mode,
                "optimize": request.optimize,
                "map_type": request.map_type,
                "total_stops": len(request.destinations),
                "music_status": music_status
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/location", response_model=NavigationResponse, tags=["Location"])
async def show_location(request: LocationRequest):
    """
    Display a location on the map.
    
    Args:
        request: LocationRequest with location and map_type
        
    Returns:
        NavigationResponse with success status, message, URL, and details
    """
    try:
        if not request.location or not request.location.strip():
            raise HTTPException(status_code=400, detail="位置地址不能为空")
        
        location_encoded = quote(request.location.strip())
        
        if request.map_type == "baidu":
            url = f"https://map.baidu.com/search/{location_encoded}"
        else:
            url = f"https://www.amap.com/search?query={location_encoded}"
        
        webbrowser.open(url)
        
        return NavigationResponse(
            success=True,
            message=f"Location opened on {request.map_type.upper()}",
            url=url,
            details={
                "location": request.location,
                "map_type": request.map_type
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/navigate", response_model=NavigationResponse, tags=["AI"])
async def ai_navigate(request: NaturalLanguageRequest):
    """
    Navigate using natural language query with AI parsing.
    
    Args:
        request: NaturalLanguageRequest with query string and optional map_type
        
    Returns:
        NavigationResponse with success status, message, URL, and details
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="查询内容不能为空")
        
        parsed = parse_natural_language(request.query.strip())
        
        if request.map_type:
            parsed["map_type"] = request.map_type
        
        if not parsed["origin"]:
            raise HTTPException(
                status_code=400, 
                detail="无法识别起点。请在查询中明确指定起点，例如：'从北京到上海'"
            )
        
        if parsed["is_multi"]:
            if not parsed["destinations"] or len(parsed["destinations"]) < 2:
                raise HTTPException(
                    status_code=400,
                    detail="无法识别多个目的地。请明确指定至少2个目的地"
                )
            
            multi_request = MultiNavigationRequest(
                origin=parsed["origin"],
                destinations=parsed["destinations"],
                mode=parsed["mode"],
                map_type=parsed["map_type"]
            )
            return await navigate_multi(multi_request)
        else:
            if not parsed["destination"]:
                raise HTTPException(
                    status_code=400,
                    detail="无法识别终点。请在查询中明确指定终点，例如：'从北京到上海'"
                )
            
            nav_request = NavigationRequest(
                origin=parsed["origin"],
                destination=parsed["destination"],
                mode=parsed["mode"],
                map_type=parsed["map_type"]
            )
            return await navigate(nav_request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解析错误: {str(e)}")

@app.get("/health", tags=["Info"])
async def health_check():
    return {"status": "healthy", "service": "AI Navigation Assistant"}

@app.get("/api/weather/{location}", tags=["Destination Info"])
async def get_weather(location: str):
    try:
        weather_info = reminder_service.get_weather(location)
        if "error" in weather_info:
            raise HTTPException(status_code=500, detail=weather_info["error"])
        return {
            "success": True,
            "data": weather_info,
            "message": reminder_service.format_weather_message(weather_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/{location}", tags=["Destination Info"])
async def get_recommendations(location: str):
    try:
        recommendations = reminder_service.get_travel_recommendations(location)
        return {
            "success": True,
            "data": recommendations,
            "message": reminder_service.format_recommendations_message(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/destination-info/{location}", tags=["Destination Info"])
async def get_destination_info(location: str):
    try:
        info = reminder_service.get_destination_info(location)
        return {
            "success": True,
            "location": location,
            "weather": info["weather"],
            "recommendations": info["recommendations"],
            "formatted_messages": {
                "weather": info["weather_message"],
                "recommendations": info["recommendations_message"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
