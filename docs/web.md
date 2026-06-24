# Flask и Jinja2 — подробное руководство

Документ для тех, кто только начинает. В каждом разделе: **что это**, **зачем нужно**, **как использовать** на практике.

---

## Часть 1. Как вообще работает веб

### Зачем понимать HTTP

Flask не «магия» — он обрабатывает обычные HTTP-запросы от браузера. Если понимать GET/POST и что уходит в ответе, проще отлаживать формы, ссылки и ошибки «данные не пришли».

### Аналогия

- **браузер** — гость (делает заказ)
- **сервер с Flask** — кухня (готовит ответ)
- **HTML** — блюдо на столе
- **база данных** — склад (Flask берёт данные, Jinja оформляет в HTML)

Гость видит только страницу в браузере, не ваш Python-код.

### HTTP-запрос и ответ

Каждый клик по ссылке или отправка формы — отдельный **запрос**. Сервер отвечает **ответом**.

**Запрос:** метод + URL + (опционально) тело  
**Ответ:** код статуса + HTML/JSON/файл

Частые коды:
- `200` — всё ок, вот страница
- `302` — перейди на другой URL (redirect)
- `404` — страница не найдена
- `500` — ошибка на сервере

### GET и POST

| | GET | POST |
|---|-----|------|
| **Зачем** | Прочитать страницу или данные | Отправить данные на сервер |
| **Где данные** | В URL: `?page=2` | В теле запроса (форма) |
| **Как использовать** | Списки, просмотр, поиск, фильтры | Создание, изменение, удаление |

**Правило:** если операция **меняет** данные на сервере (сохранить, удалить) — обычно **POST**. Если только **показать** — **GET**.

### Что делает Flask

```
URL + метод  →  какая функция?  →  вызвать  →  вернуть ответ
```

**Зачем фреймворк:** не разбирать HTTP вручную — писать функции и шаблоны.

**Как использовать:** одна view-функция = один сценарий (список, форма, удаление).

---

## Часть 2. Минимальное приложение

### Зачем такая структура папок

```
my_site/
  app.py           # маршруты и логика
  templates/       # HTML-шаблоны (Jinja)
  static/          # CSS, JS, картинки (отдаются как есть)
```

Flask **сам ищет** `templates/` и `static/` рядом с приложением. Разделение нужно, чтобы не смешивать Python, разметку и стили.

### Пример

**app.py:**

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("hello.html", name="Анна")

if __name__ == "__main__":
    app.run(debug=True)
```

**templates/hello.html:**

```html
<h1>Привет, {{ name }}!</h1>
```

### Как это работает по шагам

1. Браузер: `GET /`
2. Flask вызывает `home()`
3. `render_template("hello.html", name="Анна")` — передаёт `name` в Jinja
4. Jinja подставляет `Анна` вместо `{{ name }}`
5. Браузер показывает: **Привет, Анна!**

### Зачем передавать переменные явно

Шаблон **не видит** переменные Python сам. Всё, что нужно в HTML, передаётся в `render_template(..., имя=значение)`.

### `debug=True`

В режиме разработки: автоперезагрузка при изменении кода и подробные ошибки в браузере. **В продакшене отключать.**

---

## Часть 3. Маршруты (routes)

### Зачем нужны маршруты

Маршрут связывает **адрес в браузере** с **вашей функцией**. Без `@app.route` Flask не знает, какой код запустить для `/about`.

### Базовый маршрут

```python
@app.route("/hello")
def hello():
    return "Привет"
```

| URL | Функция | Endpoint (внутреннее имя) |
|-----|---------|---------------------------|
| `/hello` | `hello` | `hello` |

**Endpoint** — имя для `url_for("hello")`. Пользователь видит URL, вы в коде ссылаетесь на endpoint.

### Несколько страниц

```python
@app.route("/")
def index():
    return "Главная"

@app.route("/about")
def about():
    return "О нас"
```

**Как использовать:** одна функция — одна задача. Не смешивайте список, форму и удаление в одной огромной функции без необходимости.

### Параметр в URL

```python
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    return f"Книга {book_id}"
```

**Зачем:** один маршрут для всех книг (`/books/1`, `/books/2`, …), а не отдельная функция на каждый id.

**Как использовать:** имя в `<>` = аргумент функции. Тип (`int`, `string`) — проверка: `/books/abc` даст 404.

### GET и POST на одном URL

```python
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        message = request.form.get("message", "")
        save(message)
        return redirect(url_for("thanks"))
    return render_template("feedback.html")
