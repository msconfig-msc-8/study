# 🧪 Описание всех тестов проекта

> Всего в проекте **43 теста** в **13 файлах**, разделённых на две группы:
> - `tests/` — тесты моделей (35 тестов, 8 файлов)
> - `test_services/` — тесты сервисов (8 тестов, 5 файлов)

Все тесты написаны с использованием стандартной библиотеки `unittest`.

---

## Часть 1: Тесты моделей (`tests/`)

---

### 📄 `tests/test_client.py` — Тесты клиента (2 теста)

| № | Тест | Что проверяет |
|---|------|---------------|
| 1 | `test_client_creation_success` | Успешное создание клиента с корректными данными |
| 2 | `test_client_negative_budget` | Ошибка при создании клиента с отрицательным бюджетом |

#### `test_client_creation_success`
```python
def test_client_creation_success(self):
    client = Client(1, "Иван", 50000.0)
    self.assertEqual(client.name, "Иван")       # имя совпадает
    self.assertEqual(client.budget, 50000.0)     # бюджет совпадает
```
**Смысл:** создаём клиента с id=1, именем «Иван» и бюджетом 50000. Проверяем, что поля `name` и `budget` сохранились правильно. Если конструктор работает верно — тест пройдёт.

#### `test_client_negative_budget`
```python
def test_client_negative_budget(self):
    with self.assertRaises(ValueError):
        Client(2, "Должник", -1000.0)
```
**Смысл:** пытаемся создать клиента с бюджетом −1000. В конструкторе `Client` стоит проверка `if budget < 0: raise ValueError(...)`. Тест ожидает, что при отрицательном бюджете выбросится `ValueError`. Если ошибка **не** выбрасывается — тест провалится.

---

### 🧑‍💼 `tests/test_agent.py` — Тесты агента (1 тест)

| № | Тест | Что проверяет |
|---|------|---------------|
| 3 | `test_assign_client` | Закрепление клиента за агентом |

#### `test_assign_client`
```python
def test_assign_client(self):
    agent = Agent(1, "Смит", 5)
    client = Client(1, "Нео", 10000.0)
    agent.assign_client(client)
    self.assertEqual(len(agent.clients), 1)          # 1 клиент в списке
    self.assertEqual(agent.clients[0].name, "Нео")   # и это "Нео"
```
**Смысл:** создаём агента «Смит» и клиента «Нео». Вызываем `assign_client()`, после чего проверяем, что список `agent.clients` содержит ровно одного клиента и это «Нео». Тест проверяет базовую работу метода привязки клиента к агенту.

---

### 🏡 `tests/test_property.py` — Тесты недвижимости (3 теста)

Используется `setUp()` — перед **каждым** тестом создаётся новая квартира:
```python
def setUp(self):
    self.prop = Property(1, "ул. Тестовая, 1", 100000.0, 50.0)
```

| № | Тест | Что проверяет |
|---|------|---------------|
| 4 | `test_property_initial_state` | Новый объект доступен для продажи |
| 5 | `test_property_sell_success` | После продажи объект становится недоступным |
| 6 | `test_property_sell_already_sold` | Ошибка при повторной продаже |

#### `test_property_initial_state`
```python
def test_property_initial_state(self):
    self.assertTrue(self.prop.is_available)
```
**Смысл:** при создании квартиры поле `is_available` должно быть `True` — объект ещё не продан.

#### `test_property_sell_success`
```python
def test_property_sell_success(self):
    self.prop.sell()
    self.assertFalse(self.prop.is_available)
```
**Смысл:** после вызова `sell()` квартира должна стать недоступной (`is_available = False`).

#### `test_property_sell_already_sold`
```python
def test_property_sell_already_sold(self):
    self.prop.sell()
    with self.assertRaises(RuntimeError):
        self.prop.sell()
```
**Смысл:** продаём квартиру, затем пытаемся продать повторно. Ожидается `RuntimeError`, потому что квартира уже продана. Тест проверяет защиту от двойной продажи.

---

### 📈 `tests/test_market.py` — Тесты рынка (2 теста)

| № | Тест | Что проверяет |
|---|------|---------------|
| 7 | `test_update_trend_success` | Успешное обновление коэффициента рынка |
| 8 | `test_negative_trend_error` | Ошибка при отрицательном коэффициенте |

