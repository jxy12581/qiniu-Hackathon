#!/usr/bin/env python3
"""
Destination Reminder Module
Provides weather information and travel recommendations for destinations
"""
import requests
from typing import Dict, List, Optional
from urllib.parse import quote
import json


class DestinationReminder:
    """Handle destination weather and travel recommendations"""
    
    def __init__(self):
        self.weather_base_url = "https://wttr.in"
        
    def get_weather(self, location: str, language: str = "zh-CN") -> Dict:
        """
        Get weather information for a location
        
        Args:
            location: Location name (e.g., "北京", "上海")
            language: Language code (default: zh-CN for Chinese)
            
        Returns:
            Dictionary containing weather information
        """
        try:
            location_encoded = quote(location)
            url = f"{self.weather_base_url}/{location_encoded}?format=j1&lang=zh"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            current = data.get('current_condition', [{}])[0]
            weather_info = {
                "location": location,
                "current": {
                    "temperature": current.get('temp_C', 'N/A'),
                    "feels_like": current.get('FeelsLikeC', 'N/A'),
                    "condition": current.get('lang_zh', [{}])[0].get('value', current.get('weatherDesc', [{}])[0].get('value', 'N/A')) if current.get('lang_zh') else current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    "humidity": current.get('humidity', 'N/A'),
                    "wind_speed": current.get('windspeedKmph', 'N/A'),
                    "wind_dir": current.get('winddir16Point', 'N/A'),
                    "uv_index": current.get('uvIndex', 'N/A'),
                    "visibility": current.get('visibility', 'N/A')
                },
                "forecast": []
            }
            
            weather_data = data.get('weather', [])
            for day in weather_data[:3]:
                forecast_day = {
                    "date": day.get('date', 'N/A'),
                    "max_temp": day.get('maxtempC', 'N/A'),
                    "min_temp": day.get('mintempC', 'N/A'),
                    "condition": day.get('lang_zh', [{}])[0].get('value', day.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', 'N/A')) if day.get('lang_zh') else day.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    "sunrise": day.get('astronomy', [{}])[0].get('sunrise', 'N/A'),
                    "sunset": day.get('astronomy', [{}])[0].get('sunset', 'N/A'),
                    "avg_humidity": day.get('hourly', [{}])[0].get('humidity', 'N/A')
                }
                weather_info["forecast"].append(forecast_day)
            
            return weather_info
            
        except requests.RequestException as e:
            return {
                "error": f"获取天气信息失败: {str(e)}",
                "location": location
            }
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return {
                "error": f"解析天气数据失败: {str(e)}",
                "location": location
            }
    
    def format_weather_message(self, weather_info: Dict) -> str:
        """
        Format weather information into a readable message
        
        Args:
            weather_info: Weather data dictionary
            
        Returns:
            Formatted weather message string
        """
        if "error" in weather_info:
            return f"❌ {weather_info['error']}"
        
        current = weather_info.get("current", {})
        forecast = weather_info.get("forecast", [])
        location = weather_info.get("location", "未知地点")
        
        message = f"📍 {location} 天气信息\n\n"
        message += "🌡️ 当前天气:\n"
        message += f"  温度: {current.get('temperature', 'N/A')}°C (体感 {current.get('feels_like', 'N/A')}°C)\n"
        message += f"  状况: {current.get('condition', 'N/A')}\n"
        message += f"  湿度: {current.get('humidity', 'N/A')}%\n"
        message += f"  风速: {current.get('wind_speed', 'N/A')} km/h ({current.get('wind_dir', 'N/A')})\n"
        message += f"  紫外线指数: {current.get('uv_index', 'N/A')}\n"
        message += f"  能见度: {current.get('visibility', 'N/A')} km\n"
        
        if forecast:
            message += "\n📅 未来天气预报:\n"
            for i, day in enumerate(forecast, 1):
                message += f"\n  {i}. {day.get('date', 'N/A')}\n"
                message += f"     温度: {day.get('min_temp', 'N/A')}°C - {day.get('max_temp', 'N/A')}°C\n"
                message += f"     天气: {day.get('condition', 'N/A')}\n"
                message += f"     日出: {day.get('sunrise', 'N/A')} | 日落: {day.get('sunset', 'N/A')}\n"
        
        return message
    
    def get_travel_recommendations(self, location: str) -> Dict:
        """
        Get travel recommendations for a location
        
        Args:
            location: Location name
            
        Returns:
            Dictionary containing travel recommendations
        """
        recommendations = {
            "location": location,
            "tips": [],
            "best_time": "",
            "transportation": [],
            "attractions": [],
            "cuisine": []
        }
        
        location_lower = location.lower()
        
        tips_database = {
            "北京": {
                "best_time": "春季(3-5月)和秋季(9-11月)最佳,天气宜人",
                "tips": [
                    "提前在线预约故宫、长城等热门景点门票",
                    "避开国庆、春节等节假日高峰期",
                    "冬季天气寒冷,注意保暖",
                    "建议办理公交卡,方便乘坐地铁和公交"
                ],
                "transportation": [
                    "地铁网络发达,覆盖主要景点",
                    "首都机场和大兴机场都有机场快轨",
                    "共享单车适合短距离出行"
                ],
                "attractions": [
                    "故宫博物院 - 中国古代皇家宫殿",
                    "八达岭长城 - 明长城最具代表性的地段",
                    "天坛公园 - 明清皇帝祭天的场所",
                    "颐和园 - 中国现存最大的皇家园林",
                    "南锣鼓巷 - 老北京胡同文化体验"
                ],
                "cuisine": [
                    "北京烤鸭 - 全聚德、便宜坊",
                    "老北京炸酱面",
                    "铜锅涮肉",
                    "豆汁儿、焦圈(传统早餐)"
                ]
            },
            "上海": {
                "best_time": "春季(3-5月)和秋季(9-11月)最适宜游览",
                "tips": [
                    "外滩夜景最佳观赏时间为傍晚",
                    "迪士尼乐园建议购买快速通行证",
                    "梅雨季节(6-7月)记得带伞",
                    "使用上海地铁APP规划行程"
                ],
                "transportation": [
                    "地铁线路众多,是主要交通工具",
                    "磁悬浮列车连接浦东机场",
                    "轮渡体验黄浦江风光"
                ],
                "attractions": [
                    "外滩 - 万国建筑博览群",
                    "东方明珠塔 - 上海地标建筑",
                    "上海迪士尼乐园",
                    "豫园 - 江南古典园林",
                    "田子坊 - 创意艺术街区"
                ],
                "cuisine": [
                    "小笼包 - 南翔馒头店",
                    "生煎包",
                    "本帮菜 - 红烧肉、糖醋小排",
                    "上海菜饭、阳春面"
                ]
            },
            "杭州": {
                "best_time": "春季(3-5月)赏花,秋季(9-11月)观桂",
                "tips": [
                    "西湖环湖骑行约1-2小时",
                    "雷峰塔日落时分景色最美",
                    "夏季荷花盛开,值得一看",
                    "使用杭州通APP享受公交地铁优惠"
                ],
                "transportation": [
                    "公共自行车系统发达",
                    "地铁覆盖主要景区",
                    "西湖周边步行或骑行为佳"
                ],
                "attractions": [
                    "西湖 - 世界文化遗产",
                    "灵隐寺 - 江南著名古刹",
                    "宋城 - 大型文化主题公园",
                    "西溪湿地 - 都市中的天然湿地",
                    "千岛湖 - 天下第一秀水"
                ],
                "cuisine": [
                    "西湖醋鱼",
                    "东坡肉",
                    "龙井虾仁",
                    "叫花鸡",
                    "知味观小笼包"
                ]
            },
            "广州": {
                "best_time": "秋季(10-12月)气候最宜人",
                "tips": [
                    "尝试早茶文化,体验'一盅两件'",
                    "夏季炎热多雨,注意防暑防雨",
                    "使用羊城通乘坐公交地铁",
                    "珠江夜游推荐傍晚时段"
                ],
                "transportation": [
                    "地铁网络便捷",
                    "有轨电车串联珠江新城",
                    "水上巴士体验珠江风光"
                ],
                "attractions": [
                    "广州塔 - 小蛮腰地标",
                    "沙面岛 - 欧陆风情建筑群",
                    "陈家祠 - 岭南建筑艺术",
                    "长隆野生动物世界",
                    "白云山 - 羊城第一秀"
                ],
                "cuisine": [
                    "早茶 - 虾饺、肠粉、叉烧包",
                    "广式烧腊",
                    "白切鸡",
                    "艇仔粥",
                    "双皮奶"
                ]
            },
            "深圳": {
                "best_time": "全年气候温和,秋冬季最舒适",
                "tips": [
                    "世界之窗、欢乐谷建议预留一整天",
                    "海边景点注意防晒",
                    "关口通关高峰期避开",
                    "深圳通卡可刷地铁公交"
                ],
                "transportation": [
                    "地铁覆盖主要区域",
                    "共享单车普及率高",
                    "滴滴、出租车方便"
                ],
                "attractions": [
                    "世界之窗 - 微缩世界景观",
                    "欢乐谷 - 大型主题公园",
                    "大梅沙海滨公园",
                    "深圳湾公园 - 滨海休闲",
                    "OCT创意文化园"
                ],
                "cuisine": [
                    "潮汕牛肉火锅",
                    "客家菜",
                    "海鲜",
                    "港式茶餐厅",
                    "各地美食汇聚"
                ]
            },
            "成都": {
                "best_time": "春季(3-5月)和秋季(9-11月)最佳",
                "tips": [
                    "大熊猫基地早上去,熊猫更活跃",
                    "品尝正宗川菜,注意辣度选择",
                    "宽窄巷子、锦里晚上更热闹",
                    "成都地铁天府通卡很便利"
                ],
                "transportation": [
                    "地铁线路不断扩展",
                    "公交车覆盖全市",
                    "共享单车适合市区游览"
                ],
                "attractions": [
                    "大熊猫繁育研究基地",
                    "宽窄巷子 - 成都名片",
                    "锦里古街 - 三国文化",
                    "武侯祠 - 三国圣地",
                    "都江堰 - 世界水利文化遗产"
                ],
                "cuisine": [
                    "火锅 - 麻辣鲜香",
                    "串串香",
                    "担担面",
                    "夫妻肺片",
                    "龙抄手"
                ]
            },
            "西安": {
                "best_time": "春季(3-5月)和秋季(9-11月)",
                "tips": [
                    "兵马俑建议请讲解员",
                    "回民街品尝美食避开正餐高峰",
                    "城墙骑行约2-3小时",
                    "长安通卡乘公交地铁有优惠"
                ],
                "transportation": [
                    "地铁连接主要景点",
                    "城墙可租自行车游览",
                    "景区间可乘旅游专线"
                ],
                "attractions": [
                    "兵马俑 - 世界第八大奇迹",
                    "西安城墙 - 中国现存最完整古城墙",
                    "大雁塔 - 唐代建筑",
                    "华清宫 - 唐代皇家园林",
                    "回民街 - 美食文化街"
                ],
                "cuisine": [
                    "肉夹馍",
                    "羊肉泡馍",
                    "凉皮",
                    "biangbiang面",
                    "胡辣汤"
                ]
            },
            "昆明": {
                "best_time": "全年适宜,春季(3-5月)最佳,四季如春",
                "tips": [
                    "昆明紫外线强,注意防晒",
                    "早晚温差大,建议携带外套",
                    "石林景区较大,建议穿舒适的鞋",
                    "滇池最佳观赏时间为冬季,红嘴鸥成群",
                    "云南少数民族众多,尊重当地风俗习惯"
                ],
                "transportation": [
                    "地铁覆盖市区主要景点",
                    "公交车路线丰富,可办理公交卡",
                    "出租车起步价8元",
                    "共享单车适合市区短途出行",
                    "前往石林、九乡等景区可乘专线车"
                ],
                "attractions": [
                    "石林风景区 - 世界自然遗产,喀斯特地貌奇观",
                    "滇池 - 云南第一大淡水湖,观红嘴鸥",
                    "翠湖公园 - 市中心免费公园,冬季赏鸥胜地",
                    "云南民族村 - 26个民族文化展示",
                    "西山龙门 - 俯瞰滇池全景",
                    "金马碧鸡坊 - 昆明地标建筑",
                    "官渡古镇 - 千年历史古镇",
                    "世界园艺博览园 - 大型植物园"
                ],
                "cuisine": [
                    "过桥米线 - 云南特色名吃",
                    "汽锅鸡 - 传统滇菜",
                    "鲜花饼 - 云南特产",
                    "烧饵块 - 昆明传统早餐",
                    "野生菌火锅 - 季节性美食(雨季)",
                    "宣威火腿",
                    "豆花米线",
                    "凉米线"
                ]
            }
        }
        
        for city_name, city_data in tips_database.items():
            if city_name in location or location in city_name:
                recommendations["best_time"] = city_data["best_time"]
                recommendations["tips"] = city_data["tips"]
                recommendations["transportation"] = city_data["transportation"]
                recommendations["attractions"] = city_data["attractions"]
                recommendations["cuisine"] = city_data["cuisine"]
                break
        
        if not recommendations["tips"]:
            recommendations["tips"] = [
                "建议提前查询目的地天气预报",
                "了解当地交通状况和出行方式",
                "预订酒店时查看用户评价",
                "携带常用药品和个人用品",
                "保管好贵重物品和证件"
            ]
            recommendations["best_time"] = "建议根据当地气候选择合适的出行时间"
            recommendations["transportation"] = [
                "提前规划交通路线",
                "下载当地地图和交通APP",
                "考虑使用公共交通工具"
            ]
        
        return recommendations
    
    def format_recommendations_message(self, recommendations: Dict) -> str:
        """
        Format travel recommendations into a readable message
        
        Args:
            recommendations: Recommendations data dictionary
            
        Returns:
            Formatted recommendations message string
        """
        location = recommendations.get("location", "未知地点")
        message = f"🎯 {location} 旅游推荐\n\n"
        
        if recommendations.get("best_time"):
            message += f"⏰ 最佳旅游时间:\n  {recommendations['best_time']}\n\n"
        
        if recommendations.get("tips"):
            message += "💡 旅游小贴士:\n"
            for tip in recommendations["tips"]:
                message += f"  • {tip}\n"
            message += "\n"
        
        if recommendations.get("transportation"):
            message += "🚇 交通建议:\n"
            for trans in recommendations["transportation"]:
                message += f"  • {trans}\n"
            message += "\n"
        
        if recommendations.get("attractions"):
            message += "🏛️ 热门景点:\n"
            for attraction in recommendations["attractions"]:
                message += f"  • {attraction}\n"
            message += "\n"
        
        if recommendations.get("cuisine"):
            message += "🍜 特色美食:\n"
            for food in recommendations["cuisine"]:
                message += f"  • {food}\n"
        
        return message
    
    def get_destination_info(self, location: str) -> Dict:
        """
        Get comprehensive destination information including weather and recommendations
        
        Args:
            location: Location name
            
        Returns:
            Dictionary containing weather and recommendations
        """
        weather = self.get_weather(location)
        recommendations = self.get_travel_recommendations(location)
        
        return {
            "location": location,
            "weather": weather,
            "recommendations": recommendations,
            "weather_message": self.format_weather_message(weather),
            "recommendations_message": self.format_recommendations_message(recommendations)
        }
