from json import JSONDecodeError

from models.agency import Agency
from models.agent import Agent
from models.client import Client
from models.market import Market
from models.property import Property
from services.deal_service import DealService
from services.search_service import SearchService
from services.valuation_service import ValuationService
from services.viewing_service import ViewingService
from storage.json_storage import (
    backup_data_file,
    has_saved_data,
    load_agency,
    save_agen
)


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


def load_or_create_agency() -> Agency:
    if has_saved_data():
        try:
            return load_agency()
        except (
            OSError,
            JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            backup_path = backup_data_file()
            print(
                "Не удалось загрузить data.json. "
                f"Поврежденный файл сохранен как {backup_path.name}. "
                f"Причина: {error}"
            )

    agency = setup_test_data()
    save_agency(agency)
    return agency


def get_next_id(items: list, id_attribute: str) -> int:
    if not items:
        return 1

    return max(getattr(item, id_attribute) for item in items) + 1


def read_required_text(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        raise ValueError("Значение не может быть пустым.")

    return value


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


def run_add_client(agency: Agency) -> None:
    client_id = get_next_id(agency.clients, "client_id")
    name = read_required_text("Введите имя клиента: ")
    budget = float(input("Введите бюджет клиента: "))

    client = Client(client_id, name, budget)
    agency.add_client(client)
    print(f"Клиент добавлен: {client}")


def run_add_agent(agency: Agency) -> None:
    agent_id = get_next_id(agency.agents, "agent_id")
    name = read_required_text("Введите имя агента: ")
    experience_years = int(input("Введите опыт агента в годах: "))

    agent = Agent(agent_id, name, experience_years)
    agency.add_agent(agent)
    print(f"Агент добавлен: {agent}")


def run_add_property(agency: Agency) -> None:
    property_id = get_next_id(agency.properties, "property_id")
    address = read_required_text("Введите адрес объекта: ")
    price = float(input("Введите цену объекта: "))
    area = float(input("Введите площадь объекта: "))

    property_obj = Property(property_id, address, price, area)
    agency.add_property(property_obj)
    print(f"Объект добавлен: ID {property_obj.property_id}: {property_obj}")


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

    property_obj = agency.get_property_by_id(property_id)
    agency.market.update_trend(new_multiplier)
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
    agency = load_or_create_agency()
    print("Текущее состояние загружено из data.json.")

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
        print("8. Добавить клиента")
        print("9. Добавить агента")
        print("10. Добавить объект недвижимости")
        print("0. Выход")
        print("=" * 40)

        choice = input("Выберите действие (введите цифру): ").strip()
        state_changed = False

        try:
            if choice == "1":
                print_properties(agency)
            elif choice == "2":
                run_search(agency)
            elif choice == "3":
                run_viewing(agency)
            elif choice == "4":
                run_valuation(agency)
                state_changed = True
            elif choice == "5":
                run_deal(agency)
                state_changed = True
            elif choice == "6":
                print_deals(agency)
            elif choice == "7":
                print_documents(agency)
            elif choice == "8":
                run_add_client(agency)
                state_changed = True
            elif choice == "9":
                run_add_agent(agency)
                state_changed = True
            elif choice == "10":
                run_add_property(agency)
                state_changed = True
            elif choice == "0":
                save_agency(agency)
                print("Завершение работы программы. До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите цифру из меню.")

            if state_changed:
                save_agency(agency)
                print("Данные сохранены в data.json.")
        except (ValueError, RuntimeError) as error:
            print(f"\nОшибка: {error}")


if __name__ == "__main__":
    main()
