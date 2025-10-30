#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import webbrowser
from urllib.parse import quote
import platform
import subprocess
import re
import uvicorn
import os
import time
import asyncio
from destination_reminder import DestinationReminder
from speed_monitor import SpeedMonitor
from travel_guide import TravelGuidePlanner, TravelGuide
from transportation_recommender import TransportationRecommender, RouteRecommendation, TransportationOption
from performance_monitor import PerformanceMonitor
from exception_handler import ExceptionHandler
from sre_notifier import SRENotifier, NotificationConfig
from auto_scaler import AutoScaler
from structured_logger import StructuredLogger

app = FastAPI(
    title="AI Navigation Assistant API",
    description="AI-powered navigation assistant supporting Baidu Maps and Amap with natural language interface, weather reminders, travel recommendations, speed monitoring, travel guide planning, intelligent transportation recommendations, and performance monitoring with auto-scaling",
    version="2.0.0"
)

reminder_service = DestinationReminder()
speed_monitor = SpeedMonitor()
travel_planner = TravelGuidePlanner()
transport_recommender = TransportationRecommender()

perf_monitor = PerformanceMonitor(
    cpu_threshold=80.0,
    memory_threshold=85.0,
    error_rate_threshold=0.05,
    response_time_threshold_ms=1000.0
)

exception_handler = ExceptionHandler(
    max_retry_attempts=3,
    circuit_breaker_threshold=5
)

notifier_config = NotificationConfig(
    enabled=False
)
sre_notifier = SRENotifier(config=notifier_config)

auto_scaler = AutoScaler(
    deployment_type=os.getenv("DEPLOYMENT_TYPE", "kubernetes"),
    min_replicas=3,
    max_replicas=10,
    deployment_name="ai-navigator"
)

struct_logger = StructuredLogger("ai-navigator", log_level=os.getenv("LOG_LEVEL", "INFO"))

perf_monitor.start_monitoring(interval_seconds=30)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    perf_monitor.increment_connections()
    start_time = time.time()
    is_error = False
    
    try:
        response = await call_next(request)
        is_error = response.status_code >= 400
        return response
    except Exception as e:
        is_error = True
        struct_logger.error(f"Request failed: {str(e)}", path=request.url.path, method=request.method)
        raise
    finally:
        response_time_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(response_time_ms, is_error)
        perf_monitor.decrement_connections()
        
        struct_logger.info(
            f"{request.method} {request.url.path}",
            response_time_ms=round(response_time_ms, 2),
            status="error" if is_error else "success"
        )

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

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

class SpeedCheckRequest(BaseModel):
    current_speed: float = Field(..., description="Current speed in km/h")
    road_type: Optional[Literal["城市道路", "城市快速路", "普通公路", "高速公路", "学校区域", "居民区"]] = Field(
        None,
        description="Road type"
    )
    location: Optional[str] = Field(None, description="Location description")
    speed_limit: Optional[int] = Field(None, description="Specific speed limit in km/h")

class SpeedReminderRequest(BaseModel):
    origin: str = Field(..., description="Starting point address")
    destination: str = Field(..., description="Destination address")
    route_type: Optional[Literal["driving", "riding", "walking"]] = Field(
        "driving",
        description="Navigation mode"
    )

class SpeedResponse(BaseModel):
    success: bool
    message: str
    details: dict

class TravelGuideRequest(BaseModel):
    destination: str = Field(..., description="Destination city")
    duration_days: int = Field(3, ge=1, le=30, description="Trip duration in days")
    travel_style: Optional[Literal["深度游", "经典游", "打卡游"]] = Field(
        "经典游",
        description="Travel style: 深度游(deep), 经典游(classic), 打卡游(quick)"
    )
    start_date: Optional[str] = Field(None, description="Trip start date (YYYY-MM-DD)")

class TravelGuideQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language travel guide query")

class TravelGuideResponse(BaseModel):
    success: bool
    message: str
    guide: TravelGuide

