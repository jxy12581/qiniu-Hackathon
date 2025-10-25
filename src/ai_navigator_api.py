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

app = FastAPI(
    title="AI Navigation Assistant API",
    description="AI-powered navigation assistant supporting Baidu Maps and Amap with natural language interface",
    version="1.0.0"
)

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
    
    from_match = re.search(r'(?:从|出发自|起点|start from|from)\s*([^到去至,，]+)', query)
    if from_match:
        result["origin"] = from_match.group(1).strip()
    
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
            r'(?:到|去|至|导航到|navigate to|to)\s*([^,，。\n]+)',
            r'(?:终点|目的地|destination)\s*(?:是|为|:)?\s*([^,，。\n]+)',
        ]
        
        for pattern in to_patterns:
            to_match = re.search(pattern, query)
            if to_match:
                result["destination"] = to_match.group(1).strip()
                break
    
    if not result["origin"]:
        origin_patterns = [
            r'^([^从到去至]+?)(?:到|去|至)',
            r'([^,，]+?)(?:出发|开始)',
        ]
        for pattern in origin_patterns:
            origin_match = re.search(pattern, query)
            if origin_match:
                result["origin"] = origin_match.group(1).strip()
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
    try:
        origin_encoded = quote(request.origin)
        destination_encoded = quote(request.destination)
        
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
    try:
        if len(request.destinations) < 2:
            raise HTTPException(status_code=400, detail="At least 2 destinations required")
        
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
    try:
        location_encoded = quote(request.location)
        
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
    try:
        parsed = parse_natural_language(request.query)
        
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
