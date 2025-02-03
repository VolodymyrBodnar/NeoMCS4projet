import pytest

from unittest.mock import patch
from fastapi.exceptions import HTTPException


def test_create_new(client_admin, resource_new):
    data = {
        "name": "monitor",
        "description": "description of a monitor"
    }
    with patch('app.services.resources.create_new') as mock_repo:
        mock_repo.return_value = resource_new
        result = client_admin.post('/resources',json=data)
        assert result.status_code == 200

def test_create_new_with_employee_returns_401(client_employee, resource_new):
    data = {
        "name": "monitor",
        "description": "description of a monitor"
    }
    with patch('app.services.resources.create_new') as mock_repo:
        mock_repo.return_value = resource_new
        result = client_employee.post('/resources',json=data)
        assert result.status_code == 401


def test_create_new_no_auth_returns_401(client, resource_new):
    data = {
        "name": "monitor",
        "description": "description of a monitor"
    }
    with patch('app.services.resources.create_new') as mock_repo:
        mock_repo.return_value = resource_new
        result = client.post('/resources',json=data)
        assert result.status_code == 401