class TransportRecommendationRequest(BaseModel):
    origin: str = Field(..., description="Starting point address")
    destination: str = Field(..., description="Destination address")
    estimated_distance_km: Optional[float] = Field(None, description="Estimated distance in kilometers")
    trip_purpose: Optional[Literal["通勤", "旅游", "商务", "紧急"]] = Field(None, description="Trip purpose")
    luggage: Optional[Literal["无", "少量", "较多"]] = Field(None, description="Luggage amount")
    budget: Optional[Literal["经济", "标准", "舒适"]] = Field(None, description="Budget level")
    time_sensitive: bool = Field(False, description="Whether time is sensitive")

class TransportQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language transportation query")

class TransportRecommendationResponse(BaseModel):
    success: bool
    message: str
    recommendation: RouteRecommendation

class TransportModesResponse(BaseModel):
    success: bool
    message: str
    modes: List[TransportationOption]

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
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {
        "name": "AI Navigation Assistant API",
        "version": "1.5.0",
        "description": "AI-powered navigation assistant with natural language support",
        "endpoints": {
            "web_ui": "/static/index.html - Browser-based dialog interface",
            "navigate": "/api/navigate - Basic navigation",
            "navigate_multi": "/api/navigate/multi - Multi-destination navigation",
            "location": "/api/location - Show location on map",
            "ai_navigate": "/api/ai/navigate - Natural language navigation",
            "travel_guide": "/api/travel/guide - Create travel guide",
            "travel_guide_ai": "/api/travel/guide/ai - Natural language travel guide",
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
            url = f"https://map.baidu.com/?ugc_type=3&ugc_ver=1&qt=nav&start=0,{origin_encoded}&end=0,{destination_encoded}&mode={request.mode}"
        else:
            mode_map = {
                "driving": "car",
                "transit": "bus",
                "walking": "walk",
                "riding": "bike"
            }
            amap_mode = mode_map.get(request.mode, "car")
            url = f"https://uri.amap.com/navigation?from={origin_encoded}&to={destination_encoded}&src=myapp&coordinate=gaode&callnative=1&mode={amap_mode}&policy=1&t=0"
        
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
            url = f"https://map.baidu.com/?ugc_type=3&ugc_ver=1&qt=nav&start=0,{origin_encoded}&end=0,{final_destination_encoded}&sy=3&mode={request.mode}"
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

@app.post("/api/speed/check", response_model=SpeedResponse, tags=["Speed Monitoring"])
async def check_speed(request: SpeedCheckRequest):
    try:
        speed_check = speed_monitor.check_speed(
            current_speed=request.current_speed,
            speed_limit=request.speed_limit,
            road_type=request.road_type,
            location=request.location
        )
        
        alert_message = speed_monitor.format_speed_alert(speed_check)
        
        return SpeedResponse(
            success=True,
            message=alert_message,
            details=speed_check
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/speed/reminder", response_model=SpeedResponse, tags=["Speed Monitoring"])
async def get_speed_reminder(request: SpeedReminderRequest):
    try:
        reminder_message = speed_monitor.create_speed_reminder_message(
            origin=request.origin,
            destination=request.destination,
            route_type=request.route_type
        )
        
        speed_info = speed_monitor.get_navigation_speed_info(request.route_type)
        
        return SpeedResponse(
            success=True,
            message=reminder_message,
            details=speed_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/speed/limits/{city}", tags=["Speed Monitoring"])
async def get_city_speed_limits(city: str):
    try:
        limits = speed_monitor.get_speed_limit_by_city(city)
        return {
            "success": True,
            "city": city,
            "speed_limits": limits,
            "message": f"查询到{city}的速度限制信息"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/travel/guide", response_model=TravelGuideResponse, tags=["Travel Guide"])
async def create_travel_guide(request: TravelGuideRequest):
    """
    Create a comprehensive travel guide for a destination.
    
    Args:
        request: TravelGuideRequest with destination, duration, style, and start date
        
    Returns:
        TravelGuideResponse with complete travel itinerary and recommendations
    """
    try:
        guide = travel_planner.create_itinerary(
            destination=request.destination,
            duration_days=request.duration_days,
            travel_style=request.travel_style,
            start_date=request.start_date
        )
        
        return TravelGuideResponse(
            success=True,
            message=f"成功创建{request.destination}{request.duration_days}日游攻略",
            guide=guide
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/travel/guide/ai", response_model=TravelGuideResponse, tags=["Travel Guide"])
async def create_travel_guide_ai(request: TravelGuideQueryRequest):
    """
    Create a travel guide using natural language query.
    
    Supports queries like:
    - "帮我规划北京3天游"
    - "我想去上海玩5天，深度游"
    - "杭州4日游攻略"
    
    Args:
        request: TravelGuideQueryRequest with natural language query
        
    Returns:
        TravelGuideResponse with complete travel itinerary and recommendations
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="查询内容不能为空")
        
        parsed = travel_planner.parse_travel_query(request.query.strip())
        
        if not parsed["destination"]:
            raise HTTPException(
                status_code=400,
                detail=f"无法识别目的地。请明确指定城市，当前支持: {', '.join(travel_planner.city_attractions.keys())}"
            )
        
        guide = travel_planner.create_itinerary(
            destination=parsed["destination"],
            duration_days=parsed["duration_days"],
            travel_style=parsed["travel_style"],
            start_date=parsed["start_date"]
        )
        
        return TravelGuideResponse(
            success=True,
            message=f"成功创建{parsed['destination']}{parsed['duration_days']}日游攻略({parsed['travel_style']})",
            guide=guide
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解析错误: {str(e)}")

@app.get("/api/travel/cities", tags=["Travel Guide"])
async def get_supported_cities():
    """
    Get list of supported cities for travel guide planning.
    
    Returns:
        List of supported cities with their attractions count
    """
    cities = []
    for city, attractions in travel_planner.city_attractions.items():
        cities.append({
            "name": city,
            "attractions_count": len(attractions),
            "sample_attractions": [a.name for a in attractions[:3]]
        })
    
    return {
        "success": True,
        "cities": cities,
        "total": len(cities),
        "message": f"当前支持{len(cities)}个城市的旅游攻略规划"
    }

@app.post("/api/transportation/recommend", response_model=TransportRecommendationResponse, tags=["Transportation"])
async def recommend_transportation(request: TransportRecommendationRequest):
    """
    Get intelligent transportation recommendations for a route.
    
    Args:
        request: TransportRecommendationRequest with route and preference details
        
    Returns:
        TransportRecommendationResponse with recommended transportation mode and alternatives
    """
    try:
        recommendation = transport_recommender.recommend_transportation(
            origin=request.origin,
            destination=request.destination,
            estimated_distance_km=request.estimated_distance_km,
            trip_purpose=request.trip_purpose,
            luggage=request.luggage,
            budget=request.budget,
            time_sensitive=request.time_sensitive
        )
        
        return TransportRecommendationResponse(
            success=True,
            message=f"成功为您推荐从{request.origin}到{request.destination}的交通方式",
            recommendation=recommendation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transportation/recommend/ai", response_model=TransportRecommendationResponse, tags=["Transportation"])
async def recommend_transportation_ai(request: TransportQueryRequest):
    """
    Get intelligent transportation recommendations using natural language query.
    
    Supports queries like:
    - "从北京到上海用什么交通工具?"
    - "我要去杭州出差，行李多，推荐交通方式"
    - "通勤从天安门到西单，怎么去最经济?"
    
    Args:
        request: TransportQueryRequest with natural language query
        
    Returns:
        TransportRecommendationResponse with recommended transportation mode and alternatives
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="查询内容不能为空")
        
        parsed = transport_recommender.parse_recommendation_query(request.query.strip())
        
        if not parsed["origin"]:
            raise HTTPException(
                status_code=400,
                detail="无法识别起点。请在查询中明确指定起点，例如：'从北京到上海用什么交通工具'"
            )
        
        if not parsed["destination"]:
            raise HTTPException(
                status_code=400,
                detail="无法识别终点。请在查询中明确指定终点，例如：'从北京到上海用什么交通工具'"
            )
        
        recommendation = transport_recommender.recommend_transportation(
            origin=parsed["origin"],
            destination=parsed["destination"],
            trip_purpose=parsed["trip_purpose"],
            luggage=parsed["luggage"],
            budget=parsed["budget"],
            time_sensitive=parsed["time_sensitive"]
        )
        
        return TransportRecommendationResponse(
            success=True,
            message=f"成功为您推荐从{parsed['origin']}到{parsed['destination']}的交通方式",
            recommendation=recommendation
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解析错误: {str(e)}")

@app.get("/api/transportation/modes", response_model=TransportModesResponse, tags=["Transportation"])
async def get_transportation_modes():
    """
    Get all available transportation modes with details.
    
    Returns:
        List of all transportation modes with descriptions, pros, cons, and use cases
    """
    try:
        modes = transport_recommender.get_all_transportation_modes()
        
        return TransportModesResponse(
            success=True,
            message=f"共有{len(modes)}种交通方式可供选择",
            modes=modes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monitoring/status", tags=["Monitoring"])
async def get_monitoring_status():
    """
    获取系统性能监控状态,包括CPU、内存、请求统计等指标
    """
    try:
        status = perf_monitor.get_current_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monitoring/metrics/history", tags=["Monitoring"])
async def get_metrics_history(minutes: Optional[int] = 60):
    """
    获取历史性能指标数据
    
    Args:
        minutes: 获取最近N分钟的数据(默认60分钟)
    """
    try:
        metrics = perf_monitor.get_metrics_history(minutes=minutes)
        return {
            "success": True,
            "data": metrics,
            "count": len(metrics),
            "time_range_minutes": minutes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monitoring/alerts", tags=["Monitoring"])
async def get_alerts(include_resolved: bool = False):
    """
    获取系统告警列表
    
    Args:
        include_resolved: 是否包含已解决的告警
    """
    try:
        alerts = perf_monitor.get_all_alerts(include_resolved=include_resolved)
        return {
            "success": True,
            "alerts": alerts,
            "count": len(alerts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/monitoring/alerts/{metric_type}/resolve", tags=["Monitoring"])
async def resolve_alert(metric_type: str):
    """
    手动解决指定类型的告警
    """
    try:
        perf_monitor.resolve_alert(metric_type)
        return {
            "success": True,
            "message": f"已解决 {metric_type} 类型的告警"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/exceptions/summary", tags=["Exception Handling"])
async def get_exception_summary():
    """
    获取异常处理统计摘要
    """
    try:
        summary = exception_handler.get_exception_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/exceptions/unresolved", tags=["Exception Handling"])
async def get_unresolved_exceptions():
    """
    获取未解决的异常列表
    """
    try:
        exceptions = exception_handler.get_unresolved_exceptions()
        return {
            "success": True,
            "exceptions": exceptions,
            "count": len(exceptions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/exceptions/{exception_type}/resolve", tags=["Exception Handling"])
async def mark_exception_resolved(exception_type: str):
    """
    标记指定类型的异常为已解决
    """
    try:
        count = exception_handler.mark_resolved(exception_type)
        return {
            "success": True,
            "message": f"已标记 {count} 个 {exception_type} 异常为已解决",
            "resolved_count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scaling/recommendation", tags=["Auto Scaling"])
async def get_scaling_recommendation():
    """
    获取自动扩缩容建议
    """
    try:
        recommendation = perf_monitor.get_scaling_recommendation()
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scaling/evaluate", tags=["Auto Scaling"])
async def evaluate_and_scale():
    """
    评估系统状态并执行自动扩缩容(如需要)
    """
    try:
        recommendation = perf_monitor.get_scaling_recommendation()
        
        scaling_event = auto_scaler.evaluate_scaling(recommendation)
        
        if scaling_event.success and scaling_event.action != "no_action":
            report = auto_scaler.generate_scaling_report(scaling_event)
            sre_notifier.send_scaling_report(report)
        
        return {
            "success": True,
            "event": {
                "action": scaling_event.action,
                "reason": scaling_event.reason,
                "before": scaling_event.before,
                "after": scaling_event.after,
                "success": scaling_event.success
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scaling/manual", tags=["Auto Scaling"])
async def manual_scale(replicas: int, reason: str = "Manual scaling request"):
    """
    手动触发扩缩容
    
    Args:
        replicas: 目标副本数
        reason: 扩缩容原因
    """
    try:
        event = auto_scaler.manual_scale(replicas, reason)
        
        if event.success:
            report = auto_scaler.generate_scaling_report(event)
            sre_notifier.send_scaling_report(report)
        
        return {
            "success": event.success,
            "message": f"扩缩容操作{'成功' if event.success else '失败'}",
            "event": {
                "action": event.action,
                "before": event.before,
                "after": event.after,
                "error": event.error_message
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scaling/history", tags=["Auto Scaling"])
async def get_scaling_history(limit: int = 20):
    """
    获取扩缩容历史记录
    """
    try:
        history = auto_scaler.get_scaling_history(limit=limit)
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scaling/summary", tags=["Auto Scaling"])
async def get_scaling_summary():
    """
    获取扩缩容统计摘要
    """
    try:
        summary = auto_scaler.get_scaling_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/history", tags=["SRE Notifications"])
async def get_notification_history(limit: int = 50):
    """
    获取SRE通知历史记录
    """
    try:
        history = sre_notifier.get_notification_history(limit=limit)
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/stats", tags=["SRE Notifications"])
async def get_notification_stats():
    """
    获取SRE通知统计信息
    """
    try:
        stats = sre_notifier.get_notification_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notifications/test", tags=["SRE Notifications"])
async def send_test_notification():
    """
    发送测试通知
    """
    try:
        sre_notifier.send_alert(
            subject="测试通知",
            message="这是一条测试通知,用于验证通知系统配置是否正确",
            severity="info"
        )
        return {
            "success": True,
            "message": "测试通知已发送"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health/detailed", tags=["Info"])
async def detailed_health_check():
    """
    详细健康检查,包含所有子系统状态
    """
    try:
        perf_status = perf_monitor.get_current_status()
        exc_summary = exception_handler.get_exception_summary()
        scaling_summary = auto_scaler.get_scaling_summary()
        
        overall_status = "healthy"
        if perf_status.get("status") == "critical" or exc_summary.get("severity_distribution", {}).get("critical", 0) > 0:
            overall_status = "critical"
        elif perf_status.get("status") == "warning":
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "service": "AI Navigation Assistant",
            "version": "2.0.0",
            "timestamp": perf_status.get("timestamp"),
            "components": {
                "performance_monitoring": {
                    "status": perf_status.get("status"),
                    "metrics": perf_status.get("metrics"),
                    "alerts": perf_status.get("alerts")
                },
                "exception_handling": {
                    "total_exceptions": exc_summary.get("total_exceptions"),
                    "unresolved": exc_summary.get("unresolved_exceptions"),
                    "circuit_breakers": exc_summary.get("circuit_breakers")
                },
                "auto_scaling": {
                    "current_replicas": scaling_summary.get("current_replicas"),
                    "deployment_type": scaling_summary.get("deployment_type"),
                    "last_scaling": scaling_summary.get("last_scaling")
                }
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "service": "AI Navigation Assistant",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
