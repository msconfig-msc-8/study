# models/agent.py

class Agent:
    """
    Класс, представляющий агента по недвижимости.
    """
    
    def __init__(self, agent_id: int, name: str, experience_years: int):
        self.agent_id = agent_id
        self.name = name
        self.experience_years = experience_years
        
        # Список клиентов, которых ведет этот агент (изначально пуст)
        # Аннотируем как list, но пока не привязываем жестко класс Client, 
        # чтобы избежать циклического импорта на раннем этапе
        self.clients: list = [] 

    def assign_client(self, client) -> None:
        """
        Метод для прикрепления клиента к агенту.
        """
        self.clients.append(client)

    def __str__(self) -> str:
        return f"Агент: {self.name} (Опыт: {self.experience_years} лет)"