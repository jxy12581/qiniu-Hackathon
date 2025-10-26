#!/usr/bin/env python3
"""
Travel Itinerary Module
Generate detailed multi-day travel itineraries with navigation support
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from destination_reminder import DestinationReminder


class TravelItinerary:
    """Generate and manage multi-day travel itineraries"""
    
    def __init__(self):
        self.reminder = DestinationReminder()
        self.itineraries = self._init_itinerary_database()
    
    def _init_itinerary_database(self) -> Dict:
        """Initialize predefined itineraries for popular routes"""
        return {
            "北京-昆明-10天": {
                "title": "北京到昆明10天深度游",
                "description": "探索历史文化名城北京,再前往四季如春的昆明,体验云南独特的自然风光和民族文化",
                "duration_days": 10,
                "origin": "北京",
                "destination": "昆明",
                "transportation": {
                    "to_destination": {
                        "method": "飞机",
                        "duration": "约3.5小时",
                        "tips": "建议预订早班飞机,当天可以到达后游览昆明市区"
                    },
                    "return": {
                        "method": "飞机",
                        "duration": "约3.5小时",
                        "tips": "返程建议选择下午或晚上的航班"
                    }
                },
                "days": [
                    {
                        "day": 1,
                        "title": "北京市区游览",
                        "location": "北京",
                        "activities": [
                            {
                                "time": "08:00-12:00",
                                "activity": "天安门广场-故宫博物院",
                                "description": "参观世界上最大的城市广场和中国古代皇家宫殿",
                                "tips": "建议提前在线购票,避开周末高峰期"
                            },
                            {
                                "time": "12:00-13:30",
                                "activity": "午餐",
                                "description": "品尝北京烤鸭(全聚德或便宜坊)",
                                "tips": "提前预订,用餐高峰期需要等位"
                            },
                            {
                                "time": "14:00-17:00",
                                "activity": "天坛公园",
                                "description": "游览明清皇帝祭天的场所,欣赏古代建筑艺术",
                                "tips": "推荐购买联票,包含祈年殿、回音壁等主要景点"
                            },
                            {
                                "time": "18:00-20:00",
                                "activity": "王府井大街",
                                "description": "逛北京著名商业街,品尝小吃",
                                "tips": "王府井小吃街有各种北京特色小吃"
                            }
                        ],
                        "accommodation": "北京市区酒店",
                        "estimated_cost": "500-800元"
                    },
                    {
                        "day": 2,
                        "title": "长城一日游",
                        "location": "北京",
                        "activities": [
                            {
                                "time": "07:00-09:00",
                                "activity": "前往八达岭长城",
                                "description": "乘坐旅游巴士或地铁前往",
                                "tips": "建议早点出发,避开旅游团高峰"
                            },
                            {
                                "time": "09:00-14:00",
                                "activity": "游览八达岭长城",
                                "description": "攀登万里长城,感受壮丽景色",
                                "tips": "穿舒适的运动鞋,携带足够的水和食物"
                            },
                            {
                                "time": "14:00-15:00",
                                "activity": "午餐",
                                "description": "长城脚下用餐",
                                "tips": "景区餐饮较贵,可自备干粮"
                            },
                            {
                                "time": "15:00-17:00",
                                "activity": "返回市区",
                                "description": "返回北京市区休整",
                                "tips": "傍晚可在酒店附近逛逛"
                            },
                            {
                                "time": "18:00-20:00",
                                "activity": "南锣鼓巷",
                                "description": "体验老北京胡同文化",
                                "tips": "晚上更有氛围,有各种特色小店"
                            }
                        ],
                        "accommodation": "北京市区酒店",
                        "estimated_cost": "400-600元"
                    },
                    {
                        "day": 3,
                        "title": "颐和园-圆明园游览",
                        "location": "北京",
                        "activities": [
                            {
                                "time": "08:00-12:00",
                                "activity": "颐和园",
                                "description": "游览中国现存最大的皇家园林",
                                "tips": "建议乘船游览昆明湖,体验皇家园林之美"
                            },
                            {
                                "time": "12:00-13:30",
                                "activity": "午餐",
                                "description": "附近用餐",
                                "tips": "可选择宫廷菜或北京家常菜"
                            },
                            {
                                "time": "14:00-17:00",
                                "activity": "圆明园遗址公园",
                                "description": "参观万园之园遗址,了解历史",
                                "tips": "门票便宜,适合散步和拍照"
                            },
                            {
                                "time": "17:30-19:00",
                                "activity": "晚餐",
                                "description": "品尝老北京铜锅涮肉",
                                "tips": "推荐东来顺、聚宝源等老字号"
                            }
                        ],
                        "accommodation": "北京市区酒店",
                        "estimated_cost": "400-600元"
                    },
                    {
                        "day": 4,
                        "title": "北京飞往昆明",
                        "location": "北京-昆明",
                        "activities": [
                            {
                                "time": "08:00-09:30",
                                "activity": "前往机场",
                                "description": "退房后前往北京首都机场或大兴机场",
                                "tips": "提前2小时到达机场办理登机手续"
                            },
                            {
                                "time": "11:00-14:30",
                                "activity": "飞往昆明",
                                "description": "搭乘航班飞往昆明长水国际机场",
                                "tips": "航班时间约3.5小时,注意北京和昆明无时差"
                            },
                            {
                                "time": "15:00-16:30",
                                "activity": "机场前往市区",
                                "description": "乘坐地铁6号线或机场大巴到达市区酒店",
                                "tips": "地铁最方便快捷,约1小时到市区"
                            },
                            {
                                "time": "17:00-19:00",
                                "activity": "翠湖公园",
                                "description": "傍晚在翠湖公园散步,感受昆明的惬意",
                                "tips": "免费公园,冬季可以观赏红嘴鸥"
                            },
                            {
                                "time": "19:00-20:30",
                                "activity": "晚餐",
                                "description": "品尝云南特色过桥米线",
                                "tips": "推荐桥香园、建新园等知名店"
                            }
                        ],
                        "accommodation": "昆明市区酒店",
                        "estimated_cost": "800-1500元(含机票)"
                    },
                    {
                        "day": 5,
                        "title": "石林风景区一日游",
                        "location": "昆明",
                        "activities": [
                            {
                                "time": "07:30-09:30",
                                "activity": "前往石林",
                                "description": "从昆明市区出发前往石林风景区",
                                "tips": "可在昆明东部客运站乘坐直达巴士,车程约2小时"
                            },
                            {
                                "time": "09:30-15:00",
                                "activity": "游览石林景区",
                                "description": "探索世界自然遗产,欣赏喀斯特地貌奇观",
                                "tips": "景区很大,建议跟随导游或使用语音导览,穿舒适的鞋"
                            },
                            {
                                "time": "12:00-13:00",
                                "activity": "午餐",
                                "description": "景区内或附近用餐",
                                "tips": "可品尝彝族特色菜"
                            },
                            {
                                "time": "15:00-17:00",
                                "activity": "返回昆明",
                                "description": "乘车返回昆明市区",
                                "tips": "注意末班车时间"
                            },
                            {
                                "time": "18:00-20:00",
                                "activity": "金马碧鸡坊",
                                "description": "游览昆明地标建筑,夜景很美",
                                "tips": "附近有南屏步行街,可以逛街购物"
                            }
                        ],
                        "accommodation": "昆明市区酒店",
                        "estimated_cost": "400-600元"
                    },
                    {
                        "day": 6,
                        "title": "滇池-西山龙门",
                        "location": "昆明",
                        "activities": [
                            {
                                "time": "08:00-10:00",
                                "activity": "前往海埂公园",
                                "description": "滇池边的公园,可以近距离接触红嘴鸥(冬季)",
                                "tips": "可乘坐公交或打车前往"
                            },
                            {
                                "time": "10:00-12:00",
                                "activity": "乘索道上西山",
                                "description": "乘坐龙门索道上山,或选择徒步",
                                "tips": "索道可欣赏滇池全景,但冬季排队人多"
                            },
                            {
                                "time": "12:00-13:30",
                                "activity": "午餐",
                                "description": "山上或山脚用餐",
                                "tips": "推荐品尝汽锅鸡"
                            },
                            {
                                "time": "13:30-16:00",
                                "activity": "西山龙门",
                                "description": "游览龙门石窟,俯瞰滇池美景",
                                "tips": "悬崖栈道较窄,注意安全"
                            },
                            {
                                "time": "16:30-18:00",
                                "activity": "返回市区",
                                "description": "下山返回昆明市区",
                                "tips": "可在滇池边散步看日落"
                            },
                            {
                                "time": "18:30-20:00",
                                "activity": "晚餐",
                                "description": "品尝野生菌火锅(雨季)或其他云南特色菜",
                                "tips": "推荐云海肴、小锅巴等连锁餐厅"
                            }
                        ],
                        "accommodation": "昆明市区酒店",
                        "estimated_cost": "400-600元"
                    },
                    {
                        "day": 7,
                        "title": "云南民族村-官渡古镇",
                        "location": "昆明",
                        "activities": [
                            {
                                "time": "08:30-12:30",
                                "activity": "云南民族村",
                                "description": "了解云南26个民族的文化和风俗",
                                "tips": "有民族歌舞表演,注意演出时间"
                            },
                            {
                                "time": "12:30-14:00",
                                "activity": "午餐",
                                "description": "民族村内或附近品尝各民族特色美食",
                                "tips": "可品尝傣族菜、白族菜等"
                            },
                            {
                                "time": "14:30-17:30",
                                "activity": "官渡古镇",
                                "description": "游览千年历史古镇,品尝官渡粑粑",
                                "tips": "免费景点,适合拍照和品尝小吃"
                            },
                            {
                                "time": "18:00-20:00",
                                "activity": "晚餐及购物",
                                "description": "南屏街或金鹰购物中心",
                                "tips": "可采购云南特产:鲜花饼、普洱茶等"
                            }
                        ],
                        "accommodation": "昆明市区酒店",
                        "estimated_cost": "400-500元"
                    },
                    {
                        "day": 8,
                        "title": "九乡风景区",
                        "location": "昆明",
                        "activities": [
                            {
                                "time": "08:00-10:00",
                                "activity": "前往九乡",
                                "description": "从昆明市区前往九乡风景区",
                                "tips": "可在东部客运站乘车,车程约2小时"
                            },
                            {
                                "time": "10:00-15:00",
                                "activity": "游览九乡溶洞",
                                "description": "探索地下溶洞奇观,乘坐地下河船",
                                "tips": "溶洞内较冷,建议带外套;地面湿滑注意安全"
                            },
                            {
                                "time": "12:00-13:00",
                                "activity": "午餐",
                                "description": "景区内简餐",
                                "tips": "可自备零食"
                            },
                            {
                                "time": "15:00-17:00",
                                "activity": "返回昆明",
                                "description": "乘车返回市区",
                                "tips": "回程可在车上休息"
                            },
                            {
                                "time": "18:00-20:00",
                                "activity": "祥云美食城",
                                "description": "品尝各类云南小吃",
                                "tips": "汇集了云南各地美食,价格实惠"
                            }
                        ],
                        "accommodation": "昆明市区酒店",
                        "estimated_cost": "400-600元"
                    },
                    {
                        "day": 9,
                        "title": "昆明市区休闲游",
                        "location": "昆明",
                        "activities": [
                            {
                                "time": "09:00-11:30",
                                "activity": "云南省博物馆",
                                "description": "了解云南历史文化和少数民族文化",
                                "tips": "免费参观,需提前预约,周一闭馆"
                            },
                            {
                                "time": "12:00-13:30",
                                "activity": "午餐",
                                "description": "品尝昆明特色烧饵块、豆花米线",
                                "tips": "推荐老字号小吃店"
                            },
                            {
                                "time": "14:00-17:00",
                                "activity": "世界园艺博览园",
                                "description": "游览大型植物园,欣赏各国园林艺术",
                                "tips": "园区很大,可乘坐观光车"
                            },
                            {
                                "time": "17:30-19:00",
                                "activity": "购物及打包行李",
                                "description": "采购最后的云南特产",
                                "tips": "预留时间整理行李,准备返程"
                            },
                            {
                                "time": "19:00-20:30",
                                "activity": "告别晚餐",
                                "description": "最后品尝云南美食",
                                "tips": "可选择汽锅鸡、过桥米线等特色菜"
                            }
                        ],
                        "accommodation": "昆明市区酒店",
                        "estimated_cost": "400-500元"
                    },
                    {
                        "day": 10,
                        "title": "返回北京",
                        "location": "昆明-北京",
                        "activities": [
                            {
                                "time": "08:00-09:30",
                                "activity": "酒店退房",
                                "description": "退房前往机场",
                                "tips": "提前检查行李,别忘记特产"
                            },
                            {
                                "time": "10:00-10:30",
                                "activity": "到达机场",
                                "description": "办理登机手续",
                                "tips": "提前2小时到达机场"
                            },
                            {
                                "time": "12:00-15:30",
                                "activity": "返回北京",
                                "description": "搭乘航班返回北京",
                                "tips": "航班时间约3.5小时"
                            },
                            {
                                "time": "16:00-17:30",
                                "activity": "到达北京",
                                "description": "结束愉快的旅程",
                                "tips": "注意检查随身物品,安全到家"
                            }
                        ],
                        "accommodation": "-",
                        "estimated_cost": "800-1500元(含机票)"
                    }
                ],
                "total_estimated_cost": "6000-9500元(不含机票约4500-6500元)",
                "packing_list": [
                    "身份证、护照等证件",
                    "换洗衣物(春秋装为主,带一件外套)",
                    "舒适的运动鞋",
                    "防晒霜、太阳镜、遮阳帽",
                    "常用药品(感冒药、肠胃药等)",
                    "充电器、充电宝",
                    "相机或手机(拍照)",
                    "雨伞或雨衣",
                    "背包或行李箱"
                ],
                "important_tips": [
                    "提前预订机票和酒店可节省费用",
                    "热门景点建议提前在线购票",
                    "昆明紫外线强,注意防晒",
                    "早晚温差大,注意增减衣物",
                    "尊重少数民族风俗习惯",
                    "品尝野生菌务必煮熟,避免中毒",
                    "保管好贵重物品和证件",
                    "建议购买旅游保险"
                ]
            }
        }
    
    def get_itinerary(self, route_key: str) -> Optional[Dict]:
        """
        Get predefined itinerary by route key
        
        Args:
            route_key: Route identifier (e.g., "北京-昆明-10天")
            
        Returns:
            Itinerary dictionary or None if not found
        """
        return self.itineraries.get(route_key)
    
    def generate_itinerary_message(self, itinerary: Dict) -> str:
        """
        Format itinerary into a readable message
        
        Args:
            itinerary: Itinerary dictionary
            
        Returns:
            Formatted itinerary message
        """
        if not itinerary:
            return "❌ 未找到相关旅行攻略"
        
        message = f"# {itinerary['title']}\n\n"
        message += f"**{itinerary['description']}**\n\n"
        message += f"📅 行程天数: {itinerary['duration_days']}天\n"
        message += f"🚩 起点: {itinerary['origin']}\n"
        message += f"🎯 终点: {itinerary['destination']}\n"
        message += f"💰 预计费用: {itinerary['total_estimated_cost']}\n\n"
        
        message += "## 🚄 交通方式\n\n"
        trans = itinerary['transportation']
        message += f"**去程**: {trans['to_destination']['method']} ({trans['to_destination']['duration']})\n"
        message += f"💡 {trans['to_destination']['tips']}\n\n"
        message += f"**返程**: {trans['return']['method']} ({trans['return']['duration']})\n"
        message += f"💡 {trans['return']['tips']}\n\n"
        
        message += "## 📋 详细行程\n\n"
        
        for day_info in itinerary['days']:
            message += f"### Day {day_info['day']}: {day_info['title']}\n\n"
            message += f"📍 地点: {day_info['location']}\n\n"
            
            for activity in day_info['activities']:
                message += f"**{activity['time']}** - {activity['activity']}\n"
                message += f"- {activity['description']}\n"
                if activity.get('tips'):
                    message += f"- 💡 {activity['tips']}\n"
                message += "\n"
            
            message += f"🏨 住宿: {day_info['accommodation']}\n"
            message += f"💵 预计花费: {day_info['estimated_cost']}\n\n"
            message += "---\n\n"
        
        message += "## 🎒 行李清单\n\n"
        for item in itinerary['packing_list']:
            message += f"- {item}\n"
        message += "\n"
        
        message += "## ⚠️ 重要提示\n\n"
        for tip in itinerary['important_tips']:
            message += f"- {tip}\n"
        message += "\n"
        
        return message
    
    def get_navigation_info(self, origin: str, destination: str) -> Dict:
        """
        Get navigation information between two locations
        
        Args:
            origin: Starting point
            destination: Destination
            
        Returns:
            Navigation information dictionary
        """
        return {
            "origin": origin,
            "destination": destination,
            "baidu_map_url": f"https://map.baidu.com/direction?origin={origin}&destination={destination}&mode=driving",
            "amap_url": f"https://uri.amap.com/navigation?from={origin}&to={destination}&mode=car",
            "tips": "建议使用地图应用规划具体路线,并查看实时路况"
        }
