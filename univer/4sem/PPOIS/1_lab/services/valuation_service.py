# services/valuation_service.py

from models.property import Property

class ValuationService:
    """
    Сервис для оценки рыночной стоимости объекта недвижимости.
    """

    @staticmethod
    def estimate_market_value(property_obj: Property, market_trend_multiplier: float = 1.0) -> float:
        """
        Оценивает стоимость объекта с учетом рыночного коэффициента.
        Например, если цены на рынке выросли на 15%, передаем market_trend_multiplier = 1.15.
        """
        if market_trend_multiplier <= 0:
            raise ValueError("Рыночный коэффициент должен быть положительным числом!")
            
        # Умножаем изначальную цену на рыночный коэффициент
        estimated_value = property_obj.price * market_trend_multiplier
        
        # Функция round() округляет число до 2 знаков после запятой (копейки/центы)
        return round(estimated_value, 2)