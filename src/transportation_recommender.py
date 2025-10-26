#!/usr/bin/env python3
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel
from datetime import datetime
import re


class TransportationOption(BaseModel):
    mode: str
    name: str
    description: str
    typical_speed: str
    cost_range: str
    suitable_distance: str
    pros: List[str]
    cons: List[str]
    best_use_cases: List[str]


class RouteRecommendation(BaseModel):
    origin: str
    destination: str
    recommended_mode: str
    alternative_modes: List[str]
    estimated_distance: str
    estimated_duration: Dict[str, str]
    cost_estimate: Dict[str, str]
    recommendation_reason: str
    tips: List[str]


class TransportationRecommender:
    
    TRANSPORTATION_MODES = {
        "driving": TransportationOption(
            mode="driving",
            name="驾车",
            description="自驾或打车",
            typical_speed="40-80 km/h (市区), 80-120 km/h (高速)",
            cost_range="油费: 0.6-1.0元/公里, 打车: 2-3元/公里起",
            suitable_distance="5公里以上，长途最佳",
            pros=[
                "灵活自由，随时出发",
                "适合携带大量行李",
                "可直达目的地，无需换乘",
                "适合多人出行(分摊成本)",
                "舒适度高"
            ],
            cons=[
                "市区易堵车",
                "停车费用和难度",
                "长途驾驶疲劳",
                "单人成本较高",
                "需要驾照和熟悉路况"
            ],
            best_use_cases=[
                "长途旅行(200公里以上)",
                "行李较多时",
                "多人出行",
                "偏远地区公共交通不便",
                "需要途中停靠多个地点"
            ]
        ),
        "transit": TransportationOption(
            mode="transit",
            name="公共交通",
            description="地铁、公交、高铁等",
            typical_speed="地铁: 35-40 km/h, 高铁: 200-350 km/h",
            cost_range="地铁/公交: 2-10元, 高铁: 0.4-0.8元/公里",
            suitable_distance="中短途(50公里内地铁/公交), 长途(高铁)",
            pros=[
                "经济实惠",
                "准时可靠(地铁/高铁)",
                "环保低碳",
                "避免堵车(地铁)",
                "不需要驾照",
                "可在途中休息或工作"
            ],
            cons=[
                "需要换乘，不够灵活",
                "高峰期拥挤",
                "携带行李不便",
                "站点可能离目的地有距离",
                "受运营时间限制"
            ],
            best_use_cases=[
                "市区通勤",
                "中长途城际旅行(高铁)",
                "预算有限",
                "避免拥堵",
                "环保出行"
            ]
        ),
        "walking": TransportationOption(
            mode="walking",
            name="步行",
            description="徒步",
            typical_speed="4-6 km/h",
            cost_range="免费",
            suitable_distance="3公里以内",
            pros=[
                "完全免费",
                "健康锻炼",
                "零污染",
                "欣赏沿途风景",
                "最灵活，任意路线"
            ],
            cons=[
                "速度慢",
                "仅适合短距离",
                "受天气影响大",
                "体力消耗",
                "携带行李困难"
            ],
            best_use_cases=[
                "短距离出行(1-3公里)",
                "景区游览",
                "晨练或散步",
                "交通拥堵时的短途替代",
                "环境优美的路线"
            ]
        ),
        "riding": TransportationOption(
            mode="riding",
            name="骑行",
            description="自行车或共享单车",
            typical_speed="10-20 km/h",
            cost_range="共享单车: 1.5-3元/次, 自有单车: 免费",
            suitable_distance="5-15公里",
            pros=[
                "经济实惠",
                "灵活便捷",
                "锻炼身体",
                "环保",
                "避免堵车",
                "适合短中距离"
            ],
            cons=[
                "受天气影响",
                "体力消耗",
                "速度有限",
                "携带行李不便",
                "非机动车道拥挤",
                "安全风险"
            ],
            best_use_cases=[
                "中短距离出行(5-15公里)",
                "城市休闲骑行",
                "避免拥堵的通勤",
                "景区游览",
                "天气良好时"
            ]
        ),
        "taxi": TransportationOption(
            mode="taxi",
            name="出租车/网约车",
            description="出租车或滴滴等网约车",
            typical_speed="40-60 km/h (市区)",
            cost_range="起步价15元, 2-3元/公里",
            suitable_distance="3-50公里",
            pros=[
                "门到门服务",
                "舒适便捷",
                "随叫随到",
                "适合夜间出行",
                "司机熟悉路况"
            ],
            cons=[
                "成本较高",
                "高峰期涨价",
                "可能遇到堵车",
                "可能需要等待",
                "长途成本高"
            ],
            best_use_cases=[
                "紧急出行",
                "夜间出行",
                "行李较多",
                "不熟悉路线",
                "中短途舒适出行"
            ]
        ),
        "high_speed_rail": TransportationOption(
            mode="high_speed_rail",
            name="高铁/动车",
            description="高速铁路",
            typical_speed="200-350 km/h",
            cost_range="0.4-0.8元/公里",
            suitable_distance="100公里以上",
            pros=[
                "速度快",
                "准时可靠",
                "舒适安全",
                "环保",
                "可在途中休息工作",
                "不受天气影响"
            ],
            cons=[
                "需要到车站，可能不在市中心",
                "需要提前购票",
                "发车时间固定",
                "短途性价比低",
                "高峰期一票难求"
            ],
            best_use_cases=[
                "城际长途旅行(100-1500公里)",
                "商务出行",
                "追求时间效率",
                "舒适出行"
            ]
        ),
        "airplane": TransportationOption(
            mode="airplane",
            name="飞机",
            description="航空",
            typical_speed="700-900 km/h",
            cost_range="因距离和航线差异大，通常200-2000+元",
            suitable_distance="800公里以上",
            pros=[
                "速度最快",
                "适合超长距离",
                "相对安全",
                "可跨越自然障碍"
            ],
            cons=[
                "成本较高",
                "需要提前到机场(2小时)",
                "受天气影响",
                "安检流程复杂",
                "行李限制",
                "机场通常离市区远"
            ],
            best_use_cases=[
                "超长距离(800公里以上)",
                "时间紧迫",
                "跨省跨国旅行",
                "海岛或偏远地区"
            ]
        )
    }
    
    DISTANCE_RANGES = {
        "very_short": (0, 3),
        "short": (3, 15),
        "medium": (15, 100),
        "long": (100, 500),
        "very_long": (500, float('inf'))
    }
    
    def __init__(self):
        self.transportation_modes = self.TRANSPORTATION_MODES
        self.distance_ranges = self.DISTANCE_RANGES
    
    def get_distance_category(self, distance_km: float) -> str:
        for category, (min_dist, max_dist) in self.distance_ranges.items():
            if min_dist <= distance_km < max_dist:
                return category
        return "very_long"
    
    def recommend_transportation(
        self,
        origin: str,
        destination: str,
        estimated_distance_km: Optional[float] = None,
        trip_purpose: Optional[Literal["通勤", "旅游", "商务", "紧急"]] = None,
        luggage: Optional[Literal["无", "少量", "较多"]] = None,
        budget: Optional[Literal["经济", "标准", "舒适"]] = None,
        time_sensitive: bool = False
    ) -> RouteRecommendation:
        
        if estimated_distance_km is None:
            estimated_distance_km = self._estimate_distance(origin, destination)
        
        distance_category = self.get_distance_category(estimated_distance_km)
        
        recommendations = self._generate_recommendations(
            distance_category=distance_category,
            distance_km=estimated_distance_km,
            trip_purpose=trip_purpose,
            luggage=luggage,
            budget=budget,
            time_sensitive=time_sensitive
        )
        
        estimated_duration = self._calculate_duration(estimated_distance_km, recommendations)
        cost_estimate = self._calculate_cost(estimated_distance_km, recommendations)
        
        tips = self._generate_tips(
            recommendations["primary"],
            distance_category,
            trip_purpose,
            luggage
        )
        
        return RouteRecommendation(
            origin=origin,
            destination=destination,
            recommended_mode=recommendations["primary"],
            alternative_modes=recommendations["alternatives"],
            estimated_distance=f"约 {estimated_distance_km} 公里",
            estimated_duration=estimated_duration,
            cost_estimate=cost_estimate,
            recommendation_reason=recommendations["reason"],
            tips=tips
        )
    
    def _estimate_distance(self, origin: str, destination: str) -> float:
        city_distances = {
            ("北京", "上海"): 1200,
            ("北京", "广州"): 2000,
            ("上海", "杭州"): 170,
            ("北京", "天津"): 120,
            ("上海", "南京"): 300,
            ("广州", "深圳"): 120,
            ("成都", "重庆"): 300,
        }
        
        for (city1, city2), distance in city_distances.items():
            if (city1 in origin and city2 in destination) or (city2 in origin and city1 in destination):
                return distance
        
        return 50
    
    def _generate_recommendations(
        self,
        distance_category: str,
        distance_km: float,
        trip_purpose: Optional[str],
        luggage: Optional[str],
        budget: Optional[str],
        time_sensitive: bool
    ) -> Dict[str, any]:
        
        if distance_category == "very_short":
            if luggage == "较多" or trip_purpose == "紧急":
                return {
                    "primary": "taxi",
                    "alternatives": ["riding", "walking"],
                    "reason": "短距离出行，打车最便捷。若预算有限且行李不多，可选择骑行或步行。"
                }
            elif budget == "经济":
                return {
                    "primary": "walking",
                    "alternatives": ["riding", "transit"],
                    "reason": "短距离出行，步行即可到达，经济环保。若想稍快，可选择骑行。"
                }
            else:
                return {
                    "primary": "riding",
                    "alternatives": ["walking", "taxi"],
                    "reason": "短距离出行，骑行速度适中且经济，是理想选择。"
                }
        
        elif distance_category == "short":
            if luggage == "较多" or trip_purpose == "紧急":
                return {
                    "primary": "taxi",
                    "alternatives": ["transit", "driving"],
                    "reason": "中短距离，行李较多或时间紧急，打车最为便捷。"
                }
            elif budget == "经济":
                return {
                    "primary": "transit",
                    "alternatives": ["riding", "taxi"],
                    "reason": "中短距离，公共交通经济实惠，地铁可避免拥堵。"
                }
            else:
                return {
                    "primary": "transit",
                    "alternatives": ["driving", "riding"],
                    "reason": "中短距离，公共交通平衡了速度与成本，是最佳选择。"
                }
        
        elif distance_category == "medium":
            if trip_purpose == "商务" or time_sensitive:
                return {
                    "primary": "high_speed_rail",
                    "alternatives": ["driving", "taxi"],
                    "reason": "中长距离商务出行，高铁快速准时，舒适度高。"
                }
            elif luggage == "较多":
                return {
                    "primary": "driving",
                    "alternatives": ["high_speed_rail", "taxi"],
                    "reason": "中长距离，行李较多，自驾更方便灵活，可直达目的地。"
                }
            elif budget == "经济":
                return {
                    "primary": "transit",
                    "alternatives": ["high_speed_rail", "driving"],
                    "reason": "中长距离，普通列车或大巴最经济，高铁速度更快但稍贵。"
                }
            else:
                return {
                    "primary": "high_speed_rail",
                    "alternatives": ["driving", "transit"],
                    "reason": "中长距离，高铁速度快且舒适，是首选交通方式。"
                }
        
        elif distance_category == "long":
            if time_sensitive or trip_purpose == "商务":
                return {
                    "primary": "airplane",
                    "alternatives": ["high_speed_rail"],
                    "reason": "长途距离且时间紧迫，飞机最快，高铁次之。"
                }
            elif budget == "经济":
                return {
                    "primary": "high_speed_rail",
                    "alternatives": ["transit", "airplane"],
                    "reason": "长途旅行，高铁性价比高，速度与成本平衡好。普通列车更便宜但耗时长。"
                }
            else:
                return {
                    "primary": "high_speed_rail",
                    "alternatives": ["airplane", "driving"],
                    "reason": "长途距离，高铁舒适快捷，是长途旅行的理想选择。若预算充足可选飞机。"
                }
        
        else:
            return {
                "primary": "airplane",
                "alternatives": ["high_speed_rail"],
                "reason": "超长距离，飞机是唯一实际选择，速度最快。"
            }
    
    def _calculate_duration(self, distance_km: float, recommendations: Dict) -> Dict[str, str]:
        speed_map = {
            "walking": 5,
            "riding": 15,
            "driving": 60,
            "transit": 40,
            "taxi": 50,
            "high_speed_rail": 250,
            "airplane": 700
        }
        
        durations = {}
        primary = recommendations["primary"]
        
        for mode in [primary] + recommendations["alternatives"][:2]:
            if mode in speed_map:
                hours = distance_km / speed_map[mode]
                if mode == "airplane":
                    hours += 2.5
                elif mode == "high_speed_rail":
                    hours += 1.0
                
                if hours < 1:
                    durations[self.transportation_modes[mode].name] = f"{int(hours * 60)} 分钟"
                else:
                    durations[self.transportation_modes[mode].name] = f"{hours:.1f} 小时"
        
        return durations
    
    def _calculate_cost(self, distance_km: float, recommendations: Dict) -> Dict[str, str]:
        cost_map = {
            "walking": 0,
            "riding": 3,
            "driving": lambda d: d * 0.8,
            "transit": lambda d: min(d * 0.15, 100),
            "taxi": lambda d: 15 + d * 2.5,
            "high_speed_rail": lambda d: d * 0.6,
            "airplane": lambda d: max(200, d * 0.5)
        }
        
        costs = {}
        primary = recommendations["primary"]
        
        for mode in [primary] + recommendations["alternatives"][:2]:
            if mode in cost_map:
                cost_func = cost_map[mode]
                if callable(cost_func):
                    cost = cost_func(distance_km)
                    costs[self.transportation_modes[mode].name] = f"约 {int(cost)} 元"
                else:
                    if cost_func == 0:
                        costs[self.transportation_modes[mode].name] = "免费"
                    else:
                        costs[self.transportation_modes[mode].name] = f"约 {cost_func} 元"
        
        return costs
    
    def _generate_tips(
        self,
        mode: str,
        distance_category: str,
        trip_purpose: Optional[str],
        luggage: Optional[str]
    ) -> List[str]:
        
        general_tips = {
            "walking": [
                "穿着舒适的鞋子",
                "查看天气预报，准备雨具",
                "注意交通安全，走人行道",
                "规划好路线，使用地图导航"
            ],
            "riding": [
                "佩戴头盔，注意安全",
                "检查车况，确保刹车有效",
                "遵守交通规则，走非机动车道",
                "注意天气，避免雨雪天骑行",
                "使用共享单车前检查车况"
            ],
            "driving": [
                "出发前检查车况和油量",
                "规划路线，避开拥堵路段",
                "提前了解目的地停车情况",
                "长途驾驶注意休息，避免疲劳驾驶",
                "遵守交通规则，系好安全带"
            ],
            "transit": [
                "查询地铁/公交线路和时刻表",
                "避开高峰期，错峰出行",
                "准备零钱或交通卡",
                "预留换乘时间",
                "注意列车运营时间"
            ],
            "taxi": [
                "高峰期提前叫车",
                "核对车牌和司机信息",
                "选择正规平台，注意安全",
                "保管好随身物品",
                "提前告知目的地，避免绕路"
            ],
            "high_speed_rail": [
                "提前购票，避免一票难求",
                "至少提前30分钟到站",
                "携带有效身份证件",
                "了解行李限制",
                "注意检票时间和站台信息",
                "预订座位时考虑靠窗/过道偏好"
            ],
            "airplane": [
                "提前2-3小时到达机场",
                "网上值机节省时间",
                "了解行李托运规定",
                "携带有效证件(身份证/护照)",
                "关注航班动态，防止延误",
                "液体物品需符合安检规定"
            ]
        }
        
        tips = general_tips.get(mode, ["注意安全，遵守交通规则"])
        
        if luggage == "较多" and mode in ["walking", "riding"]:
            tips.append("⚠️ 注意：您有较多行李，可能不太适合此交通方式，建议考虑打车或自驾")
        
        if distance_category == "long" and mode == "driving":
            tips.append("💡 长途驾驶建议：每2小时休息一次，轮换驾驶员，注意高速公路服务区位置")
        
        return tips[:5]
    
    def parse_recommendation_query(self, query: str) -> Dict:
        result = {
            "origin": None,
            "destination": None,
            "trip_purpose": None,
            "luggage": None,
            "budget": None,
            "time_sensitive": False
        }
        
        from_patterns = [
            r'(?:从|出发自|起点)\s*([^到去至,，]+)',
        ]
        for pattern in from_patterns:
            match = re.search(pattern, query)
            if match:
                result["origin"] = match.group(1).strip()
                break
        
        to_patterns = [
            r'(?:到|去|至|前往)\s*([^,，。\n]+?)(?:,|，|。|的|怎么|用什么|$)',
        ]
        for pattern in to_patterns:
            match = re.search(pattern, query)
            if match:
                result["destination"] = match.group(1).strip()
                break
        
        if "通勤" in query or "上班" in query:
            result["trip_purpose"] = "通勤"
        elif "旅游" in query or "游玩" in query:
            result["trip_purpose"] = "旅游"
        elif "商务" in query or "出差" in query:
            result["trip_purpose"] = "商务"
        elif "紧急" in query or "急" in query:
            result["trip_purpose"] = "紧急"
        
        if "行李多" in query or "行李较多" in query or "东西多" in query:
            result["luggage"] = "较多"
        elif "行李少" in query or "轻装" in query:
            result["luggage"] = "少量"
        elif "没有行李" in query or "无行李" in query:
            result["luggage"] = "无"
        
        if "经济" in query or "便宜" in query or "省钱" in query:
            result["budget"] = "经济"
        elif "舒适" in query or "高端" in query:
            result["budget"] = "舒适"
        else:
            result["budget"] = "标准"
        
        if "时间紧" in query or "赶时间" in query or "最快" in query:
            result["time_sensitive"] = True
        
        return result
    
    def get_all_transportation_modes(self) -> List[TransportationOption]:
        return list(self.transportation_modes.values())
    
    def get_transportation_mode(self, mode: str) -> Optional[TransportationOption]:
        return self.transportation_modes.get(mode)
