class CaloriesService:
    """Сервис расчёта каллорий пользователя"""

    @staticmethod
    def calc_daily_calories(weight, height, age, activity_minutes):

        base = 10 * weight + 6.25 * height - 5 * age    # Согласно тз
        activity_bonus = (activity_minutes // 30) * 200 # Бонус активности

        return int(base + activity_bonus)