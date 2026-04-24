# 🏠 Разбор лабы — Агентство недвижимости

## Общая идея: что вообще делает программа?

Программа моделирует работу **агентства недвижимости**. Представь реальное агентство:
- Есть **агентство** (контора)
- В нём работают **агенты** (риелторы)
- К ним приходят **клиенты** (покупатели с деньгами)
- Агентство продаёт **объекты недвижимости** (квартиры)
- Когда клиент покупает квартиру — оформляется **документ** и заключается **сделка**
- Цена квартиры зависит от **рынка** (рынок растёт → цена выше)

Всё это написано через **классы** (ООП = объектно-ориентированное программирование).

---

## Шаг 1: Что такое класс — на пальцах

Класс — это **чертёж/шаблон** для создания объектов. Например:

```python
class Client:
    def __init__(self, client_id, name, budget):
        self.client_id = client_id   # номер клиента
        self.name = name             # имя
        self.budget = budget         # сколько денег
```

- `class Client` — мы описываем шаблон «Клиент»
- `__init__` — это **конструктор** (вызывается при создании клиента)
- `self` — это **ссылка на самого себя** (на создаваемый объект)
- `self.name = name` — сохраняем данные **внутри** объекта

Когда пишем:
```python
petya = Client(1, "Петр Петров", 150000.0)
```
Создаётся конкретный клиент Пётр с бюджетом 150000$.

---

## Шаг 2: Все модели (файлы в `models/`)

Модели — это классы, которые описывают **данные** (сущности). Вот все 7 штук:

### 📄 `client.py` — Клиент
```python
class Client:
    def __init__(self, client_id, name, budget):
        self.client_id = client_id
        self.name = name
        if budget < 0:                    # ← проверка: бюджет не может быть отрицательным
            raise ValueError("...")
        self.budget = budget
```
> **Проще говоря**: клиент = имя + деньги. Если попытаться создать клиента с отрицательным бюджетом — будет ошибка.

---

### 🧑‍💼 `agent.py` — Агент (риелтор)
```python
class Agent:
    def __init__(self, agent_id, name, experience_years):
        self.agent_id = agent_id
        self.name = name
        self.experience_years = experience_years
        self.clients = []              # список клиентов, закреплённых за агентом

    def assign_client(self, client):   # закрепить клиента за агентом
        self.clients.append(client)
```
> **Проще говоря**: агент = имя + опыт + список его клиентов.

---

### 🏡 `property.py` — Объект недвижимости (квартира)
```python
class Property:
    def __init__(self, property_id, address, price, area):
        self.property_id = property_id
        self.address = address
        self.price = price            # цена
        self.area = area              # площадь в кв.м
        self.is_available = True      # доступна ли для продажи

    def sell(self):                   # продать квартиру
        if not self.is_available:
            raise RuntimeError("Уже продана!")
        self.is_available = False     # помечаем как «продана»
```
> **Проще говоря**: квартира = адрес + цена + площадь + статус (продана или нет).
> Метод `sell()` переводит квартиру в статус «продана». Нельзя продать дважды.

---

### 📈 `market.py` — Рынок
```python
class Market:
    def __init__(self, name, trend_multiplier=1.0):
        self.name = name
        self.trend_multiplier = trend_multiplier   # коэффициент рынка

    def update_trend(self, new_multiplier):
        self.trend_multiplier = new_multiplier
```
> **Проще говоря**: рынок = коэффициент. Если коэфф. = 1.0 → цены стабильны. Если 1.2 → цены выросли на 20%. Если 0.8 → упали на 20%.

---

### 📃 `document.py` — Документ (договор)
```python
class Document:
    def __init__(self, document_id, client, agent, property_obj):
        self.document_id = document_id
        self.client = client
        self.agent = agent
        self.property_obj = property_obj
        self.created_at = datetime.datetime.now()   # дата создания
        self.is_signed = False                      # подписан или нет

    def sign(self):                  # подписать документ
        if self.is_signed:
            raise RuntimeError("Уже подписан!")
        self.is_signed = True
```
> **Проще говоря**: документ хранит кто покупает, кто продаёт, какую квартиру, и подписан ли.

---

### 🤝 `deal.py` — Сделка
```python
class Deal:
    def __init__(self, deal_id, property_obj, client, agent, final_price):
        self.deal_id = deal_id
        self.property_obj = property_obj
        self.client = client
        self.agent = agent
        self.final_price = final_price
        self.document = None              # документ (привяжется позже)
        self.is_completed = False         # завершена ли сделка

    def complete(self, document):         # завершить сделку
        self.document = document
        self.is_completed = True
```
> **Проще говоря**: сделка = кто + что + за сколько + документ. Метод `complete()` закрывает сделку.

---

### 🏢 `agency.py` — Агентство (главный «контейнер»)
```python
class Agency:
    def __init__(self, name, market):
        self.name = name
        self.market = market
        self.agents = []          # все агенты
        self.clients = []         # все клиенты
        self.properties = []      # все квартиры
        self.documents = []       # все документы
        self.deals = []           # все сделки
```
> **Проще говоря**: агентство — это «коробка», которая хранит ВСЁ: агентов, клиентов, квартиры, документы и сделки. Плюс методы для добавления и поиска по `id`.

