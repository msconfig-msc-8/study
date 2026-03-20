# models/agency.py

class Agency:
    """
    Класс, представляющий само агентство недвижимости.
    Хранит списки агентов, клиентов и объектов.
    """
    
    def __init__(self, name: str):
        self.name = name
        # Базовые конструкции языка Python: списки для хранения данных [cite: 11]
        self.agents: list = []
        self.clients: list = []
        self.properties: list = []
        self.documents: list = []

    def add_agent(self, agent) -> None:
        self.agents.append(agent)

    def add_client(self, client) -> None:
        self.clients.append(client)

    def add_property(self, property_obj) -> None:
        self.properties.append(property_obj)

    def add_document(self, document) -> None:
        self.documents.append(document)

    def __str__(self) -> str:
        return (f"Агентство '{self.name}' | Агентов: {len(self.agents)} | "
                f"Клиентов: {len(self.clients)} | Объектов: {len(self.properties)}")