import pytest

from app.scheemas.resources import ResourceDetail, ResourceCreate
from app.scheemas.user import AuthenticatedUser, UserDetail
from app.dependencies.auth import create_access_token

from fastapi.testclient import TestClient
from app.main import app


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db_session  # Імпортуємо вашу базу моделей
from app.main import app

# Створюємо тестову БД у пам’яті
TEST_DATABASE_URL = "sqlite:///:memory:"

# Створюємо engine та сесію для тестів
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    """Створює і очищує тестову базу"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    """Тестова сесія БД"""
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()

# Підміняємо залежність get_db на тестову БД
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()

    app.dependency_overrides[get_db_session] = override_get_db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def client_admin(client: TestClient):
    """
    Fixture that returns a TestClient with superuser authentication headers.
    It also creates a user in DB.
    """
    user_data =  {"name": "test", "role": "ADMIN"}
    # user = AuthenticatedUser(role="ADMIN", name='test')
    access_token: str = create_access_token(user_data)
    headers = {"Authorization": f"Bearer {access_token}"}
    # Modify the client to automatically include the superuser headers in each request
    client.headers.update(headers)
    yield client
    # Clean up: Remove the superuser headers after the test
    client.headers.clear()


@pytest.fixture(scope="function")
def client_employee(client: TestClient):
    """
    Fixture that returns a TestClient with superuser authentication headers.
    It also creates a user in DB.
    """
    user_data =  {"name": "test", "role": "EMPLOYEE"}
    # user = AuthenticatedUser(role="ADMIN", name='test')
    access_token: str = create_access_token(user_data)
    headers = {"Authorization": f"Bearer {access_token}"}
    # Modify the client to automatically include the superuser headers in each request
    client.headers.update(headers)
    yield client
    # Clean up: Remove the superuser headers after the test
    client.headers.clear()



@pytest.fixture
def admin_user():
    return AuthenticatedUser(role="ADMIN", name='test')


@pytest.fixture
def emplyee():
    return AuthenticatedUser(role="EMPLOYEE", name='test')


@pytest.fixture
def resource_new():
    return ResourceCreate(name="test monitor", description="our test moitor")


@pytest.fixture
def resource(resource_new):
    return ResourceDetail(id=12, name=resource_new.name, description=resource_new.description)

@pytest.fixture
def admin_user_detail():
    return UserDetail(name="test_user", role="ADMIN", id=12, password="pass23", email='tst@mail.com')