---

## Шаг 3: Сервисы (файлы в `services/`)

Сервисы — это классы, которые описывают **логику/действия**. Модели хранят данные, а сервисы — работают с ними.

### 🔍 `SearchService` — Поиск квартир
```python
@staticmethod
def find_properties(properties, max_price=None, min_area=None):
    # Проходит по всем квартирам и отбирает подходящие:
    # - только доступные (не проданные)
    # - цена не больше max_price
    # - площадь не меньше min_area
```
> Пример: «Найди мне квартиры до 100000$ и от 50 кв.м»

---

### 👁️ `ViewingService` — Организация просмотра
```python
@staticmethod
def arrange_viewing(client, agent, property_obj):
    # Проверяет, доступна ли квартира
    # Формирует строку-отчёт: «Агент Иванов показывает квартиру клиенту Петрову»
```

---

### 💰 `ValuationService` — Оценка стоимости
```python
@staticmethod
def estimate_market_value(property_obj, market):
    return property_obj.price * market.trend_multiplier
    # Цена × коэффициент рынка = рыночная стоимость
```
> Пример: квартира стоит 100000$, рынок растёт (коэфф. 1.15) → рыночная цена = 115000$

---

### 📝 `DocumentService` — Работа с документами
```python
@staticmethod
def draft_document(doc_id, client, agent, property_obj):
    return Document(doc_id, client, agent, property_obj)   # создать черновик

@staticmethod
def sign_document(document):
    document.sign()    # подписать
```

---

### 🏦 `DealService` — Проведение сделки (самый важный)
```python
@staticmethod
def make_deal(deal_id, client, agent, property_obj):
    # 1. Проверяет: квартира ещё не продана?
    # 2. Проверяет: хватает ли клиенту денег?
    # 3. Списывает деньги у клиента:    client.budget -= property_obj.price
    # 4. Помечает квартиру как проданную: property_obj.sell()
    # 5. Создаёт сделку (Deal)
    # 6. Создаёт документ (Document) и подписывает его
    # 7. Завершает сделку:               deal.complete(document)
    # 8. Возвращает готовую сделку
```
> Это самая сложная часть — объединяет всё остальное.

---

## Шаг 4: `main.py` — точка входа

Вот что происходит при запуске `python main.py`:

```
1. Вызывается функция main()
2. Вызывается setup_test_data() — создаются тестовые данные:
   - Агентство "Мечта Риелтора"
   - 2 агента (Иван, Мария)
   - 2 клиента (Пётр с 150000$, Анна с 50000$)
   - 3 квартиры (разные адреса, цены, площади)
3. Запускается бесконечный цикл while True с меню:
   - Пользователь вводит цифру
   - Программа выполняет действие
   - Повторяет, пока не выберут "0" (выход)
```

### Схема вызова при сделке (пункт 5 меню):
```
Пользователь выбирает "5"
   └── run_deal(agency)
        ├── Выводит клиентов, агентов, квартиры
        ├── Пользователь вводит id
        ├── agency.get_client_by_id() → находит клиента
        ├── agency.get_agent_by_id()  → находит агента
        ├── agency.get_property_by_id() → находит квартиру
        └── DealService.make_deal()
             ├── Проверяет бюджет
             ├── Списывает деньги
             ├── property_obj.sell()
             ├── DocumentService.draft_document() → создаёт документ
             ├── DocumentService.sign_document()  → подписывает
             └── deal.complete(document) → завершает сделку
```

---

## Шаг 5: Что такое `@staticmethod`?

В сервисах используется `@staticmethod` — это метод, который **не привязан к конкретному объекту**. Ему не нужен `self`. Он просто получает данные на вход и возвращает результат.

```python
class ValuationService:
    @staticmethod
    def estimate_market_value(property_obj, market):
        return property_obj.price * market.trend_multiplier
```

Вызывается так: `ValuationService.estimate_market_value(квартира, рынок)` — не нужно создавать объект `ValuationService()`.

---

## Шаг 6: Обработка ошибок

В коде используются два типа ошибок:
- `ValueError` — неправильные входные данные (отрицательный бюджет, нулевая цена)
- `RuntimeError` — логическая ошибка (продажа уже проданной квартиры)

В `main.py` все ошибки ловятся через `try/except`:
```python
try:
    # выполняем действие
except (ValueError, RuntimeError) as error:
    print(f"Ошибка: {error}")
```
Программа **не падает** при ошибке, а просто выводит сообщение и продолжает работать.

---

## Итого: архитектура одной картинкой

```
main.py (CLI — интерфейс)
   │
   ├── models/ (ДАННЫЕ — «что хранить?»)
   │   ├── Agency    ← хранит всё
   │   ├── Agent     ← имя + опыт
   │   ├── Client    ← имя + бюджет
   │   ├── Property  ← адрес + цена + площадь
   │   ├── Market    ← коэффициент рынка
   │   ├── Document  ← договор
   │   └── Deal      ← сделка
   │
   └── services/ (ЛОГИКА — «что делать?»)
       ├── SearchService     ← поиск квартир
       ├── ViewingService    ← организация просмотра
       ├── ValuationService  ← оценка стоимости
       ├── DocumentService   ← создание/подписание документов
       └── DealService       ← проведение сделки
```