#### `test_update_trend_success`
```python
def test_update_trend_success(self):
    market = Market("Москва", 1.0)
    market.update_trend(1.2)
    self.assertEqual(market.trend_multiplier, 1.2)
```
**Смысл:** создаём рынок с коэффициентом 1.0 (стабильный), обновляем до 1.2 (рост 20%). Проверяем, что значение сохранилось.

#### `test_negative_trend_error`
```python
def test_negative_trend_error(self):
    market = Market("Москва", 1.0)
    with self.assertRaises(ValueError):
        market.update_trend(-0.5)
```
**Смысл:** коэффициент рынка не может быть отрицательным. При попытке установить −0.5 ожидается `ValueError`.

---

### 📃 `tests/test_document.py` — Тесты документа (2 теста)

Используется `setUp()`:
```python
def setUp(self):
    self.client = Client(1, "Клиент", 100000.0)
    self.agent = Agent(1, "Агент", 5)
    self.property_obj = Property(1, "Улица", 50000.0, 40.0)
```

| № | Тест | Что проверяет |
|---|------|---------------|
| 9 | `test_sign_document` | Подписание документа переводит статус в `True` |
| 10 | `test_sign_already_signed` | Ошибка при повторном подписании |

#### `test_sign_document`
```python
def test_sign_document(self):
    doc = Document(1, self.client, self.agent, self.property_obj)
    self.assertFalse(doc.is_signed)    # черновик — не подписан
    doc.sign()
    self.assertTrue(doc.is_signed)     # теперь подписан
```
**Смысл:** создаём документ (черновик), проверяем что `is_signed = False`. Подписываем — проверяем что стало `True`.

#### `test_sign_already_signed`
```python
def test_sign_already_signed(self):
    doc = Document(1, self.client, self.agent, self.property_obj)
    doc.sign()
    with self.assertRaises(RuntimeError):
        doc.sign()
```
**Смысл:** подписываем документ, пытаемся подписать повторно — ожидается `RuntimeError`. Аналогично защите от двойной продажи квартиры.

---

### 🤝 `tests/test_deal.py` — Тесты сделки (2 теста)

Используется `setUp()`:
```python
def setUp(self):
    self.agent = Agent(1, "Смит", 5)
    self.client = Client(1, "Джон", 70000.0)
    self.property_obj = Property(1, "Улица", 50000.0, 45.0)
    self.document = Document(1, self.client, self.agent, self.property_obj)
```

| № | Тест | Что проверяет |
|---|------|---------------|
| 11 | `test_complete_deal` | Завершение сделки привязывает документ и меняет статус |
| 12 | `test_negative_price_error` | Ошибка при отрицательной цене сделки |

#### `test_complete_deal`
```python
def test_complete_deal(self):
    deal = Deal(1, self.property_obj, self.client, self.agent, 50000.0)
    deal.complete(self.document)
    self.assertTrue(deal.is_completed)              # сделка завершена
    self.assertIs(deal.document, self.document)     # документ привязан
```
**Смысл:** создаём сделку, вызываем `complete(document)`. Проверяем, что `is_completed = True` и поле `document` ссылается на тот же объект документа. `assertIs` проверяет, что это **один и тот же объект в памяти**, а не просто равный по значению.

#### `test_negative_price_error`
```python
def test_negative_price_error(self):
    with self.assertRaises(ValueError):
        Deal(2, self.property_obj, self.client, self.agent, -100.0)
```
**Смысл:** нельзя создать сделку с отрицательной ценой. Конструктор `Deal` выбрасывает `ValueError`.

---

### 🏢 `tests/test_agency.py` — Тесты агентства (12 тестов)

Самый большой тестовый файл. Используется `setUp()`:
```python
def setUp(self):
    self.market = Market("Тестовый рынок", 1.0)
    self.agency = Agency("Тестовое агентство", self.market)
    self.agent = Agent(1, "Иван", 5)
    self.client = Client(1, "Пётр", 100000.0)
    self.prop = Property(1, "ул. Тестовая, 1", 50000.0, 40.0)
```

| № | Тест | Что проверяет |
|---|------|---------------|
| 13 | `test_add_agent` | Добавление агента в агентство |
| 14 | `test_add_client` | Добавление клиента в агентство |
| 15 | `test_add_property` | Добавление объекта недвижимости |
| 16 | `test_add_document` | Добавление документа |
| 17 | `test_add_deal` | Добавление сделки |
| 18 | `test_get_agent_by_id_success` | Поиск агента по id — найден |
| 19 | `test_get_agent_by_id_not_found` | Поиск агента по id — не найден |
| 20 | `test_get_client_by_id_success` | Поиск клиента по id — найден |
| 21 | `test_get_client_by_id_not_found` | Поиск клиента по id — не найден |
| 22 | `test_get_property_by_id_success` | Поиск объекта по id — найден |
| 23 | `test_get_property_by_id_not_found` | Поиск объекта по id — не найден |
| 24 | `test_str` | Строковое представление агентства |

