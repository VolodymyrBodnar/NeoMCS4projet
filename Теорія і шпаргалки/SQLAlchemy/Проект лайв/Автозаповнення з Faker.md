
### **Інсталяція бібліотеки Faker**

Якщо `Faker` ще не встановлений:

```bash
pip install faker
```

---

### **Код для генерації фейкових даних**

```python
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
from datetime import datetime, timedelta
from app.models import User, Resource, Booking
from app.database import SessionLocal

# Ініціалізація Faker
faker = Faker()

def generate_fake_data(db: Session, num_users=10, num_resources=5, num_bookings=20):
    try:
        # Початок транзакції
        with db.begin():
            # Генерація користувачів
            users = []
            for _ in range(num_users):
                user = User(
                    name=faker.name(),
                    email=faker.unique.email(),
                    created_at=datetime.utcnow(),
                )
                db.add(user)
                users.append(user)

            # Генерація ресурсів
            resources = []
            for _ in range(num_resources):
                resource = Resource(
                    name=faker.word().capitalize(),
                    description=faker.sentence(),
                )
                db.add(resource)
                resources.append(resource)

            db.flush()  # Зберегти зміни для доступу до `id` об'єктів

            # Генерація бронювань
            for _ in range(num_bookings):
                user = faker.random.choice(users)
                resource = faker.random.choice(resources)

                start_time = faker.date_time_this_month()
                end_time = start_time + timedelta(hours=faker.random_int(min=1, max=5))

                booking = Booking(
                    user_id=user.id,
                    resource_id=resource.id,
                    start_time=start_time,
                    end_time=end_time,
                    created_at=datetime.utcnow(),
                )
                db.add(booking)

        # Підтвердження транзакції
        db.commit()
        print("Fake data successfully added to the database.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Transaction failed: {str(e)}")

# Виконання функції
if __name__ == "__main__":
    db = SessionLocal()
    try:
        generate_fake_data(db)
    finally:
        db.close()
```

---

### **Пояснення коду**

1. **Користувачі (`User`):**
    
    - Використовуються методи Faker для генерації випадкових імен (`name`) та унікальних email-адрес (`unique.email`).
    - Додаються в базу в межах транзакції.
2. **Ресурси (`Resource`):**
    
    - Генерується випадкова назва ресурсу (`word`) та опис (`sentence`).
3. **Бронювання (`Booking`):**
    
    - Випадковий користувач та ресурс обираються для кожного бронювання.
    - Генеруються `start_time` та `end_time` із часовим інтервалом 1–5 годин.
4. **Транзакції:**
    
    - Усі операції виконуються в межах однієї транзакції (`with db.begin()`).
    - Якщо виникає помилка, транзакція відкочується (`db.rollback()`).
5. **`db.flush()`:**
    
    - Зберігає зміни в базі, дозволяючи отримати `id` для створених об'єктів (користувачів і ресурсів), які потрібні для бронювань.

---