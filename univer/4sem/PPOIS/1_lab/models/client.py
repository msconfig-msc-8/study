# models/client.py

class Client:
    """
    Класс, представляющий клиента агентства недвижимости.
    """
    
    def __init__(self, client_id: int, name: str, budget: float):
        # Аннотации типов (int, str, float) подсказывают, какие данные мы ждем
        self.client_id = client_id
        self.name = name
        
        # Мы можем сделать небольшую проверку прямо при создании объекта
        if budget < 0:
            # Выбрасываем встроенное исключение, если бюджет отрицательный
            raise ValueError("Бюджет клиента не может быть отрицательным!")
        
        self.budget = budget

    def __str__(self) -> str:
        # Этот магический метод делает так, чтобы при print(client) 
        # выводился красивый текст, а не непонятный адрес в памяти
        return f"Клиент: {self.name} (Бюджет: {self.budget}$)"