#### Тесты добавления (`test_add_*`)
```python
def test_add_agent(self):
    self.agency.add_agent(self.agent)
    self.assertEqual(len(self.agency.agents), 1)         # в списке 1 агент
    self.assertEqual(self.agency.agents[0].name, "Иван") # и это "Иван"
```
**Смысл (для всех add-тестов):** добавляем сущность в агентство через `add_*()`, затем проверяем, что соответствующий список (`agents`, `clients`, `properties`, `documents`, `deals`) увеличился на 1. Для агента и клиента дополнительно проверяется имя.

#### Тесты поиска — успех (`test_get_*_by_id_success`)
```python
def test_get_agent_by_id_success(self):
    self.agency.add_agent(self.agent)
    found = self.agency.get_agent_by_id(1)
    self.assertEqual(found.name, "Иван")
```
**Смысл:** добавляем сущность, затем ищем по id. Если найдена — проверяем, что это та самая сущность (по имени/адресу).

#### Тесты поиска — провал (`test_get_*_by_id_not_found`)
```python
def test_get_agent_by_id_not_found(self):
    with self.assertRaises(ValueError):
        self.agency.get_agent_by_id(999)
```
**Смысл:** ищем по несуществующему id=999 в пустом списке. Ожидается `ValueError`, потому что сущность не найдена.

#### Тест строкового представления
```python
def test_str(self):
    result = str(self.agency)
    self.assertIn("Тестовое агентство", result)   # название в строке
    self.assertIn("Агентов: 0", result)            # 0 агентов
```
**Смысл:** вызываем `str(agency)` (т.е. метод `__str__`). Проверяем, что в результате есть название агентства и количество агентов.

---

### 🔤 `tests/test_str_methods.py` — Тесты `__str__` методов (11 тестов)

Проверяют, что при вызове `str(объект)` (или `print(объект)`) выводится осмысленная строка.

| № | Тест | Что проверяет |
|---|------|---------------|
| 25 | `test_client_str` | `str(Client)` содержит имя и бюджет |
| 26 | `test_agent_str` | `str(Agent)` содержит имя и опыт |
| 27 | `test_property_str_available` | `str(Property)` — доступный объект, содержит «Доступен» |
| 28 | `test_property_str_sold` | `str(Property)` — проданный, содержит «Продан» |
| 29 | `test_market_str_stable` | `str(Market)` при коэфф. 1.0 — «Стабилен» |
| 30 | `test_market_str_growing` | `str(Market)` при коэфф. 1.2 — «Растет» |
| 31 | `test_market_str_falling` | `str(Market)` при коэфф. 0.8 — «Падает» |
| 32 | `test_document_str` | `str(Document)` черновик — содержит «Черновик», имена |
| 33 | `test_document_str_signed` | `str(Document)` подписан — содержит «Подписан» |
| 34 | `test_deal_str_in_progress` | `str(Deal)` незавершённая — содержит «В процессе» |
| 35 | `test_deal_str_completed` | `str(Deal)` завершённая — содержит «Завершена» |

#### Пример: тест строки клиента
```python
def test_client_str(self):
    client = Client(1, "Иван", 50000.0)
    result = str(client)
    self.assertIn("Иван", result)       # имя есть в строке
    self.assertIn("50000.0", result)     # бюджет есть в строке
```
**Смысл:** метод `__str__` клиента должен выводить его имя и бюджет. Тест не проверяет точный формат строки (это хрупко), а проверяет **наличие** ключевых данных.

#### Пример: три состояния рынка
```python
def test_market_str_stable(self):       # коэфф = 1.0
    market = Market("Минск", 1.0)
    self.assertIn("Стабилен", str(market))

def test_market_str_growing(self):      # коэфф = 1.2
    market = Market("Минск", 1.2)
    self.assertIn("Растет", str(market))

def test_market_str_falling(self):      # коэфф = 0.8
    market = Market("Минск", 0.8)
    self.assertIn("Падает", str(market))
```
**Смысл:** метод `__str__` рынка выводит текстовое описание тренда в зависимости от `trend_multiplier`: если = 1.0 → «Стабилен», > 1.0 → «Растет», < 1.0 → «Падает».

