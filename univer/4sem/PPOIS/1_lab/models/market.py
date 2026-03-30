# models/market.py


class Market:
    """
    Класс, представляющий рынок недвижимости.
    Хранит текущее состояние рынка через коэффициент тренда.
    """

    def __init__(self, name: str, trend_multiplier: float = 1.0):
        self.name = name
        if trend_multiplier <= 0:
            raise ValueError("Коэффициент рынка должен быть больше нуля!")
        self.trend_multiplier = trend_multiplier

    def update_trend(self, new_multiplier: float) -> None:
        """
        Метод для обновления рыночной ситуации.
        """
        if new_multiplier <= 0:
            raise ValueError("Новый коэффициент не может быть отрицательным!")
        self.trend_multiplier = new_multiplier

    def __str__(self) -> str:
        trend = "Стабилен"
        if self.trend_multiplier > 1.0:
            trend = "Растет"
        elif self.trend_multiplier < 1.0:
            trend = "Падает"
        return (
            f"Рынок '{self.name}' | Состояние: {trend} "
            f"(коэф. {self.trend_multiplier})"
        )