```

**Зачем один URL:** форма часто отправляется на тот же адрес, где показана (`action` = текущая страница).

**Как использовать:**
- `GET` → показать форму
- `POST` → прочитать `request.form`, сохранить, `redirect`

---

## Часть 4. Объект `request`

### Зачем нужен `request`

Во view-функции нужно знать: какой метод, какие поля формы, какие параметры в URL. Всё это в объекте `request` **на время одного запроса**.

### `request.form` — данные POST-формы

**Зачем:** после нажатия «Сохранить» поля формы попадают сюда.

HTML:

```html
<input name="email" value="user@mail.com">
```

Python:

```python
request.form.get("email")  # "user@mail.com"
```

**Как использовать:**
- `name` в HTML **обязан** совпадать с ключом в `request.form`
- `.get("ключ", "")` — безопасно, если поля нет
- всё приходит **строками** — числа преобразуйте: `int(...)`, `float(...)`

### `request.args` — параметры в URL

URL: `/products?category=books&page=2`

```python
request.args.get("category")  # "books"
request.args.get("page", "1")  # "2" или "1" по умолчанию
```

**Зачем:** поиск, фильтры, пагинация — без изменения данных на сервере.

**Как использовать:**
- форма с `method="get"` → параметры в адресной строке
- ссылку можно скопировать и отправить коллеге
- для сохранения/удаления записей **не** используйте GET

### Пример: поиск

```python
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = find(query) if query else []
    return render_template("search.html", query=query, results=results)
```

```html
<form method="get">
  <input name="q" value="{{ query or '' }}">
  <button type="submit">Найти</button>
</form>
```

**Зачем `value="{{ query or '' }}"`:** после поиска в поле остаётся введённый текст.

---

## Часть 5. Ответы сервера

### `render_template` — отдать HTML-страницу

```python
return render_template("list.html", items=items, title="Список")
```

**Зачем:** отделить Python (данные) от HTML (вёрстка).

**Как использовать:** передавайте в шаблон всё, что нужно для отображения: списки, заголовки, флаги ошибок.

### `redirect` — отправить браузер на другой URL

```python
return redirect(url_for("item_list"))
```

**Зачем:**
- после сохранения формы — показать список, а не ту же форму
- избежать повторной отправки при F5 (паттерн PRG)

**Как использовать:** после успешного POST почти всегда `flash` + `redirect`, а не `render_template` той же формы.

### PRG (Post → Redirect → Get)

```
POST /items/new  →  сохранили  →  redirect  →  GET /items
```

**Без redirect:** F5 спросит «повторить отправку?» → дубликат записи.  
**С redirect:** F5 просто обновит список.

---

## Часть 6. `url_for` — правильные ссылки

### Зачем не писать URL вручную

```html
<a href="/users/42/edit">  <!-- хрупко -->
```

Сменили путь в `@app.route` — все ссылки сломались.

### Как работает `url_for`

Flask строит URL по **endpoint** (имени функции) и параметрам:

```python
@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    ...
```

```python
url_for("edit_user", user_id=42)  # → "/users/42/edit"
```

В шаблоне:

```html
<a href="{{ url_for('edit_user', user_id=user.id) }}">Изменить</a>
```

**Как использовать:**
- в `<a href>`, в `<form action>`, в `redirect(url_for(...))`
- передать **все** параметры маршрута (`user_id`, `item_id`, …)

### Blueprint

```python
bp = Blueprint("shop", __name__, url_prefix="/shop")

@bp.route("/items")
def item_list():
    ...