#### Пример: документ в двух состояниях
```python
def test_document_str(self):                        # черновик
    doc = Document(1, client, agent, prop)
    self.assertIn("Черновик", str(doc))

def test_document_str_signed(self):                 # подписанный
    doc = Document(1, client, agent, prop)
    doc.sign()
    self.assertIn("Подписан", str(doc))
```
**Смысл:** черновик документа показывает «Черновик», а после подписания — «Подписан». Тест проверяет, что `__str__` корректно отражает текущее состояние.

---

## Часть 2: Тесты сервисов (`test_services/`)

---

### 🏦 `test_services/test_deal_service.py` — Тесты сервиса сделок (3 теста)

Самый важный сервис — проводит полный цикл сделки.

Используется `setUp()`:
```python
def setUp(self):
    self.agent = Agent(1, "Агент Смит", 10)
    self.rich_client = Client(1, "Богач", 100000.0)      # бюджет 100k
    self.poor_client = Client(2, "Бедняк", 10000.0)      # бюджет 10k
    self.property = Property(1, "Вилла", 50000.0, 100.0)  # цена 50k
```

| № | Тест | Что проверяет |
|---|------|---------------|
| 36 | `test_make_deal_success` | Полный успешный сценарий сделки |
| 37 | `test_make_deal_not_enough_money` | Ошибка при нехватке денег |
| 38 | `test_make_deal_already_sold` | Ошибка при продаже уже проданного объекта |

#### `test_make_deal_success`
```python
def test_make_deal_success(self):
    deal = DealService.make_deal(1, self.rich_client, self.agent, self.property)

    self.assertEqual(self.rich_client.budget, 50000.0)   # 100k - 50k = 50k
    self.assertFalse(self.property.is_available)           # квартира продана
    self.assertTrue(deal.is_completed)                     # сделка завершена
    self.assertEqual(deal.client.name, "Богач")            # клиент — Богач
    self.assertIsNotNone(deal.document)                    # документ создан
    self.assertTrue(deal.document.is_signed)               # документ подписан
```
**Смысл:** «Богач» (100k) покупает «Виллу» (50k). После сделки:
- Бюджет клиента уменьшился: 100000 − 50000 = 50000 ✅
- Квартира помечена как проданная ✅
- Сделка завершена (`is_completed = True`) ✅
- Документ создан и подписан автоматически ✅

Это **интеграционный тест** — проверяет всю цепочку: списание денег → продажа → документ → закрытие сделки.

#### `test_make_deal_not_enough_money`
```python
def test_make_deal_not_enough_money(self):
    with self.assertRaises(ValueError):
        DealService.make_deal(2, self.poor_client, self.agent, self.property)
```
**Смысл:** «Бедняк» (10k) пытается купить «Виллу» (50k). Денег не хватает → `ValueError`.

#### `test_make_deal_already_sold`
```python
def test_make_deal_already_sold(self):
    DealService.make_deal(3, self.rich_client, self.agent, self.property)
    with self.assertRaises(RuntimeError):
        DealService.make_deal(4, self.poor_client, self.agent, self.property)
```
**Смысл:** сначала продаём «Виллу» «Богачу». Затем пытаемся продать ту же квартиру повторно — ожидается `RuntimeError`.

---

### 📝 `test_services/test_document_service.py` — Тесты сервиса документов (1 тест)

| № | Тест | Что проверяет |
|---|------|---------------|
| 39 | `test_draft_and_sign` | Создание черновика и подписание через сервис |

#### `test_draft_and_sign`
```python
def test_draft_and_sign(self):
    client = Client(1, "Джон", 50000.0)
    agent = Agent(1, "Смит", 5)
    prop = Property(1, "Улица", 20000.0, 30.0)

    doc = DocumentService.draft_document(1, client, agent, prop)
    self.assertFalse(doc.is_signed)       # черновик — не подписан

    DocumentService.sign_document(doc)
    self.assertTrue(doc.is_signed)        # теперь подписан
```
**Смысл:** проверяет двухэтапный процесс: `draft_document()` создаёт черновик (не подписан), `sign_document()` подписывает его. Отдельный тест на сервисный слой (а не напрямую `Document.sign()`).

---

### 🔍 `test_services/test_search_service.py` — Тесты сервиса поиска (2 теста)