**Модели** = существительные (Клиент, Квартира, Сделка)
**Сервисы** = глаголы (Искать, Оценивать, Продавать)
**main.py** = связывает всё через меню

---

## Шаг 7: Как работают тесты

Тесты проверяют, что код работает правильно. Используется библиотека `unittest`.

### Пример: тест клиента (`tests/test_client.py`)
```python
import unittest
from models.client import Client

class TestClient(unittest.TestCase):

    def test_client_creation_success(self):
        client = Client(1, "Иван", 50000.0)        # создаём клиента
        self.assertEqual(client.name, "Иван")       # имя = "Иван"? ✅
        self.assertEqual(client.budget, 50000.0)     # бюджет = 50000? ✅

    def test_client_negative_budget(self):
        with self.assertRaises(ValueError):          # ожидаем ошибку ValueError
            Client(2, "Должник", -1000.0)            # отрицательный бюджет → ошибка! ✅
```

**Что тут происходит:**
- `assertEqual(a, b)` — проверяет, что `a == b`
- `assertTrue(x)` — проверяет, что `x` это `True`
- `assertFalse(x)` — проверяет, что `x` это `False`
- `assertRaises(ValueError)` — проверяет, что код **выбрасывает** ошибку
- `setUp(self)` — метод, который вызывается **перед каждым** тестом (подготавливает данные)

### Пример: тест квартиры (`tests/test_property.py`)
```python
class TestProperty(unittest.TestCase):
    def setUp(self):
        self.prop = Property(1, "ул. Тестовая, 1", 100000.0, 50.0)  # создаём квартиру ПЕРЕД каждым тестом

    def test_property_initial_state(self):
        self.assertTrue(self.prop.is_available)    # новая квартира доступна? ✅

    def test_property_sell_success(self):
        self.prop.sell()                            # продаём
        self.assertFalse(self.prop.is_available)    # теперь недоступна? ✅

    def test_property_sell_already_sold(self):
        self.prop.sell()                            # продали
        with self.assertRaises(RuntimeError):       # продаём второй раз → ошибка! ✅
            self.prop.sell()
```

### Пример: тест сделки (`test_services/test_deal_service.py`)
```python
class TestDealService(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(1, "Агент Смит", 10)
        self.rich_client = Client(1, "Богач", 100000.0)    # у этого денег хватит
        self.poor_client = Client(2, "Бедняк", 10000.0)    # а у этого нет
        self.property = Property(1, "Вилла", 50000.0, 100.0)

    def test_make_deal_success(self):
        deal = DealService.make_deal(1, self.rich_client, self.agent, self.property)
        self.assertEqual(self.rich_client.budget, 50000.0)  # 100000 - 50000 = 50000 ✅
        self.assertFalse(self.property.is_available)         # квартира продана ✅
        self.assertTrue(deal.is_completed)                   # сделка завершена ✅
        self.assertTrue(deal.document.is_signed)             # документ подписан ✅

    def test_make_deal_not_enough_money(self):
        with self.assertRaises(ValueError):                  # у бедняка 10000, а квартира 50000
            DealService.make_deal(2, self.poor_client, self.agent, self.property)  # → ошибка! ✅

    def test_make_deal_already_sold(self):
        DealService.make_deal(3, self.rich_client, self.agent, self.property)  # продали
        with self.assertRaises(RuntimeError):                # пытаемся продать снова
            DealService.make_deal(4, self.poor_client, self.agent, self.property)  # → ошибка! ✅
```

### Результаты тестов (все 20 прошли ✅):
```
Ran 20 tests in 0.001s — OK
```

---

## Частые вопросы на защите

| Вопрос | Ответ |
|--------|-------|
| **Что такое ООП?** | Программирование через классы и объекты. Данные и методы объединены в одном месте |
| **Что такое класс?** | Шаблон/чертёж для создания объектов |
| **Что такое объект?** | Конкретный экземпляр класса, созданный через `ClassName(...)` |
| **Что такое `self`?** | Ссылка объекта на самого себя. Через `self.name` мы обращаемся к полям объекта |
| **Что такое `__init__`?** | Конструктор — метод, который автоматически вызывается при создании объекта |
| **Что такое `__str__`?** | Метод, который определяет, как объект выводится через `print()` |
| **Что такое `@staticmethod`?** | Метод класса, которому не нужен `self`. Вызывается через `ClassName.method()` |
| **Зачем разделять models и services?** | Разделение данных и логики. Модели хранят **что**, сервисы описывают **что делать** |
| **Что такое `raise`?** | Выбрасывает ошибку (исключение). Программа останавливается, если не поймать через `try/except` |
| **Что делает `try/except`?** | «Попробуй выполнить, а если ошибка — не падай, а обработай» |
| **Зачем нужен `setUp` в тестах?** | Подготовка тестовых данных перед **каждым** тестом, чтобы тесты не влияли друг на друга |
