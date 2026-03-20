# models/property.py

class Property:
    """
    Класс, представляющий объект недвижимости (квартира, дом, участок).
    """
    
    def __init__(self, property_id: int, address: str, price: float, area: float):
        self.property_id = property_id
        self.address = address
        
        # Снова используем механизм исключений для защиты от "дурака"
        if price <= 0:
            raise ValueError("Цена объекта недвижимости должна быть больше нуля!")
        if area <= 0:
            raise ValueError("Площадь не может быть отрицательной или нулевой!")
            
        self.price = price
        self.area = area
        
        # По умолчанию, когда мы добавляем объект в базу, он доступен для продажи
        self.is_available: bool = True  

    def sell(self) -> None:
        """
        Метод, который помечает объект как проданный.
        """
        # Если объект уже продан, выбрасываем ошибку состояния
        if not self.is_available:
            raise RuntimeError(f"Ошибка: Объект по адресу {self.address} уже продан!")
        
        self.is_available = False

    def __str__(self) -> str:
        # Быстрая проверка: если True - пишем "Доступен", если False - "Продан"
        status = "Доступен" if self.is_available else "Продан"
        return f"Объект [{status}]: {self.address} | Площадь: {self.area} кв.м | Цена: {self.price}$"