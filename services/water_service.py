class WaterService:

    @staticmethod
    def calc_water_goal(weight, activity_min, temp):

        base = weight * 30  # Базово 30 мл/кг
        activity_bonus = (activity_min // 30) * 500     # Ещё по 500 мл за каждые 30 минут активности

        temp_bonus = 0
        if temp > 25:
            extra_temp = temp - 25
            temp_bonus = 500 + (extra_temp * 100)   # За каждый градус, начиная с 25, я даю дополнительные 100 мл воды

        return base + activity_bonus + temp_bonus