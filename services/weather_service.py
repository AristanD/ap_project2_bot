import aiohttp
from config import config


class WeatherService:
    """Сервис для получения инфо о текущей температуре через Open Weather Map (взята из предыдущего задания)"""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    async def get_temp(city: str) -> float:
        """Получение текущей температуры в городе"""
        params = {
            "q": city,
            "appid": config.OWM_API_KEY,
            "units": "metric"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(WeatherService.BASE_URL, params=params) as resp:

                if resp.status != 200:
                    return 20   # Если получить не удалось, возвращаю такую температуру, чтобы не было никаких бонусов пользователю
                
                data = await resp.json()

                return data["main"]["temp"]