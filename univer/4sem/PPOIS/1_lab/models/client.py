# models/client.py


class Client:
    """
    Класс, представляющий клиента агентства недвижимости.
    """

    def __init__(self, client_id: int, name: str, budget: float):
        self.client_id = client_id
        self.name = name

        if budget < 0:
            raise ValueError("Бюджет клиента не может быть отрицательным!")

        self.budget = budget

    def __str__(self) -> str:
        return f"Клиент: {self.name} (Бюджет: {self.budget}$)"
