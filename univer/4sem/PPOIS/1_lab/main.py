# main.py

from models.agency import Agency
from models.agent import Agent
from models.client import Client
from models.property import Property
from services.search_service import SearchService
from services.viewing_service import ViewingService
from services.valuation_service import ValuationService
from services.deal_service import DealService

def setup_test_data() -> Agency:
    """
    Создает агентство и наполняет его стартовыми (тестовыми) данными.
    """
    agency = Agency("Мечта Риелтора")
    
    # Добавляем агентов
    agent1 = Agent(1, "Иван Иванов", 5)
    agency.add_agent(agent1)
    
    # Добавляем клиентов
    client1 = Client(1, "Петр Петров", 150000.0) # Богатый клиент
    client2 = Client(2, "Анна Смирнова", 50000.0) # Клиент со скромным бюджетом
    agency.add_client(client1)
    agency.add_client(client2)
    
    # Добавляем недвижимость
    prop1 = Property(1, "ул. Пушкина, д. Колотушкина, кв. 5", 45000.0, 40.5)
    prop2 = Property(2, "Невский проспект, д. 1, пентхаус", 120000.0, 120.0)
    agency.add_property(prop1)
    agency.add_property(prop2)
    
    return agency

def main():
    """
    Главная функция программы, запускающая интерфейс командной строки (CLI).
    """
    print("Добро пожаловать в систему управления агентством недвижимости!")
    agency = setup_test_data()
    
    # Бесконечный цикл, который держит меню открытым, пока мы сами не выйдем
    while True:
        print("\n" + "="*40)
        print("Главное меню:")
        print("1. Показать все объекты")
        print("2. Поиск недвижимости (до 50 000$)")
        print("3. Организовать просмотр (Агент 1, Клиент 1, Объект 1)")
        print("4. Оценить стоимость Объекта 1 (рост рынка на 10%)")
        print("5. Провести сделку (Клиент 1 покупает Объект 2)")
        print("6. Показать все документы (сделки)")
        print("0. Выход")
        print("="*40)
        
        choice = input("Выберите действие (введите цифру): ")
        
        # Обработка исключений для безопасной работы программы
        try:
            if choice == "1":
                for p in agency.properties:
                    print(p)
                    
            elif choice == "2":
                print("Ищем объекты дешевле 50 000$...")
                found = SearchService.find_properties(agency.properties, max_price=50000.0)
                for f in found:
                    print(f)
                    
            elif choice == "3":
                # Берем первых из списка для демонстрации
                client = agency.clients[0]
                agent = agency.agents[0]
                prop = agency.properties[0]
                report = ViewingService.arrange_viewing(client, agent, prop)
                print(report)
                
            elif choice == "4":
                prop = agency.properties[0]
                new_price = ValuationService.estimate_market_value(prop, 1.10)
                print(f"Старая цена: {prop.price}$. Новая рыночная цена: {new_price}$")
                
            elif choice == "5":
                # Петр (бюджет 150к) покупает Пентхаус (цена 120к)
                client = agency.clients[0]
                agent = agency.agents[0]
                prop = agency.properties[1] 
                
                print(f"Начинаем сделку: {client.name} покупает '{prop.address}'...")
                # Проводим сделку и сохраняем документ в агентство
                doc = DealService.make_deal(len(agency.documents) + 1, client, agent, prop)
                agency.add_document(doc)
                print("Сделка успешно завершена!")
                print(doc)
                
            elif choice == "6":
                if not agency.documents:
                    print("Сделок пока не было.")
                for d in agency.documents:
                    print(d)
                    
            elif choice == "0":
                print("Завершение работы программы. До свидания!")
                break # Выход из бесконечного цикла
                
            else:
                print("Неверный ввод. Пожалуйста, выберите цифру из меню.")
                
        except (ValueError, RuntimeError) as e:
            # Сюда мы попадем, если попытаемся купить проданную квартиру
            # или если не хватит денег! Программа не упадет, а просто выдаст этот текст.
            print(f"\n❌ ПРОИЗОШЛА ОШИБКА: {e}")

# Эта конструкция гарантирует, что main() запустится только если мы напрямую запустим этот файл
if __name__ == "__main__":
    main()