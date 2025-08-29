from sqlalchemy.orm import Session
from uuid import uuid4
from loguru import logger

# Примерная модель для вставки тестовых данных (замени на реальные модели, если нужно)
from src.infra.database.models import (
    Bill, Seller, User
)  # Убедись, что у тебя есть такие модели в проекте


def create_test_data(db_session: Session):
    """Функция для добавления тестовых данных в БД"""
    seller_id = str(uuid4())
    bill_id = str(uuid4())

    test_user = User.query.filter_by(login="test_user").first()

    # Добавляем продавца
    seller = Seller(
        id=seller_id,
        name="Test Seller",
        official_name="Official Seller One",
        address="123 Test St",
        city="Test City"
    )
    db_session.add(seller)

    # Добавляем счет
    bill = Bill(
        id=bill_id,
        created="2023-01-01T12:00:00",
        value="100.50",
        seller_id=seller_id,
        user_id=test_user.id
    )
    db_session.add(bill)

    db_session.commit()
    return bill_id, seller_id


def test_get_all_bills(test_client, auth_headers, db_session):
    """Тест получения всех счетов"""
    bill_id, seller_id = create_test_data(db_session)  # Добавляем тестовые данные

    bill_db = Bill.query.get(bill_id)

    logger.info(f"bill_db: {bill_db}")

    seller_db = Seller.query.get(seller_id)

    logger.info(f"seller_db: {seller_db}")
    
    response = test_client.get("/api/v1/bills/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_create_bill(test_client, auth_headers, db_session):
    """Тест создания нового счета"""
    _, seller_id = create_test_data(db_session)  # Добавляем тестовые данные

    user = User.query.filter_by(login="test_user").first()

    data = {
        "created": "2023-01-01T12:00:00",
        "value": "200.75",
        "seller_id": seller_id,
        "user_id": str(user.id)
    }

    response = test_client.post("/api/v1/bills/", json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["value"] == data["value"]


def test_get_bill_by_id(test_client, auth_headers, db_session):
    """Тест получения счета по ID"""
    bill_id, _ = create_test_data(db_session)  # Добавляем тестовые данные

    response = test_client.get(f"/api/v1/bills/{bill_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == bill_id


def test_update_bill(test_client, auth_headers, db_session):
    """Тест обновления счета"""
    bill_id, _ = create_test_data(db_session)  # Добавляем тестовые данные
    
    update_data = {"value": "300.99"}
    response = test_client.put(f"/api/v1/bills/{bill_id}", json=update_data, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["value"] == update_data["value"]


def test_delete_bill(test_client, auth_headers, db_session):
    """Тест удаления счета"""
    bill_id, _ = create_test_data(db_session)  # Добавляем тестовые данные

    response = test_client.delete(f"/api/v1/bills/{bill_id}", headers=auth_headers)
    assert response.status_code == 200

    # Проверяем, что удаленного счета больше нет
    response = test_client.get(f"/api/v1/bills/{bill_id}", headers=auth_headers)
    assert response.status_code == 404


def test_parse_url_bill(test_client, auth_headers):
    """Тест парсинга ссылки на счет"""
    data = {"link": "https://mapr.tax.gov.me/ic/#/verify?iic=B1EEF0F469C52D9B26E869841CB73700&tin=03224678&crtd=2024-12-28T17:10:14%2001:00&ord=68288&bu=oj275xi131&cr=bu831zx287&sw=on241rl293&prc=36.80"}
    response = test_client.post(
        "/api/v1/bills/parse_url/", json=data, headers=auth_headers
    )

    assert response.status_code in [200, 422]  # 422, если ссылка недействительная
    if response.status_code == 200:
        assert "id" in response.json()
        assert "created" in response.json()
        assert response.json()["created"] == "2024-12-28 16:10:14"
        assert "seller" in response.json()
        assert response.json()["seller"] == {"name": '"GUŠTI" D.O.O.', 'address': 'NJEGOŠEVA BR.139(C-VRAČAR) - H. NOVI'}
        assert "summ" in response.json()
        assert response.json()["summ"] == 36.8

    data = {"link": "https://mar"}
    response = test_client.post(
        "/api/v1/bills/parse_url/", json=data, headers=auth_headers
    )
    assert response.status_code == 422


def test_get_uncategorized_goods(test_client, auth_headers, db_session):
    """Тест получения некатегоризированных товаров"""
    bill_id, _ = create_test_data(db_session)

    response = test_client.get(
        f"/api/v1/bills/{bill_id}/uncategorized_goods/",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_uncategorized_goods_by_category(
    test_client, auth_headers, db_session
):
    """Тест получения некатегоризированных товаров по `bill_id` и `cat_id`"""
    bill_id, _ = create_test_data(db_session)
    cat_id = str(uuid4())

    response = test_client.get(f"/api/v1/bills/{bill_id}/uncategorized_goods/{cat_id}", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_uncategorized_products(test_client, auth_headers, db):
    """Тест получения некатегоризированных продуктов"""
    bill_id, _ = create_test_data(db)

    response = test_client.get(
        f"/api/v1/bills/{bill_id}/uncategorized_products/",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_uncategorized_products_by_category(test_client, auth_headers, db):
    """Тест получения некатегоризированных продуктов по `bill_id` и `cat_id`"""
    bill_id, _ = create_test_data(db)
    cat_id = str(uuid4())

    response = test_client.get(f"/api/v1/bills/{bill_id}/uncategorized_products/{cat_id}", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_month_summary(test_client, auth_headers):
    """Тест получения суммы счетов за определенное количество месяцев"""
    delta_month = 3
    response = test_client.get(
        f"/api/v1/bills/month_summ/{delta_month}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), str)  # Ожидается строка (как в OpenAPI)