Используется `setUp()` — три квартиры, одна из которых уже продана:
```python
def setUp(self):
    self.prop1 = Property(1, "Дешевая", 30000.0, 30.0)     # продана!
    self.prop2 = Property(2, "Дорогая", 150000.0, 100.0)
    self.prop3 = Property(3, "Средняя", 70000.0, 60.0)
    self.prop1.sell()                                         # помечаем как проданную
    self.all_properties = [self.prop1, self.prop2, self.prop3]
```

| № | Тест | Что проверяет |
|---|------|---------------|
| 40 | `test_find_properties_by_price` | Поиск по максимальной цене |
| 41 | `test_find_properties_by_area` | Поиск по минимальной площади |

#### `test_find_properties_by_price`
```python
def test_find_properties_by_price(self):
    found = SearchService.find_properties(self.all_properties, max_price=100000.0)
    self.assertEqual(len(found), 1)
    self.assertEqual(found[0].address, "Средняя")
```
**Смысл:** ищем квартиры до 100000$. «Дешевая» (30k) подходит по цене, но **уже продана**. «Дорогая» (150k) — слишком дорогая. Остаётся «Средняя» (70k) — единственный результат. Тест проверяет, что поиск фильтрует и по цене, и по доступности.

#### `test_find_properties_by_area`
```python
def test_find_properties_by_area(self):
    found = SearchService.find_properties(self.all_properties, min_area=80.0)
    self.assertEqual(len(found), 1)
    self.assertEqual(found[0].address, "Дорогая")
```
**Смысл:** ищем квартиры от 80 кв.м. «Дешевая» (30 кв.м) — продана и мала. «Средняя» (60 кв.м) — мала. «Дорогая» (100 кв.м) — подходит. Единственный результат.

---

### 💰 `test_services/test_valuation_service.py` — Тесты сервиса оценки (1 тест)

| № | Тест | Что проверяет |
|---|------|---------------|
| 42 | `test_estimate_market_value_with_market_object` | Расчёт рыночной стоимости с учётом коэффициента |

#### `test_estimate_market_value_with_market_object`
```python
def test_estimate_market_value_with_market_object(self):
    property_obj = Property(1, "Улица", 100000.0, 50.0)
    market = Market("Минск", 1.15)                           # рост 15%

    estimated_value = ValuationService.estimate_market_value(property_obj, market)

    self.assertEqual(estimated_value, 115000.0)              # 100000 × 1.15 = 115000
```
**Смысл:** квартира стоит 100000$, рынок растёт (коэфф. 1.15 = +15%). Рыночная стоимость: 100000 × 1.15 = 115000$. Тест проверяет, что формула `price × trend_multiplier` работает корректно.

---

### 👁️ `test_services/test_viewing_service.py` — Тесты сервиса просмотров (1 тест)

| № | Тест | Что проверяет |
|---|------|---------------|
| 43 | `test_arrange_viewing_sold_property` | Ошибка при просмотре проданного объекта |

#### `test_arrange_viewing_sold_property`
```python
def test_arrange_viewing_sold_property(self):
    client = Client(1, "Покупатель", 10000.0)
    agent = Agent(1, "Агент", 2)
    prop = Property(1, "Квартира", 50000.0, 40.0)
    prop.sell()                                     # квартира уже продана

    with self.assertRaises(ValueError):
        ViewingService.arrange_viewing(client, agent, prop)
```
**Смысл:** нельзя организовать просмотр уже проданной квартиры. Сервис проверяет `is_available` и выбрасывает `ValueError`. Тест гарантирует, что просмотры возможны **только** для доступных объектов.

---

## Сводная таблица: все 43 теста

