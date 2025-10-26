#!/usr/bin/env python3
import re
from typing import List, Dict, Optional, Literal
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class Attraction(BaseModel):
    name: str
    category: str
    description: str
    recommended_duration: str
    best_time: str
    entrance_fee: str


class DayItinerary(BaseModel):
    day: int
    date: str
    attractions: List[str]
    activities: List[str]
    notes: str


class TravelBudget(BaseModel):
    transportation: float
    accommodation: float
    food: float
    tickets: float
    shopping: float
    total: float


class TravelGuide(BaseModel):
    destination: str
    duration_days: int
    travel_style: str
    itinerary: List[DayItinerary]
    recommended_attractions: List[Attraction]
    budget_estimate: TravelBudget
    travel_tips: List[str]
    best_season: str


class TravelGuidePlanner:
    
    CITY_ATTRACTIONS = {
        "北京": [
            Attraction(
                name="故宫博物院",
                category="历史文化",
                description="中国明清两代的皇家宫殿，世界文化遗产",
                recommended_duration="3-4小时",
                best_time="春秋季节，避开周一闭馆",
                entrance_fee="60元(旺季)/40元(淡季)"
            ),
            Attraction(
                name="长城(八达岭)",
                category="历史文化",
                description="世界七大奇迹之一，中国古代防御工程",
                recommended_duration="半天",
                best_time="春秋季节，早上人少",
                entrance_fee="40元"
            ),
            Attraction(
                name="天坛公园",
                category="历史文化",
                description="明清两代皇帝祭天祈谷的场所",
                recommended_duration="2-3小时",
                best_time="清晨看老人晨练",
                entrance_fee="15元"
            ),
            Attraction(
                name="颐和园",
                category="园林景观",
                description="中国现存最大的皇家园林",
                recommended_duration="半天",
                best_time="春夏季节",
                entrance_fee="30元(旺季)/20元(淡季)"
            ),
            Attraction(
                name="天安门广场",
                category="地标建筑",
                description="世界最大的城市广场",
                recommended_duration="1-2小时",
                best_time="清晨看升旗仪式",
                entrance_fee="免费"
            ),
        ],
        "上海": [
            Attraction(
                name="外滩",
                category="城市地标",
                description="上海的标志性景观，万国建筑博览群",
                recommended_duration="2-3小时",
                best_time="傍晚至夜景",
                entrance_fee="免费"
            ),
            Attraction(
                name="东方明珠",
                category="城市地标",
                description="上海地标性建筑，登高俯瞰城市",
                recommended_duration="2小时",
                best_time="傍晚看日落夜景",
                entrance_fee="180-260元"
            ),
            Attraction(
                name="南京路步行街",
                category="购物美食",
                description="中国最繁华的商业街之一",
                recommended_duration="2-3小时",
                best_time="傍晚至晚上",
                entrance_fee="免费"
            ),
            Attraction(
                name="豫园",
                category="园林景观",
                description="明代私家园林，江南园林代表",
                recommended_duration="2小时",
                best_time="上午或下午",
                entrance_fee="40元"
            ),
            Attraction(
                name="田子坊",
                category="文化艺术",
                description="上海特色创意园区，艺术文化街区",
                recommended_duration="2-3小时",
                best_time="下午",
                entrance_fee="免费"
            ),
        ],
        "杭州": [
            Attraction(
                name="西湖",
                category="自然景观",
                description="世界文化遗产，中国最著名的湖泊之一",
                recommended_duration="半天到一天",
                best_time="春秋季节，清晨或傍晚",
                entrance_fee="免费"
            ),
            Attraction(
                name="灵隐寺",
                category="宗教文化",
                description="中国佛教著名寺院之一",
                recommended_duration="2-3小时",
                best_time="清晨",
                entrance_fee="45元+30元(飞来峰景区+寺庙)"
            ),
            Attraction(
                name="雷峰塔",
                category="历史文化",
                description="西湖十景之一，白娘子传说所在地",
                recommended_duration="1-2小时",
                best_time="傍晚看日落",
                entrance_fee="40元"
            ),
            Attraction(
                name="宋城",
                category="主题公园",
                description="展现宋代文化的主题公园",
                recommended_duration="半天",
                best_time="下午观看演出",
                entrance_fee="310元(含演出)"
            ),
            Attraction(
                name="西溪湿地",
                category="自然景观",
                description="城市湿地公园，生态旅游胜地",
                recommended_duration="半天",
                best_time="春夏季节",
                entrance_fee="80元"
            ),
        ],
        "成都": [
            Attraction(
                name="大熊猫繁育研究基地",
                category="动物观赏",
                description="世界著名的大熊猫保护研究中心",
                recommended_duration="半天",
                best_time="上午8-10点(熊猫最活跃)",
                entrance_fee="55元"
            ),
            Attraction(
                name="宽窄巷子",
                category="历史文化",
                description="成都历史文化街区，体验老成都生活",
                recommended_duration="2-3小时",
                best_time="下午至晚上",
                entrance_fee="免费"
            ),
            Attraction(
                name="武侯祠",
                category="历史文化",
                description="中国唯一君臣合祀祠庙",
                recommended_duration="2小时",
                best_time="上午或下午",
                entrance_fee="60元"
            ),
            Attraction(
                name="锦里",
                category="文化美食",
                description="成都著名步行商业街，品尝四川美食",
                recommended_duration="2-3小时",
                best_time="傍晚至晚上",
                entrance_fee="免费"
            ),
            Attraction(
                name="都江堰",
                category="历史文化",
                description="世界文化遗产，古代水利工程",
                recommended_duration="半天",
                best_time="春夏季节",
                entrance_fee="80元"
            ),
        ],
        "西安": [
            Attraction(
                name="兵马俑",
                category="历史文化",
                description="世界八大奇迹之一，秦始皇陵陪葬坑",
                recommended_duration="半天",
                best_time="上午早些时候",
                entrance_fee="120元"
            ),
            Attraction(
                name="大雁塔",
                category="历史文化",
                description="唐代古塔，丝绸之路的象征",
                recommended_duration="2小时",
                best_time="傍晚看音乐喷泉",
                entrance_fee="50元"
            ),
            Attraction(
                name="城墙",
                category="历史文化",
                description="中国现存最完整的古城墙",
                recommended_duration="2-3小时",
                best_time="傍晚骑行",
                entrance_fee="54元"
            ),
            Attraction(
                name="回民街",
                category="美食文化",
                description="西安特色美食街区",
                recommended_duration="2-3小时",
                best_time="傍晚至晚上",
                entrance_fee="免费"
            ),
            Attraction(
                name="华清宫",
                category="历史文化",
                description="唐代皇家园林，杨贵妃沐浴之地",
                recommended_duration="半天",
                best_time="上午或下午",
                entrance_fee="120元"
            ),
        ],
    }
    
    TRAVEL_STYLES = {
        "深度游": {
            "daily_attractions": 2,
            "pace": "慢节奏，充分体验每个景点",
            "budget_multiplier": 1.3
        },
        "经典游": {
            "daily_attractions": 3,
            "pace": "适中节奏，游览主要景点",
            "budget_multiplier": 1.0
        },
        "打卡游": {
            "daily_attractions": 4,
            "pace": "快节奏，走马观花式游览",
            "budget_multiplier": 0.8
        }
    }
    
    def __init__(self):
        self.city_attractions = self.CITY_ATTRACTIONS
        self.travel_styles = self.TRAVEL_STYLES
    
    def get_attractions_for_city(self, city: str) -> List[Attraction]:
        for city_name in self.city_attractions.keys():
            if city_name in city or city in city_name:
                return self.city_attractions[city_name]
        return []
    
    def create_itinerary(
        self,
        destination: str,
        duration_days: int,
        travel_style: str = "经典游",
        start_date: Optional[str] = None
    ) -> TravelGuide:
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start = datetime.now()
        
        attractions = self.get_attractions_for_city(destination)
        if not attractions:
            raise ValueError(f"暂不支持{destination}的旅游攻略，目前支持: {', '.join(self.city_attractions.keys())}")
        
        style_config = self.travel_styles.get(travel_style, self.travel_styles["经典游"])
        daily_count = min(style_config["daily_attractions"], len(attractions))
        
        itinerary = []
        attraction_names = [a.name for a in attractions]
        
        for day in range(1, duration_days + 1):
            day_date = (start + timedelta(days=day-1)).strftime("%Y-%m-%d")
            start_idx = ((day - 1) * daily_count) % len(attraction_names)
            end_idx = start_idx + daily_count
            
            day_attractions = attraction_names[start_idx:end_idx]
            if len(day_attractions) < daily_count and len(attraction_names) > daily_count:
                remaining = daily_count - len(day_attractions)
                day_attractions.extend(attraction_names[:remaining])
            
            activities = self._generate_activities(day_attractions, attractions)
            
            itinerary.append(DayItinerary(
                day=day,
                date=day_date,
                attractions=day_attractions,
                activities=activities,
                notes=f"根据{travel_style}安排，{style_config['pace']}"
            ))
        
        budget = self._estimate_budget(destination, duration_days, travel_style)
        
        travel_tips = self._generate_travel_tips(destination)
        
        best_season = self._get_best_season(destination)
        
        return TravelGuide(
            destination=destination,
            duration_days=duration_days,
            travel_style=travel_style,
            itinerary=itinerary,
            recommended_attractions=attractions,
            budget_estimate=budget,
            travel_tips=travel_tips,
            best_season=best_season
        )
    
    def _generate_activities(self, day_attractions: List[str], all_attractions: List[Attraction]) -> List[str]:
        activities = []
        for attr_name in day_attractions:
            for attraction in all_attractions:
                if attraction.name == attr_name:
                    activities.append(f"游览{attraction.name} (建议{attraction.recommended_duration})")
                    break
        return activities
    
    def _estimate_budget(self, destination: str, duration_days: int, travel_style: str) -> TravelBudget:
        style_config = self.travel_styles.get(travel_style, self.travel_styles["经典游"])
        multiplier = style_config["budget_multiplier"]
        
        base_budget = {
            "北京": {"transport": 500, "hotel": 400, "food": 150, "ticket": 200},
            "上海": {"transport": 500, "hotel": 450, "food": 180, "ticket": 150},
            "杭州": {"transport": 400, "hotel": 350, "food": 140, "ticket": 120},
            "成都": {"transport": 450, "hotel": 300, "food": 120, "ticket": 150},
            "西安": {"transport": 400, "hotel": 280, "food": 100, "ticket": 180},
        }
        
        city_base = None
        for city_name in base_budget.keys():
            if city_name in destination or destination in city_name:
                city_base = base_budget[city_name]
                break
        
        if not city_base:
            city_base = {"transport": 450, "hotel": 350, "food": 150, "ticket": 150}
        
        transportation = city_base["transport"] * multiplier
        accommodation = city_base["hotel"] * duration_days * multiplier
        food = city_base["food"] * duration_days * multiplier
        tickets = city_base["ticket"] * duration_days * multiplier
        shopping = 500 * duration_days * multiplier * 0.5
        
        total = transportation + accommodation + food + tickets + shopping
        
        return TravelBudget(
            transportation=round(transportation, 2),
            accommodation=round(accommodation, 2),
            food=round(food, 2),
            tickets=round(tickets, 2),
            shopping=round(shopping, 2),
            total=round(total, 2)
        )
    
    def _generate_travel_tips(self, destination: str) -> List[str]:
        general_tips = [
            "提前预订酒店和景点门票，可享受优惠",
            "携带身份证件，部分景点需要实名制购票",
            "关注天气预报，准备相应的衣物和雨具",
            "下载离线地图，避免迷路",
            "准备一些常用药品(感冒药、创可贴等)",
            "尊重当地风俗习惯",
        ]
        
        city_specific_tips = {
            "北京": [
                "故宫需要提前网上预约购票",
                "地铁是最方便的交通工具",
                "北京烤鸭、炸酱面等特色美食值得品尝",
            ],
            "上海": [
                "可以购买上海公共交通卡方便出行",
                "外滩夜景最佳观赏时间是晚上7-9点",
                "小笼包、生煎包等本帮菜不容错过",
            ],
            "杭州": [
                "西湖景区很大，建议租用自行车或乘坐观光车",
                "龙井茶是杭州特产，可以品尝购买",
                "杭帮菜清淡鲜美，西湖醋鱼是代表菜",
            ],
            "成都": [
                "熊猫基地最好早上去，熊猫比较活跃",
                "成都火锅、串串香必须尝试",
                "市区交通拥堵，建议乘坐地铁",
            ],
            "西安": [
                "兵马俑景区较远，建议参加一日游或包车",
                "回民街美食众多，羊肉泡馍、肉夹馍必吃",
                "古城墙可以租自行车骑行，体验更佳",
            ],
        }
        
        tips = general_tips.copy()
        for city_name, city_tips in city_specific_tips.items():
            if city_name in destination or destination in city_name:
                tips.extend(city_tips)
                break
        
        return tips
    
    def _get_best_season(self, destination: str) -> str:
        seasons = {
            "北京": "春季(4-5月)和秋季(9-10月)，气候宜人，适合旅游",
            "上海": "春季(3-5月)和秋季(9-11月)，温度适中，降雨较少",
            "杭州": "春季(3-5月)和秋季(9-11月)，西湖景色最美",
            "成都": "春季(3-5月)和秋季(9-11月)，气候舒适，适合游玩",
            "西安": "春季(4-5月)和秋季(9-10月)，避开夏季高温和冬季严寒",
        }
        
        for city_name, season in seasons.items():
            if city_name in destination or destination in city_name:
                return season
        
        return "春秋季节通常是最佳旅游时间"
    
    def parse_travel_query(self, query: str) -> Dict:
        result = {
            "destination": None,
            "duration_days": 3,
            "travel_style": "经典游",
            "start_date": None
        }
        
        for city in self.city_attractions.keys():
            if city in query:
                result["destination"] = city
                break
        
        day_patterns = [
            r'(\d+)\s*天',
            r'(\d+)\s*日游',
        ]
        for pattern in day_patterns:
            match = re.search(pattern, query)
            if match:
                result["duration_days"] = int(match.group(1))
                break
        
        if "深度" in query or "深度游" in query:
            result["travel_style"] = "深度游"
        elif "打卡" in query or "快速" in query:
            result["travel_style"] = "打卡游"
        
        date_pattern = r'(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})'
        match = re.search(date_pattern, query)
        if match:
            year, month, day = match.groups()
            result["start_date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        return result
