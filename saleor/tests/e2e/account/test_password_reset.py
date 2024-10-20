import pytest
from ..utils import password_reset_request, password_reset_confirm

@pytest.mark.e2e
def test_password_reset_flow(e2e_not_logged_api_client, e2e_staff_api_client, shop_permissions):
    # Подготовка
    permissions = shop_permissions
    assign_permissions(e2e_staff_api_client, permissions)
    
    # Данные для теста
    test_email = "test-user@saleor.io"
    test_password = "initialpassword"
    new_password = "newsecurepassword"
    channel_slug = "default-channel"
    
    # Создание пользователя
    account_register(e2e_not_logged_api_client, test_email, test_password, channel_slug)
    
    # Шаг 1 - Запрос на сброс пароля
    reset_request = password_reset_request(e2e_not_logged_api_client, test_email)
    assert reset_request["status"] == "ok", "Не удалось запросить сброс пароля"
    
    # Шаг 2 - Получение токена для сброса пароля
    reset_token = reset_request["token"]
    
    # Шаг 3 - Подтверждение сброса пароля
    reset_confirm = password_reset_confirm(e2e_not_logged_api_client, test_email, new_password, reset_token)
    assert reset_confirm["status"] == "ok", "Не удалось сбросить пароль"
    
    # Шаг 4 - Аутентификация с новым паролем
    login_data = token_create(e2e_not_logged_api_client, test_email, new_password)
    assert login_data["user"]["email"] == test_email, "Не удалось аутентифицироваться с новым паролем"