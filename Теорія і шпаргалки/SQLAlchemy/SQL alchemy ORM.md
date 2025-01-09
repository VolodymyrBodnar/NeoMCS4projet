
### Що таке SQLAlchemy ORM?

SQLAlchemy ORM (Object-Relational Mapping) дозволяє працювати з базою даних через Python-класи та об'єкти, а не безпосередньо через SQL-запити. ORM автоматизує процес перетворення між об'єктами Python і таблицями в базі даних.

---

### Основні компоненти ORM

1. **`declarative_base`** — базовий клас для створення моделей.
2. **Моделі (Models)** — класи Python, які відображають таблиці бази даних.
3. **Сесія (Session)** — об'єкт для роботи з базою даних (додавання, видалення, оновлення даних).
4. **Запити (Query)** — виконання запитів до бази даних.

---

### Налаштування ORM

1. **Імпорт бібліотек і створення бази**

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Підключення до бази даних
engine = create_engine('sqlite:///example.db')

# Створення базового класу
Base = declarative_base()
```

2. **Створення моделі**

```python
class User(Base):
    __tablename__ = 'users'  # Назва таблиці
    id = Column(Integer, primary_key=True)  # Первинний ключ
    name = Column(String, nullable=False)  # Текстовий стовпчик
    age = Column(Integer)  # Числовий стовпчик

# Створення таблиці у базі
Base.metadata.create_all(engine)
```

---

### Робота з сесією

Сесія використовується для виконання CRUD-операцій (створення, читання, оновлення, видалення).

1. **Створення сесії**

```python
Session = sessionmaker(bind=engine)
session = Session()
```

2. **Додавання даних**

```python
new_user = User(name="Alice", age=25)  # Створення об'єкта
session.add(new_user)  # Додавання об'єкта до сесії
session.commit()  # Підтвердження змін
```

3. **Додавання кількох записів**

```python
users = [
    User(name="Bob", age=30),
    User(name="Charlie", age=35)
]
session.add_all(users)
session.commit()
```

4. **Отримання даних**

```python
# Всі записи
all_users = session.query(User).all()
for user in all_users:
    print(user.name, user.age)

# Фільтрація
young_users = session.query(User).filter(User.age < 30).all()

# Один запис
user = session.query(User).filter(User.name == "Alice").first()
print(user.name, user.age)
```

5. **Оновлення даних**

```python
user = session.query(User).filter(User.name == "Alice").first()
user.age = 26
session.commit()
```

6. **Видалення даних**

```python
user = session.query(User).filter(User.name == "Bob").first()
session.delete(user)
session.commit()
```

7. **Закриття сесії**

```python
session.close()
```

---

### Зв’язки між таблицями

SQLAlchemy ORM підтримує зв’язки між таблицями: `one-to-many`, `many-to-one`, `many-to-many`.

1. **Приклад зв’язку `one-to-many`**

```python
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    children = relationship("Child", backref="parent")  # Відношення

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'))  # Зовнішній ключ
```

2. **Додавання даних із зв’язком**

```python
parent = Parent(name="John")
child1 = Child(name="Alice", parent=parent)
child2 = Child(name="Bob", parent=parent)

session.add(parent)
session.commit()
```

3. **Отримання даних із зв’язком**

```python
parent = session.query(Parent).filter(Parent.name == "John").first()
for child in parent.children:
    print(child.name)
```

---

### Транзакції в ORM

SQLAlchemy ORM автоматично керує транзакціями. Але ви можете вручну керувати ними:

```python
try:
    new_user = User(name="Dave", age=40)
    session.add(new_user)
    session.commit()  # Підтвердження
except:
    session.rollback()  # Скасування змін у разі помилки
    raise
finally:
    session.close()
```

---

### Основні переваги SQLAlchemy ORM

1. **Абстракція**: Робота з таблицями через Python-класи.
2. **Простота**: Мінімум прямого SQL-коду.
3. **Гнучкість**: Підтримка зв’язків між таблицями.
4. **Масштабованість**: Підходить як для простих проектів, так і для складних.
