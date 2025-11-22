from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from app.bill import BillCommands, BillQueries


@pytest.mark.asyncio
async def test_get_all_bills_with_offset_and_limit(monkeypatch):
    user_id = uuid4()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.offset.return_value.limit.return_value.all.return_value = [
        "bill1",
        "bill2",
    ]
    monkeypatch.setattr("app.bill.BillORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_all_bills(user_id, offset=1, limit=2)
    assert result == ["bill1", "bill2"]


@pytest.mark.asyncio
async def test_get_all_bills_with_limit(monkeypatch):
    user_id = uuid4()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.limit.return_value.all.return_value = ["bill1"]
    monkeypatch.setattr("app.bill.BillORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_all_bills(user_id, limit=1)
    assert result == ["bill1"]


@pytest.mark.asyncio
async def test_get_all_bills_with_offset(monkeypatch):
    user_id = uuid4()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.offset.return_value.all.return_value = ["bill2"]
    monkeypatch.setattr("app.bill.BillORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_all_bills(user_id, offset=1)
    assert result == ["bill2"]


@pytest.mark.asyncio
async def test_get_all_bills_default(monkeypatch):
    user_id = uuid4()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = ["bill1", "bill2", "bill3"]
    monkeypatch.setattr("app.bill.BillORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_all_bills(user_id)
    assert result == ["bill1", "bill2", "bill3"]


@pytest.mark.asyncio
async def test_get_bill(monkeypatch):
    bill_id = uuid4()
    mock_query = MagicMock()
    mock_query.get.return_value = "bill"
    monkeypatch.setattr("app.bill.BillORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_bill(bill_id)
    assert result == "bill"


@pytest.mark.asyncio
async def test_get_uncategorized_goods_no_cat(monkeypatch):
    bill_id = uuid4()
    user_id = uuid4()
    mock_goods = MagicMock()
    mock_goods.categories = []
    mock_goods2 = MagicMock()
    mock_goods2.categories = ["cat"]
    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = [mock_goods, mock_goods2]
    monkeypatch.setattr("app.bill.GoodsORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_uncategorized_goods(bill_id, user_id)
    assert mock_goods in result
    assert mock_goods2 not in result


@pytest.mark.asyncio
async def test_get_uncategorized_goods_with_cat(monkeypatch):
    bill_id = uuid4()
    user_id = uuid4()
    cat_id = uuid4()
    mock_cat = MagicMock(id=cat_id)
    mock_goods = MagicMock()
    mock_goods.categories = [mock_cat]
    mock_goods2 = MagicMock()
    mock_goods2.categories = []
    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = [mock_goods, mock_goods2]
    monkeypatch.setattr("app.bill.GoodsORM", MagicMock(query=mock_query))
    queries = BillQueries()
    result = await queries.get_uncategorized_goods(bill_id, user_id, cat_id)
    assert mock_goods2 in result
    assert mock_goods not in result


@pytest.mark.asyncio
async def test_get_uncategorized_product_no_cat(monkeypatch):
    bill_id = uuid4()
    user_id = uuid4()
    mock_result = [("id1", "prod1")]
    mock_db_session = MagicMock()
    mock_db_session.execute.return_value = mock_result
    monkeypatch.setattr("app.bill.db_session", mock_db_session)
    queries = BillQueries()
    result = await queries.get_uncategorized_product(bill_id, user_id)
    assert result == mock_result


@pytest.mark.asyncio
async def test_get_uncategorized_product_with_cat(monkeypatch):
    bill_id = uuid4()
    user_id = uuid4()
    cat_id = uuid4()
    mock_result = [("id2", "prod2")]
    mock_db_session = MagicMock()
    mock_db_session.execute.return_value = mock_result
    monkeypatch.setattr("app.bill.db_session", mock_db_session)
    queries = BillQueries()
    result = await queries.get_uncategorized_product(bill_id, user_id, cat_id)
    assert result == mock_result


@pytest.mark.asyncio
async def test_get_month_summ(monkeypatch):
    user_id = uuid4()
    mock_result = [MagicMock(summ=Decimal("123.45"))]
    monkeypatch.setattr(
        "app.bill.get_fisrt_day_month_by_delta_month", lambda x: "2024-01-01"
    )
    monkeypatch.setattr(
        "app.bill.get_last_day_of_month_by_datetime", lambda x: "2024-01-31"
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = mock_result
    mock_db_session = MagicMock()
    mock_db_session.query.return_value = mock_query
    monkeypatch.setattr("app.bill.db_session", mock_db_session)
    queries = BillQueries()
    result = await queries.get_month_summ(user_id, 0)
    assert result == Decimal("123.45")


def test_get_params_from_income_url():
    url = "https://mapr.tax.gov.me/ic?iic=123&tin=456&crtd=2024-01-01%2020%3A00%3A00"
    commands = BillCommands()
    params = commands.get_params_from_income_url(url)
    assert params["iic"] == "123"
    assert params["tin"] == "456"
    assert params["crtd"] == "2024-01-01 20:00:00"


def test_validate_url_success(monkeypatch):
    commands = BillCommands()
    url = "https://mapr.tax.gov.me/ic?verify?#"
    monkeypatch.setattr("app.bill.metric_validated_bill", lambda status: None)
    assert commands.validate_url(url) is True


def test_validate_url_failure(monkeypatch):
    commands = BillCommands()
    url = "https://wrong.url"
    monkeypatch.setattr("app.bill.metric_validated_bill", lambda status: None)
    assert commands.validate_url(url) is False


@pytest.mark.asyncio
async def test_get_data_from_fiscal_api_success(monkeypatch):
    commands = BillCommands()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"seller": {"name": "Test", "address": "", "town": ""}, "items": [], "paymentMethod": [{"type": "cash"}], "dateTimeCreated": "2024-01-01T00:00:00", "totalPrice": 100}'
    monkeypatch.setattr("app.bill.post", lambda **kwargs: mock_response)
    monkeypatch.setattr("app.bill.metric_call_external_api", lambda **kwargs: None)
    monkeypatch.setattr("app.bill.metric_processed_bill", lambda status: None)
    result = await commands.get_data_from_fiscal_api(
        iic="1", tin="2", crtd="2024-01-01 00:00:00"
    )
    assert result["seller"]["name"] == "Test"
    assert result["totalPrice"] == 100


@pytest.mark.asyncio
async def test_get_data_from_fiscal_api_failure(monkeypatch):
    commands = BillCommands()
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.content = b"{}"
    monkeypatch.setattr("app.bill.post", lambda **kwargs: mock_response)
    monkeypatch.setattr("app.bill.metric_call_external_api", lambda **kwargs: None)
    monkeypatch.setattr("app.bill.metric_processed_bill", lambda status: None)
    result = await commands.get_data_from_fiscal_api(
        iic="1", tin="2", crtd="2024-01-01 00:00:00"
    )
    assert result is None


def test_get_total_summ():
    commands = BillCommands()
    user_id = uuid4()
    result = commands.get_total_summ(user_id)
    assert result == 1700.0
