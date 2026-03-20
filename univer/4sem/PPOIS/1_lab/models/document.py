# models/document.py

import datetime

class Document:
    """
    Класс, представляющий документ (договор купли-продажи).
    """
    
    def __init__(self, document_id: int, client, agent, property_obj):
        self.document_id = document_id
        self.client = client
        self.agent = agent
        self.property_obj = property_obj
        
        # Автоматически фиксируем дату и время создания документа
        self.created_at = datetime.datetime.now()
        self.is_signed: bool = False  # Документ изначально не подписан

    def sign(self) -> None:
        """
        Метод для подписания документа.
        """
        if self.is_signed:
            # Используем исключения, как того требует задание [cite: 18]
            raise RuntimeError(f"Документ №{self.document_id} уже подписан!")
        
        self.is_signed = True

    def __str__(self) -> str:
        status = "Подписан" if self.is_signed else "Черновик"
        # Форматируем дату, чтобы она выглядела красиво (День-Месяц-Год)
        date_str = self.created_at.strftime("%d-%m-%Y")
        return (f"Документ №{self.document_id} [{status}] от {date_str} | "
                f"Клиент: {self.client.name} | Агент: {self.agent.name}")