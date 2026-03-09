class WorkoutService:
    """Расчёт нормы по сжиганию каллорий"""

    CALORIES_PER_MINUTE = {
        "running": 10,
        "cycling": 8,
        "swimming": 9,
        "walking": 4,
        "gym": 6
    }   # Разные виды активности - разное число калорий в минуту

    WATER_PER_30_MIN = 200

    @staticmethod
    def calc_calories(workout_type, minutes):
        """Расчёт калорий"""
        
        calories_rate = WorkoutService.CALORIES_PER_MINUTE.get(workout_type, 4)     # Если пользователь не указал вид своей активности, считаем, что он просто гулял

        return calories_rate * minutes
    

    @staticmethod
    def additional_water(minutes):
        """Расчёт дополнительной воды с учётом активности"""
        return (minutes // 30) * WorkoutService.WATER_PER_30_MIN    # Доп. вода за 30 минут активности