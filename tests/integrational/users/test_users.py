from unittest.mock import patch

def test_api_with_different_users(client, admin_user_detail):
    user = {"name": "name23", "password": "pass23"}
    with patch("app.services.user.get_user_from_db_by_name") as mock_repo:
        mock_repo.return_value = admin_user_detail
        # 1. Логін користувача 
        with patch("app.services.user.salted_hash") as mock_hash:
            mock_hash.return_value = "pass23"
            login_response = client.post("/login", json=user)

            assert login_response.status_code == 200
            token = login_response.json().get("token")
            assert token is not None
            print(token)
