import pytest
from ..utils import assign_permissions, add_product_to_cart, get_cart
from ..shop.utils import prepare_shop
from ..product.utils import prepare_product

@pytest.mark.e2e
def test_add_product_to_cart_functionality(
    e2e_staff_api_client,
    e2e_app_api_client,
    shop_permissions,
    permission_manage_product_types_and_attributes
):
    # Подготовка
    permissions = [
        permission_manage_product_types_and_attributes,
        *shop_permissions
    ]
    assign_permissions(e2e_staff_api_client, permissions)

    # Подготовка данных магазина и продукта
    shop_data = prepare_shop(e2e_staff_api_client)
    channel_id = shop_data["channel"]["id"]
    warehouse_id = shop_data["warehouse"]["id"]
    channel_slug = shop_data["channel"]["slug"]
    price = 10

    # Создание продукта
    product_data = prepare_product(e2e_staff_api_client, warehouse_id, channel_id, price)
    product_variant_id = product_data["product"]["variants"][0]["id"]

    # Тест добавления продукта в корзину
    lines = [
        {
            "variantId": product_variant_id,
            "quantity": 1,
        },
    ]
    cart_data = add_product_to_cart(e2e_app_api_client, lines, channel_slug)
    assert cart_data is not None, "Корзина не создана"
    assert len(cart_data["lines"]) > 0, "Продукт не добавлен в корзину"
    assert cart_data["lines"][0]["variant"]["id"] == product_variant_id, "Неверный продукт в корзине"

    # Проверка содержимого корзины
    cart = get_cart(e2e_app_api_client)
    assert cart is not None, "Корзина не найдена"
    assert len(cart["lines"]) > 0, "Продукты отсутствуют в корзине"
    assert cart["lines"][0]["variant"]["id"] == product_variant_id, "Продукт в корзине не соответствует ожиданиям"