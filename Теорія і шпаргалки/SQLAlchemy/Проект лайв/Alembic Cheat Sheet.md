### **Alembic Cheat Sheet**

---

### **Основні Команди**

1. **Ініціалізація Alembic у проекті**
   ```bash
   alembic init migrations
   ```
   Створює папку `migrations` з базовою конфігурацією.

2. **Створення нового файлу міграції**
   ```bash
   alembic revision --autogenerate -m "Опис міграції"
   ```
   Генерує новий файл міграції на основі змін у моделях SQLAlchemy. `--autogenerate` дозволяє Alembic самостійно виявити зміни.

3. **Застосування міграцій до бази даних**
   ```bash
   alembic upgrade head
   ```
   Застосовує всі доступні міграції до актуальної версії.

   Для застосування конкретної версії:
   ```bash
   alembic upgrade <version>
   ```

4. **Відкат міграції**
   ```bash
   alembic downgrade -1
   ```
   Відкочується на одну версію назад.

   Для відкату до конкретної версії:
   ```bash
   alembic downgrade <version>
   ```

5. **Перегляд поточного стану міграцій**
   ```bash
   alembic current
   ```
   Виводить поточну версію, застосовану до бази даних.

6. **Перегляд журналу міграцій**
   ```bash
   alembic history
   ```
   Виводить список усіх доступних міграцій.

7. **Синхронізація бази даних із поточними моделями без створення файлу міграції**
   ```bash
   alembic stamp head
   ```
   Встановлює базу даних на останню версію без виконання реальних змін.

---

### **Основні Секції у Файлах Alembic**

#### **Файл `alembic.ini`**

**`sqlalchemy.url`**  

  URL бази даних, наприклад:
  ```ini
  sqlalchemy.url = sqlite:///./test.db
```
  Для PostgreSQL:
  ```ini
  sqlalchemy.url = postgresql://user:password@localhost/dbname
  ```
- **`script_location`**  
	  Шлях до папки з міграціями (зазвичай `migrations`):
  ```ini
  script_location = migrations
  ```

- **`file_template`**  
  Шаблон іменування файлів міграцій:
  ```ini
  file_template = %%(rev)s_%%(slug)s.py
  ```
  Де `%%(rev)s` — ідентифікатор ревізії, а `%%(slug)s` — опис.

---
```



#### **Файл `env.py`**
Відповідає за зв'язок між Alembic та SQLAlchemy моделями.

- **`target_metadata`**  
  Додає метадані моделей SQLAlchemy:
  ```python
  from app.database import Base
  from app.models import User, Resource, Booking

  target_metadata = Base.metadata
  ```

- **Налаштування підключення до бази даних**
  У `env.py` визначається метод підключення:
  ```python
  connectable = engine_from_config(
      config.get_section(config.config_ini_section),
      prefix='sqlalchemy.',
      poolclass=pool.NullPool,
  )
  ```

- **Ручний запуск**
  Додає змінення в базі під час автоматичного створення міграцій:
  ```python
  context.configure(
      connection=connection,
      target_metadata=target_metadata,
      compare_type=True,  # Враховує зміну типів колонок
  )
  ```

---