```

Endpoint: `shop.item_list`, URL: `/shop/items`.

```html
{{ url_for('shop.item_list') }}
```

**Зачем blueprint:** разбить большое приложение на модули (магазин, админка, API), не смешивая маршруты в одном файле.

### Статические файлы

```html
<link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
```

**Зачем:** CSS/JS не вшивают в Python — лежат в `static/`, Flask отдаёт по `/static/...`.

**Как использовать:** один CSS в `base.html` — стили на всех страницах.

---

## Часть 7. Flash-сообщения

### Зачем нужен flash

После `redirect` начинается **новый** запрос. Обычные переменные Python (`message = "Сохранено"`) **исчезают**.

Нужен способ сказать следующей странице: «покажи пользователю зелёное уведомление».

### Как работает

```python
flash("Товар сохранён", "success")
return redirect(url_for("item_list"))
```

1. Сообщение кладётся в **сессию** (cookie в браузере, подписанная секретным ключом)
2. Браузер переходит на список (новый GET)
3. Шаблон вызывает `get_flashed_messages()` — сообщение показывается **один раз**

В **base.html** (один раз на весь сайт):

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="flash {{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
```

**Как использовать:**
- `"success"` — зелёное «Сохранено»
- `"error"` — красное «Ошибка валидации»
- категория → CSS-класс: `.flash.success`, `.flash.error`

**Настройка:** `app.secret_key = "случайная-длинная-строка"` — без этого flash и сессии не работают.

---

## Часть 8. Jinja2 — шаблонизатор

### Зачем Jinja, а не HTML в Python

Сборка HTML строками в Python — нечитаемо и небезопасно. Jinja даёт HTML + вставки логики:

```html
{% for item in items %}
  <li>{{ item.name }}</li>
{% endfor %}
```

**Как использовать:** в шаблоне только **отображение**. Запросы к БД и валидация — в Flask.

### Три вида скобок

| Синтаксис | Назначение |
|-----------|------------|
| `{{ ... }}` | Вывести значение в HTML |
| `{% ... %}` | Условие, цикл, наследование (в HTML не видно) |
| `{# ... #}` | Комментарий для разработчика |

### Переменные

```python
render_template("page.html", title="Блог", items=[])
```

```html
<h1>{{ title }}</h1>
```

**Зачем явная передача:** шаблон знает только то, что вы передали. Имя в Python = имя в шаблоне.

**Полезные выражения:**

```html
{{ text or "—" }}           <!-- если пусто — прочерк -->
{{ price * 1.2 }}           <!-- простая арифметика -->
{{ items|length }}          <!-- фильтр: длина списка -->
```

### Условия `{% if %}`

```html
{% if items %}
  <table>...</table>
{% else %}
  <p>Ничего не найдено</p>
{% endif %}
```

**Зачем:** один шаблон и для пустого списка, и для заполненного.

**Как использовать:** `{% if item %}` — различать создание (`item=None`) и редактирование.

### Циклы `{% for %}`

```html
{% for product in products %}
  <tr>
    <td>{{ loop.index }}</td>
    <td>{{ product.name }}</td>
  </tr>
{% else %}
  <tr><td colspan="2">Товаров нет</td></tr>
{% endfor %}
```

**Зачем `loop.index`:** порядковый номер строки.  
**Зачем `{% else %}` у for:** сработает, если список пуст.

### Наследование `{% extends %}`

**Зачем:** меню, шапка, footer, flash — один раз в `base.html`. Страницы переопределяют только `content`.

**base.html:**

```html
<head>
  <title>{% block title %}Сайт{% endblock %}</title>
</head>
<body>
  <nav>...</nav>
  {% block content %}{% endblock %}
</body>
```

**page.html:**

```html
{% extends "base.html" %}

{% block content %}
  <h1>Заголовок страницы</h1>
{% endblock %}
```

**Как использовать:**
- `{% extends %}` — **первая** строка дочернего шаблона
- общее (меню, flash, CSS) — в base
- уникальное содержимое — в блоке `content`

### Фильтры

```html
{{ name|upper }}
{{ description|default("Нет описания") }}
```

**Зачем:** форматировать вывод, не меняя данные в Python.

---

## Часть 9. Формы — полный цикл

### Зачем формы в веб-приложении

Форма — способ отправить данные с страницы на сервер: регистрация, создание записи, фильтр.

Связка: **HTML `name`** → **`request.form`** → **сохранение в БД** → **redirect** → **сообщение flash**.

### Список записей

**View:**

```python
@app.route("/items")
def item_list():
    items = load_all()
    return render_template("items/list.html", items=items)
```

**Шаблон:**

