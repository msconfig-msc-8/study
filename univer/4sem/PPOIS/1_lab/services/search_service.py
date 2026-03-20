# services/search_service.py

from typing import List
# Импортируем наш класс Property только для того, чтобы подсказывать типы (аннотации)
from models.property import Property 

class SearchService:
    """
    Сервис, отвечающий за поиск объектов недвижимости по заданным критериям.
    """

    @staticmethod
    def find_properties(properties: List[Property], max_price: float = None, min_area: float = None) -> List[Property]:
        """
        Метод ищет доступные объекты в списке properties по цене и площади.
        Если критерий (max_price или min_area) не передан, он не учитывается.
        """
        # Сюда мы будем складывать подходящие объекты
        found_properties: List[Property] = []

        # Перебираем каждую "коробку" (объект) в нашем списке
        for prop in properties:
            # Нам нужны только те квартиры, которые еще не проданы
            if not prop.is_available:
                continue # Пропускаем проданные и идем к следующей

            # Проверяем по цене (если клиент указал максимальную цену)
            if max_price is not None and prop.price > max_price:
                continue 

            # Проверяем по площади (если клиент указал минимальную площадь)
            if min_area is not None and prop.area < min_area:
                continue 

            # Если объект прошел все проверки выше, значит он нам подходит!
            found_properties.append(prop)

        # Возвращаем готовую стопочку (список)
        return found_properties