import pytest

from app.scheemas.resources import ResourceDetail, ResourceCreate
from app.scheemas.user import AuthenticatedUser



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



