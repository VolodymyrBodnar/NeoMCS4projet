

**SQLAlchemy Core** — це рівень, який забезпечує роботу з базою даних через SQL-запити, але надає додаткові можливості Python API. Він особливо підходить для тих, хто хоче контролювати SQL-запити без використання ORM.

---

## Основні компоненти Core

1. **Engine (Двигун)**: Інтерфейс для взаємодії з базою даних.
2. **MetaData (Метадані)**: Об'єкт для зберігання структури таблиць і взаємозв'язків.
3. **Table (Таблиця)**: Визначення таблиці для взаємодії.
4. **Column (Стовпчик)**: Опис стовпчиків таблиці.
5. **SQL Expressions (SQL-вирази)**: Виконання запитів через вирази Python.

---

## 1. **Engine (Двигун)**

Engine — це об'єкт, який управляє підключенням до бази даних. Створюється через функцію `create_engine()`.

### Створення з'єднання
```python
from sqlalchemy import create_engine

# SQLite
engine = create_engine('sqlite:///example.db')

# PostgreSQL
# engine = create_engine('postgresql://user:password@localhost/dbname')
````

### Виконання запитів через Engine

```python
with engine.connect() as connection:
    result = connection.execute("SELECT 1")
    print(result.scalar())  # Повертає перший результат
```

---

## 2. **MetaData (Метадані)**

MetaData — це об'єкт, який зберігає інформацію про структуру бази даних.

### Приклад створення MetaData

```python
from sqlalchemy import MetaData

metadata = MetaData()
```

---

## 3. **Table (Таблиця)**

Об'єкт `Table` використовується для визначення таблиць.

### Створення таблиці

```python
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)
```

### Створення таблиці у базі

```python
metadata.create_all(engine)  # Створює всі таблиці, описані в MetaData
```

---

## 4. **Виконання SQL-запитів через Table**

SQLAlchemy Core дозволяє створювати і виконувати запити через Python API.

### Вставка даних

```python
with engine.connect() as connection:
    connection.execute(users.insert().values(name="Alice", age=25))
```

### Вибірка даних

```python
with engine.connect() as connection:
    result = connection.execute(users.select())
    for row in result:
        print(row)  # Кожний рядок — це об'єкт Row
```

### Фільтрація

```python
from sqlalchemy import select

with engine.connect() as connection:
    stmt = select(users).where(users.c.age > 20)
    result = connection.execute(stmt)
    for row in result:
        print(row)
```

---

## 5. **SQL Expressions (SQL-вирази)**

SQLAlchemy Core дозволяє створювати SQL-запити за допомогою виразів Python.

### Оператори

- `==`, `<`, `>`, `!=` — порівняння.
- `and_`, `or_` — логічні оператори.

### Приклад фільтрації

```python
from sqlalchemy import and_

stmt = users.select().where(and_(users.c.age > 20, users.c.name == "Alice"))
```

### Агрегації

```python
from sqlalchemy import func

stmt = select(func.count(users.c.id))
with engine.connect() as connection:
    result = connection.execute(stmt)
    print(result.scalar())  # Повертає кількість записів
```

---

## 6. **Оновлення та видалення**

### Оновлення

```python
with engine.connect() as connection:
    connection.execute(users.update().where(users.c.name == "Alice").values(age=30))
```

### Видалення

```python
with engine.connect() as connection:
    connection.execute(users.delete().where(users.c.name == "Alice"))
```

---

## 7. **Транзакції**

SQLAlchemy Core підтримує транзакції, які можна керувати вручну.

### Приклад транзакції

```python
with engine.connect() as connection:
    trans = connection.begin()
    try:
        connection.execute(users.insert().values(name="Bob", age=22))
        trans.commit()  # Підтвердження змін
    except:
        trans.rollback()  # Скасування змін
        raise
```

---

## 8. **Переваги Core**

- **Гнучкість:** Можна писати запити на рівні SQL.
- **Продуктивність:** Менше оверхеду порівняно з ORM.
- **Контроль:** Повний контроль над SQL-запитами.
- **Універсальність:** Підходить для складних або оптимізованих операцій.

---

## Повний приклад роботи з Core

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# Підключення до бази
engine = create_engine('sqlite:///example.db')

# Опис таблиці
metadata = MetaData()
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)

# Створення таблиці
metadata.create_all(engine)

# Вставка даних
with engine.connect() as connection:
    connection.execute(users.insert().values(name="Alice", age=25))
    connection.execute(users.insert().values(name="Bob", age=30))

# Вибірка даних
with engine.connect() as connection:
    result = connection.execute(users.select())
    for row in result:
        print(row)
```