from app.services.resources import create_item
from unittest.mock import patch


def test_demo_resource(resource):
    assert resource.name == "test monitor"


def test_create_item(resource_new):
    with patch("app.services.resources.create_new") as mock:
        mock.return_value = "TEST"
        mock_db = {}
        create_item(resource_new, mock_db)
        args, _ = mock.call_args
        result = args[0]
    assert "UUID" in result.description



def test_create_item_frequent_error(resource_new):
    # EXAMPLE OF USELESS TEST (IT TESTS ITSELF)
    with patch("app.services.resources.create_new") as mock:
        test_data = resource_new
        test_data.description = f"{test_data}, UUID: dkashdjkahsjkdhas"
        mock.return_value = test_data 
        mock_db = {}
        result = create_item(resource_new, mock_db)
    assert "UUID" in result.description


