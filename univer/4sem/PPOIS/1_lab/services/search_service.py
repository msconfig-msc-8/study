from typing import Optional

from models.property import Property


class SearchService:
    """
    Сервис, отвечающий за поиск объектов недвижимости по заданным критериям.
    """

    @staticmethod
    def find_properties(
        properties: list[Property],
        max_price: Optional[float] = None,
        min_area: Optional[float] = None,
    ) -> list[Property]:
        """
        Метод ищет доступные объекты по цене и площади.
        """
        found_properties: list[Property] = []

        for prop in properties:
            if not prop.is_available:
                continue

            if max_price is not None and prop.price > max_price:
                continue

            if min_area is not None and prop.area < min_area:
                continue

            found_properties.append(prop)

        return found_properties