| № | Файл | Тест | Тип проверки |
|---|------|------|--------------|
| 1 | `test_client.py` | `test_client_creation_success` | Создание объекта |
| 2 | `test_client.py` | `test_client_negative_budget` | Валидация (ValueError) |
| 3 | `test_agent.py` | `test_assign_client` | Метод модели |
| 4 | `test_property.py` | `test_property_initial_state` | Начальное состояние |
| 5 | `test_property.py` | `test_property_sell_success` | Изменение состояния |
| 6 | `test_property.py` | `test_property_sell_already_sold` | Защита (RuntimeError) |
| 7 | `test_market.py` | `test_update_trend_success` | Метод модели |
| 8 | `test_market.py` | `test_negative_trend_error` | Валидация (ValueError) |
| 9 | `test_document.py` | `test_sign_document` | Изменение состояния |
| 10 | `test_document.py` | `test_sign_already_signed` | Защита (RuntimeError) |
| 11 | `test_deal.py` | `test_complete_deal` | Завершение сделки |
| 12 | `test_deal.py` | `test_negative_price_error` | Валидация (ValueError) |
| 13 | `test_agency.py` | `test_add_agent` | Добавление в контейнер |
| 14 | `test_agency.py` | `test_add_client` | Добавление в контейнер |
| 15 | `test_agency.py` | `test_add_property` | Добавление в контейнер |
| 16 | `test_agency.py` | `test_add_document` | Добавление в контейнер |
| 17 | `test_agency.py` | `test_add_deal` | Добавление в контейнер |
| 18 | `test_agency.py` | `test_get_agent_by_id_success` | Поиск по id |
| 19 | `test_agency.py` | `test_get_agent_by_id_not_found` | Поиск — ошибка |
| 20 | `test_agency.py` | `test_get_client_by_id_success` | Поиск по id |
| 21 | `test_agency.py` | `test_get_client_by_id_not_found` | Поиск — ошибка |
| 22 | `test_agency.py` | `test_get_property_by_id_success` | Поиск по id |
| 23 | `test_agency.py` | `test_get_property_by_id_not_found` | Поиск — ошибка |
| 24 | `test_agency.py` | `test_str` | `__str__` |
| 25 | `test_str_methods.py` | `test_client_str` | `__str__` |
| 26 | `test_str_methods.py` | `test_agent_str` | `__str__` |
| 27 | `test_str_methods.py` | `test_property_str_available` | `__str__` |
| 28 | `test_str_methods.py` | `test_property_str_sold` | `__str__` |
| 29 | `test_str_methods.py` | `test_market_str_stable` | `__str__` |
| 30 | `test_str_methods.py` | `test_market_str_growing` | `__str__` |
| 31 | `test_str_methods.py` | `test_market_str_falling` | `__str__` |
| 32 | `test_str_methods.py` | `test_document_str` | `__str__` |
| 33 | `test_str_methods.py` | `test_document_str_signed` | `__str__` |
| 34 | `test_str_methods.py` | `test_deal_str_in_progress` | `__str__` |
| 35 | `test_str_methods.py` | `test_deal_str_completed` | `__str__` |
| 36 | `test_deal_service.py` | `test_make_deal_success` | Интеграционный |
| 37 | `test_deal_service.py` | `test_make_deal_not_enough_money` | Валидация (ValueError) |
| 38 | `test_deal_service.py` | `test_make_deal_already_sold` | Защита (RuntimeError) |
| 39 | `test_document_service.py` | `test_draft_and_sign` | Сервисный слой |
| 40 | `test_search_service.py` | `test_find_properties_by_price` | Фильтрация |
| 41 | `test_search_service.py` | `test_find_properties_by_area` | Фильтрация |
| 42 | `test_valuation_service.py` | `test_estimate_market_value_with_market_object` | Расчёт |
| 43 | `test_viewing_service.py` | `test_arrange_viewing_sold_property` | Валидация (ValueError) |

---

## Используемые методы `unittest`

| Метод | Что делает | Пример |
|-------|-----------|--------|
| `assertEqual(a, b)` | Проверяет `a == b` | `assertEqual(client.name, "Иван")` |
| `assertTrue(x)` | Проверяет `x is True` | `assertTrue(deal.is_completed)` |
| `assertFalse(x)` | Проверяет `x is False` | `assertFalse(prop.is_available)` |
| `assertIn(a, b)` | Проверяет `a in b` | `assertIn("Иван", str(client))` |
| `assertIs(a, b)` | Проверяет `a is b` (тот же объект) | `assertIs(deal.document, doc)` |
| `assertIsNotNone(x)` | Проверяет `x is not None` | `assertIsNotNone(deal.document)` |
| `assertRaises(Error)` | Ожидает выброс исключения | `assertRaises(ValueError)` |

---

## Как запустить все тесты

```bash
# Тесты моделей (35 шт.)
python -m unittest discover -s tests -v

# Тесты сервисов (8 шт.)
python -m unittest discover -s test_services -v

# Всё вместе
python -m unittest discover -s tests -v && python -m unittest discover -s test_services -v
```

Ожидаемый результат:
```
Ran 35 tests in 0.003s — OK
Ran 8 tests in 0.001s — OK
```
