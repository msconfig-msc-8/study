from models.market import Market
from models.property import Property


class ValuationService:
    """
    Сервис для оценки рыночной стоимости объекта недвижимости.
    """

    @staticmethod
    def estimate_market_value(property_obj: Property, market: Market) -> float:
        """
        Оценивает стоимость объекта с учетом состояния рынка недвижимости.
        """
        estimated_value = property_obj.price * market.trend_multiplier
        return round(estimated_value, 2)