```html
<a href="{{ url_for('create_item') }}">Добавить</a>
{% for item in items %}
  <a href="{{ url_for('edit_item', item_id=item.id) }}">Изменить</a>
{% endfor %}
```

**Зачем `url_for` в цикле:** у каждой строки свой `item.id` — своя ссылка на редактирование.

### Создание (GET + POST)

```python
@app.route("/items/new", methods=["GET", "POST"])
def create_item():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Введите название", "error")
        else:
            save_item(title)
            flash("Создано", "success")
            return redirect(url_for("item_list"))
    return render_template("items/form.html", item=None)
```

**Зачем `item=None`:** шаблон один на создание и редактирование; при создании поля пустые.

### Шаблон формы

```html
<form method="post">
  <input name="title" value="{{ item.title if item else '' }}" required>
  <button type="submit">Сохранить</button>
</form>
```

| Атрибут | Зачем |
|---------|--------|
| `method="post"` | данные в теле запроса, не в URL |
| `name="title"` | ключ в `request.form` |
| `value="..."` | показать сохранённое значение при редактировании |
| `required` | браузер не отправит пустое (дополнительно проверяйте в Python) |

### Редактирование — тот же шаблон

```python
return render_template("items/form.html", item=item)
```

**Зачем один шаблон:** меньше дублирования. Различие только в данных: `item=None` или объект с полями.

### Удаление — только POST

```html
<form method="post" action="{{ url_for('delete_item', item_id=item.id) }}">
  <button type="submit">Удалить</button>
</form>
```

**Зачем не `<a href=".../delete">`:** ссылка = GET. Поисковик или случайный клик мог бы удалить запись. POST-форма — осознанное действие.

### Типы полей

| Поле | На сервере | Зачем |
|------|------------|--------|
| `<input name="title">` | `request.form.get("title")` | текст |
| `<input type="number">` | строка → `int()` / `float()` | числа |
| `<input type="date">` | строка `"2025-06-16"` | даты |
| `<select name="cat_id">` | строка с id | выбор из списка |
| `<textarea name="body">` | многострочный текст | описания |

### 9.6. Атрибут `selected` — подробно

#### Что такое `<select>`

Выпадающий список — набор `<option>`. Пользователь видит один выбранный пункт.

```html
<select name="direction_id">
  <option value="1">Программирование</option>
  <option value="2">Дизайн</option>
</select>
```

- `value` — уходит на сервер при сохранении
- текст между тегами — видит пользователь

#### Что делает `selected`

```html
<option value="2" selected>Дизайн</option>
```

Браузер сразу покажет «Дизайн» выбранным. Без `selected` выбран первый пункт (часто пустой «— выберите —»).

#### Зачем при редактировании

При создании направление не выбрано. При редактировании курс уже привязан к `direction_id = 2` — в списке должен быть выбран этот пункт, иначе кажется, что поле пустое.

#### Как в Jinja

```html
<select name="direction_id">
  <option value="">— выберите —</option>
  {% for direction in directions %}
  <option value="{{ direction.id }}"
    {% if item and item.direction_id == direction.id %}selected{% endif %}>
    {{ direction.name }}
  </option>
  {% endfor %}
</select>
```

| Часть условия | Смысл |
|---------------|--------|
| `item` | режим редактирования (не создание) |
| `item.direction_id == direction.id` | этот вариант — сохранённый |
| `selected` | вставить атрибут в тег |

#### Итоговый HTML (пример)

```html
<option value="1">Программирование</option>
<option value="2" selected>Дизайн</option>
<option value="3">Маркетинг</option>
```

#### Аналогия

| Элемент | Как показать сохранённое значение |
|---------|-----------------------------------|
| `<input>` | `value="{{ item.name }}"` |
| `<select>` | `selected` у нужного `<option>` |
| `<textarea>` | текст между тегами |

`selected` влияет только на отображение при загрузке. При отправке уходит `value` выбранного пункта: `request.form.get("direction_id")` → `"2"`.

---

## Часть 10. Blueprint — структура проекта

### Зачем

В маленьком приложении маршруты в одном `app.py`. Когда разделов много (товары, пользователи, заказы), файл раздувается. **Blueprint** — отдельный модуль маршрутов со своим префиксом URL.

