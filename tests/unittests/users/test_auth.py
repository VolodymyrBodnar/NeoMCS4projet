import pytest
from fastapi.exceptions import HTTPException

from app.dependencies.auth import validate_is_admin_user, validate_is_employee


def test_validate_is_employee(emplyee):
    assert validate_is_employee(emplyee) == emplyee

def test_validate_is_admin_user(emplyee, admin_user):
    assert validate_is_admin_user(admin_user) == admin_user
    with pytest.raises(HTTPException):
        validate_is_admin_user(emplyee)



def calculate_volume(l, w, h):
    volume = l * w * h
    return volume


@pytest.mark.parametrize("l, w, h, expected",[
    (10, 10, 10, 1000),
    (50,30,15, 22500),
    (10, 5, 1, 50)
])
def test_volume(l, w, h, expected):
    assert calculate_volume(l, w, h) == expected