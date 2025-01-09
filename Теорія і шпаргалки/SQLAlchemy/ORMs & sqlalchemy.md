
Робота з базами даних у Python переважно виконується через бібліотеки. Найпоширенішим варіантом є `sqlite3` для роботи з SQLite, яка входить до стандартної бібліотеки. Ось основи роботи:

### Підключення до бази даних

Для створення або підключення до бази даних використовується метод `connect()`:

```python
import sqlite3

# Створення або підключення до файлу бази даних
connection = sqlite3.connect("my_database.db")

# Створення курсора для виконання SQL-запитів
cursor = connection.cursor()
```

### Виконання SQL-запитів

1. **Створення таблиць**:

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
)
""")
connection.commit()
```

2. **Додавання даних**:

```python
cursor.execute("""
INSERT INTO users (name, age)
VALUES (?, ?)
""", ("Alice", 25))
connection.commit()
```

3. **Отримання даних**:

```python
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()  # Отримати всі результати
for row in rows:
    print(row)
```

4. **Оновлення та видалення**:

```python
# Оновлення
cursor.execute("""
UPDATE users SET age = ? WHERE name = ?
""", (26, "Alice"))
connection.commit()

# Видалення
cursor.execute("""
DELETE FROM users WHERE name = ?
""", ("Alice",))
connection.commit()
```

### Закриття з'єднання

Після завершення роботи потрібно закрити з'єднання:

```python
connection.close()
```

### Робота з помилками

Рекомендується використовувати конструкцію `try...except` для обробки помилок:

```python
try:
    connection = sqlite3.connect("my_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM non_existent_table")
except sqlite3.Error as e:
    print(f"Error: {e}")
finally:
    connection.close()
```

### Робота з іншими СУБД

Для роботи з MySQL, PostgreSQL чи іншими базами даних використовуються спеціалізовані бібліотеки:

- **MySQL**: `mysql-connector-python` або `pymysql`
- **PostgreSQL**: `psycopg2`
- **MongoDB**: `pymongo`

Кожна з цих бібліотек має свої специфічні методи, але основні концепції роботи (підключення, виконання запитів) схожі.


# Робота з Connection і Cursor у Python

У Python робота з базами даних організована через **з'єднання (connection)** та **курсор (cursor)**. Ось як вони працюють і взаємодіють.

## Connection (З'єднання)

З'єднання — це об'єкт, який відповідає за взаємодію з базою даних. Воно забезпечує:
- Виконання SQL-запитів.
- Управління транзакціями (підтвердження або скасування змін).
- Закриття з'єднання після завершення роботи.

### Створення з'єднання

Для створення з'єднання використовується функція `sqlite3.connect()`:
```python
import sqlite3

# Підключення до бази даних (створює файл, якщо його ще немає)
connection = sqlite3.connect("example.db")
````

### Основні методи об'єкта Connection

1. **`commit()`**  
    Підтверджує всі виконані зміни у базі даних.
    
    ```python
    connection.commit()
    ```
    
2. **`rollback()`**  
    Скасовує всі зміни, виконані з моменту останнього `commit()`.
    
    ```python
    connection.rollback()
    ```
    
3. **`close()`**  
    Закриває з'єднання з базою даних. Потрібно викликати після завершення роботи.
    
    ```python
    connection.close()
    ```
    
4. **`execute()`**  
    Виконує SQL-запит без створення курсора (корисно для простих операцій).
    
    ```python
    connection.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    ```
    

---

## Cursor (Курсор)

Курсор — це об'єкт, через який виконується більшість операцій із базою даних. Він дозволяє:

- Виконувати SQL-запити.
- Отримувати результати запитів.
- Ітеруватися по результатах.

### Створення курсора

Курсор створюється через з'єднання:

```python
cursor = connection.cursor()
```

### Основні методи об'єкта Cursor

1. **`execute()`**  
    Виконує SQL-запит:
    
    ```python
    cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (1, "Alice"))
    ```
    
2. **`executemany()`**  
    Виконує SQL-запит для кількох наборів даних:
    
    ```python
    data = [(2, "Bob"), (3, "Charlie")]
    cursor.executemany("INSERT INTO users (id, name) VALUES (?, ?)", data)
    ```
    
3. **`fetchone()`**  
    Повертає один рядок результату запиту:
    
    ```python
    cursor.execute("SELECT * FROM users")
    row = cursor.fetchone()
    print(row)
    ```
    
4. **`fetchall()`**  
    Повертає всі результати запиту:
    
    ```python
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    ```
    
5. **`fetchmany(size)`**  
    Повертає вказану кількість рядків:
    
    ```python
    rows = cursor.fetchmany(2)
    print(rows)
    ```
    
6. **`close()`**  
    Закриває курсор:
    
    ```python
    cursor.close()
    ```
    

---

## Приклад повного циклу роботи

```python
import sqlite3

# Створення з'єднання
connection = sqlite3.connect("example.db")

# Створення курсора
cursor = connection.cursor()

# Створення таблиці
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

# Додавання даних
cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (1, "Alice"))
connection.commit()  # Підтвердження змін

# Отримання даних
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Закриття курсора і з'єднання
cursor.close()
connection.close()
```

---

## Примітки

- Використовуйте `commit()` після запитів, які змінюють дані, щоб зберегти зміни.
- Використовуйте `try...except...finally` для обробки помилок і закриття з'єднання навіть у разі помилки:
    
    ```python
    try:
        connection = sqlite3.connect("example.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM non_existent_table")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()
    ```



# SQLAlchemy: Основні особливості

**SQLAlchemy** — це популярна бібліотека Python для роботи з базами даних. Вона забезпечує два основних рівні доступу:
1. **Core (Рівень SQL)**: Робота напряму через SQL-запити.
2. **ORM (Object-Relational Mapping)**: Робота з базою через об'єкти Python.

## Основні особливості SQLAlchemy

### 1. **Робота з різними СУБД**
SQLAlchemy підтримує багато популярних СУБД: SQLite, PostgreSQL, MySQL, Oracle, Microsoft SQL Server та інші. Для підключення до бази даних використовується строка з'єднання (connection string).

```python
from sqlalchemy import create_engine

# Підключення до SQLite
engine = create_engine('sqlite:///example.db')

# Підключення до PostgreSQL
# engine = create_engine('postgresql://user:password@localhost/dbname')
````

---

### 2. **Рівень Core (Робота з SQL)**

SQLAlchemy Core надає інструменти для написання SQL-запитів у Python.

#### Створення таблиці

```python
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)

# Створення таблиці в базі
metadata.create_all(engine)
```

#### Виконання SQL-запитів

```python
with engine.connect() as connection:
    # Вставка даних
    connection.execute(users.insert().values(name="Alice", age=25))
    
    # Вибірка даних
    result = connection.execute(users.select())
    for row in result:
        print(row)
```

---

### 3. **Рівень ORM (Object-Relational Mapping)**

ORM дозволяє працювати з базою даних через об'єкти Python.

#### Налаштування ORM

```python
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

# Створення таблиць у базі
Base.metadata.create_all(engine)
```

#### Робота з об'єктами через ORM

```python
# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Додавання об'єкта
new_user = User(name="Bob", age=30)
session.add(new_user)
session.commit()

# Вибірка даних
users = session.query(User).all()
for user in users:
    print(user.name, user.age)

# Закриття сесії
session.close()
```

---

### 4. **Транзакції**

SQLAlchemy автоматично обгортає всі операції в транзакції. Транзакції можна вручну почати, підтвердити або скасувати:

```python
with engine.connect() as connection:
    trans = connection.begin()
    try:
        connection.execute(users.insert().values(name="Charlie", age=22))
        trans.commit()
    except:
        trans.rollback()
        raise
```

---

### 5. **Сумісність з популярними СУБД**

SQLAlchemy дозволяє писати код, який легко переноситься між СУБД, не змінюючи логіку програми. Достатньо замінити строку з'єднання (`create_engine`).

---

### 6. **Запити через ORM**

SQLAlchemy ORM дозволяє використовувати фільтри, сортування, обмеження:

```python
# Фільтрація
young_users = session.query(User).filter(User.age < 30).all()

# Сортування
sorted_users = session.query(User).order_by(User.name).all()

# Ліміт
limited_users = session.query(User).limit(2).all()
```

---

### 7. **Розширюваність**

SQLAlchemy підтримує:

- Роботу з асоціаціями (зв'язки між таблицями: `one-to-many`, `many-to-many`).
- Міграції через додаткові інструменти (наприклад, Alembic).
- Налаштування кешування.

---

## Переваги SQLAlchemy

- **Абстракція:** Можна працювати як на рівні SQL, так і через ORM.
- **Універсальність:** Підтримка багатьох СУБД.
- **Гнучкість:** Можна використовувати рівень Core, ORM або комбінувати їх.
- **Зручність:** Інтуїтивний API для роботи з об'єктами та запитами.

---

## Приклад: Повний цикл роботи з ORM

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Створення бази
engine = create_engine('sqlite:///example.db')
Base = declarative_base()

# Модель
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

# Створення таблиці
Base.metadata.create_all(engine)

# Сесія
Session = sessionmaker(bind=engine)
session = Session()

# Додавання даних
session.add_all([
    User(name="Alice", age=25),
    User(name="Bob", age=30)
])
session.commit()

# Отримання даних
users = session.query(User).filter(User.age > 25).all()
for user in users:
    print(user.name, user.age)

# Закриття сесії
session.close()
```



