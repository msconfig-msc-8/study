from models.agency import Agency
from models.agent import Agent
from models.client import Client
from models.market import Market
from models.property import Property
from services.deal_service import DealService
from services.search_service import SearchService
from services.valuation_service import ValuationService
from services.viewing_service import ViewingService


def setup_test_data() -> Agency:
    """
    Создает агентство и наполняет его стартовыми данными.
    """
    market = Market("Минск", 1.0)
    agency = Agency("Мечта Риелтора", market)

    agency.add_agent(Agent(1, "Иван Иванов", 5))
    agency.add_agent(Agent(2, "Мария Орлова", 8))

    agency.add_client(Client(1, "Петр Петров", 150000.0))
    agency.add_client(Client(2, "Анна Смирнова", 50000.0))

    agency.add_property(
        Property(1, "ул. Пушкина, д. Колотушкина, кв. 5", 45000.0, 40.5)
    )
    agency.add_property(
        Property(2, "Невский проспект, д. 1, пентхаус", 120000.0, 120.0)
    )
    agency.add_property(
        Property(3, "ул. Садовая, д. 10, кв. 14", 65000.0, 62.0)
    )

    return agency


def print_agents(agency: Agency) -> None:
    for agent in agency.agents:
        print(agent)


def print_clients(agency: Agency) -> None:
    for client in agency.clients:
        print(
            f"Клиент #{client.client_id}: {client.name} | "
            f"Бюджет: {client.budget}$"
        )


def print_properties(agency: Agency) -> None:
    for property_obj in agency.properties:
        print(f"ID {property_obj.property_id}: {property_obj}")


def print_deals(agency: Agency) -> None:
    if not agency.deals:
        print("Сделок пока не было.")
        return

    for deal in agency.deals:
        print(deal)


def print_documents(agency: Agency) -> None:
    if not agency.documents:
        print("Документов пока нет.")
        return

    for document in agency.documents:
        print(document)


def run_search(agency: Agency) -> None:
    max_price_input = input(
        "Введите максимальную цену (Enter, чтобы пропустить): "
    ).strip()
    min_area_input = input(
        "Введите минимальную площадь (Enter, чтобы пропустить): "
    ).strip()

    max_price = float(max_price_input) if max_price_input else None
    min_area = float(min_area_input) if min_area_input else None

    found = SearchService.find_properties(
        agency.properties,
        max_price=max_price,
        min_area=min_area,
    )
    if not found:
        print("Подходящих объектов не найдено.")
        return

    for property_obj in found:
        print(f"ID {property_obj.property_id}: {property_obj}")


def run_viewing(agency: Agency) -> None:
    print_clients(agency)
    client_id = int(input("Введите id клиента: "))
    print_agents(agency)
    agent_id = int(input("Введите id агента: "))
    print_properties(agency)
    property_id = int(input("Введите id объекта: "))

    client = agency.get_client_by_id(client_id)
    agent = agency.get_agent_by_id(agent_id)
    property_obj = agency.get_property_by_id(property_id)

    report = ViewingService.arrange_viewing(client, agent, property_obj)
    print(report)


def run_valuation(agency: Agency) -> None:
    print_properties(agency)
    property_id = int(input("Введите id объекта для оценки: "))
    new_multiplier = float(
        input("Введите коэффициент рынка (например 1.10): ")
    )

    agency.market.update_trend(new_multiplier)
    property_obj = agency.get_property_by_id(property_id)
    new_price = ValuationService.estimate_market_value(
        property_obj,
        agency.market,
    )

    print(f"Рынок: {agency.market}")
    print(f"Исходная цена: {property_obj.price}$")
    print(f"Оцененная рыночная цена: {new_price}$")


def run_deal(agency: Agency) -> None:
    print_clients(agency)
    client_id = int(input("Введите id клиента-покупателя: "))
    print_agents(agency)
    agent_id = int(input("Введите id агента: "))
    print_properties(agency)
    property_id = int(input("Введите id объекта для покупки: "))

    client = agency.get_client_by_id(client_id)
    agent = agency.get_agent_by_id(agent_id)
    property_obj = agency.get_property_by_id(property_id)

    deal = DealService.make_deal(
        len(agency.deals) + 1,
        client,
        agent,
        property_obj,
    )
    agency.add_deal(deal)

    if deal.document is not None:
        agency.add_document(deal.document)

    print("Сделка успешно завершена.")
    print(deal)
    if deal.document is not None:
        print(deal.document)


def main() -> None:
    """
    Главная функция программы, запускающая интерфейс командной строки.
    """
    print("Добро пожаловать в систему управления агентством недвижимости!")
    agency = setup_test_data()

    while True:
        print("\n" + "=" * 40)
        print("Главное меню:")
        print("1. Показать все объекты")
        print("2. Поиск недвижимости")
        print("3. Организовать просмотр")
        print("4. Оценить рыночную стоимость")
        print("5. Провести сделку")
        print("6. Показать все сделки")
        print("7. Показать все документы")
        print("0. Выход")
        print("=" * 40)

        choice = input("Выберите действие (введите цифру): ").strip()

        try:
            if choice == "1":
                print_properties(agency)
            elif choice == "2":
                run_search(agency)
            elif choice == "3":
                run_viewing(agency)
            elif choice == "4":
                run_valuation(agency)
            elif choice == "5":
                run_deal(agency)
            elif choice == "6":
                print_deals(agency)
            elif choice == "7":
                print_documents(agency)
            elif choice == "0":
                print("Завершение работы программы. До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите цифру из меню.")
        except (ValueError, RuntimeError) as error:
            print(f"\nОшибка: {error}")


if __name__ == "__main__":
    main()