### Как использовать

**Файл модуля:**

```python
bp = Blueprint("shop", __name__, url_prefix="/shop")

@bp.route("/items")
def item_list():
    return render_template("shop/list.html", items=...)
```

**Главное приложение:**

```python
app.register_blueprint(shop_bp)
```

| Функция | Endpoint | URL |
|---------|----------|-----|
| `item_list` | `shop.item_list` | `/shop/items` |

**Шаблоны** остаются в общей `templates/` (удобно группировать: `templates/shop/list.html`).

**Когда вводить:** когда в одном файле больше ~10–15 маршрутов или логически разные разделы сайта.

---

## Часть 11. Application factory

### Зачем

```python
def create_app():
    app = Flask(__name__)
    app.secret_key = "..."
    app.register_blueprint(shop_bp)
    return app
```

**Не** создавать `app = Flask(__name__)` глобально при импорте, а собирать приложение в функции.

**Как использовать:**
- тесты: `app = create_app()` для каждого теста
- разные конфиги: dev/prod
- инициализация БД, blueprints в одном месте

---

## Часть 12. Что где писать

| Задача | Flask | Jinja | Почему |
|--------|-------|-------|--------|
| Запрос к БД | ✓ | ✗ | доступ к данным только на сервере |
| Валидация «цена > 0» | ✓ | ✗ | правила и безопасность |
| Решение redirect / ошибка | ✓ | ✗ | управление потоком HTTP |
| Таблица со списком | ✗ | ✓ | это вёрстка |
| «Список пуст» | ✗ | ✓ | условие отображения |
| Ссылки | ✗ | ✓ | `url_for` в шаблоне |
| CSS | ✗ | ✓ | `url_for('static', ...)` |
| «Сохранено» | flash в Python | вывод в base | сообщение через redirect |

**Принцип:** Python **готовит** и **решает**, шаблон **рисует**.

---

## Часть 13. Жизненный цикл запроса (редактирование)

Пользователь меняет название и жмёт «Сохранить»:

```
1.  POST /items/5/edit, тело: title=Учебник
2.  Flask → edit_item(item_id=5)
3.  request.method == "POST"
4.  title = request.form.get("title")
5.  update в БД
6.  flash("Сохранено")
7.  redirect → GET /items
8.  item_list() → render_template(..., items=...)
9.  Jinja: extends, цикл, flash
10. Браузер: список + зелёное сообщение
```

Каждый шаг — отдельный HTTP-запрос после redirect (шаги 7–10 — уже новый GET).

---

## Часть 14. Типичные ошибки

| Ошибка | Что происходит | Как исправить |
|--------|----------------|---------------|
| Нет `name` у input | `request.form` пустой | Добавить `name="..."` |
| Нет `methods=["POST"]` | POST не обрабатывается | Указать methods в route |
| POST без redirect | F5 дублирует запись | PRG: redirect после успеха |
| Жёсткий URL `/items/5` | ломается при смене route | `url_for('edit', item_id=5)` |
| Переменная не в render_template | пусто в HTML | передать в шаблон |
| `extends` не первая строка | ошибка Jinja | `{% extends %}` в начале |
| Удаление через ссылку | случайное удаление | `<form method="post">` |
| Нет secret_key | flash не работает | `app.secret_key = "..."` |

---

## Часть 15. Чеклист новой страницы

1. **Маршрут** — `@app.route`, `methods` если есть форма.
2. **View** — GET: данные + `render_template`; POST: `request.form` → сохранить → `flash` → `redirect`.
3. **Шаблон** — `{% extends "base.html" %}`, блок `content`.
4. **Переменные** — всё для HTML передать в `render_template`.
5. **Ссылки** — `url_for` с нужными параметрами.
6. **Форма** — `name` = ключ в `request.form`.
7. **Flash** — блок в `base.html`.
8. **Стили** — `static/` + `url_for('static', ...)`.

---

## Полезные ссылки

- Flask: https://flask.palletsprojects.com/
- Jinja2: https://jinja.palletsprojects.com/
- HTML-формы: https://developer.mozilla.org/ru/docs/Web/HTML/Element/form
- HTTP: https://developer.mozilla.org/ru/docs/Web/HTTP
