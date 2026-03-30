# models/property.py


class Property:
    """
    Класс, представляющий объект недвижимости.
    """

    def __init__(
        self,
        property_id: int,
        address: str,
        price: float,
        area: float,
    ):
        self.property_id = property_id
        self.address = address

        if price <= 0:
            raise ValueError(
                "Цена объекта недвижимости должна быть больше нуля!"
            )
        if area <= 0:
            raise ValueError(
                "Площадь не может быть отрицательной или нулевой!"
            )

        self.price = price
        self.area = area
        self.is_available: bool = True

    def sell(self) -> None:
        """
        Метод, который помечает объект как проданный.
        """
        if not self.is_available:
            raise RuntimeError(
                f"Ошибка: Объект по адресу {self.address} уже продан!"
            )

        self.is_available = False

    def __str__(self) -> str:
        status = "Доступен" if self.is_available else "Продан"
        return (
            f"Объект [{status}]: {self.address} | "
            f"Площадь: {self.area} кв.м | Цена: {self.price}$"
        )
