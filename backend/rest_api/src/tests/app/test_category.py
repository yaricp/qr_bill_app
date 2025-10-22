import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from src.app.category import CategoryQueries, CategoryCommands
from src.app.entities.category import CategoryCreate, CategoryUpdate


# --------------------------
# Fixtures
# --------------------------
@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def category_create(user_id):
    return CategoryCreate(name="Food", user_id=user_id)


@pytest.fixture
def category_update(user_id):
    return CategoryUpdate(id=uuid4(), name="Drinks", user_id=user_id)


@pytest.fixture
def mock_category():
    cat = MagicMock()
    cat.name = "Food"
    return cat


# --------------------------
# CategoryQueries Tests
# --------------------------
@pytest.mark.asyncio
async def test_get_all_categories(user_id, mock_category):
    with patch("src.app.category.CategoryORM.query") as query_mock:
        query_mock.filter_by.return_value.all.return_value = [mock_category]
        cq = CategoryQueries()
        result = await cq.get_all_categories(user_id=user_id)
        assert result == [mock_category]


@pytest.mark.asyncio
async def test_get_category(user_id, mock_category):
    with patch("src.app.category.CategoryORM.query") as query_mock:
        query_mock.filter_by.return_value.first.return_value = mock_category
        cq = CategoryQueries()
        result = await cq.get_category(id=uuid4(), user_id=user_id)
        assert result == mock_category


@pytest.mark.asyncio
async def test_count_goods_by_name_A1(user_id=uuid4()):
    """first_of > 0, delta_month != 1"""
    mock_result = [("cat1", 10)]
    with patch("src.app.category.db_session.query") as query_mock, \
         patch("src.app.category.get_fisrt_day_month_by_delta_month", return_value="2025-10-01"), \
         patch("src.app.category.get_last_day_of_month_by_datetime", return_value="2025-10-31"):

        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.count_goods_by_name(first_of=5, user_id=user_id, delta_month=-1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_count_goods_by_name_A2(user_id=uuid4()):
    """first_of > 0, delta_month == 1"""
    mock_result = [("cat2", 20)]
    with patch("src.app.category.db_session.query") as query_mock:

        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.count_goods_by_name(first_of=3, user_id=user_id, delta_month=1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_count_goods_by_name_B1(user_id=uuid4()):
    """first_of=None, delta_month != 1"""
    mock_result = [("cat3", 30)]
    with patch("src.app.category.db_session.query") as query_mock, \
         patch("src.app.category.get_fisrt_day_month_by_delta_month", return_value="2025-09-01"), \
         patch("src.app.category.get_last_day_of_month_by_datetime", return_value="2025-09-30"):

        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.count_goods_by_name(first_of=None, user_id=user_id, delta_month=-1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_count_goods_by_name_B2(user_id=uuid4()):
    """first_of=None, delta_month == 1"""
    mock_result = [("cat4", 40)]
    with patch("src.app.category.db_session.query") as query_mock:

        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.count_goods_by_name(first_of=None, user_id=user_id, delta_month=1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_summ_goods_by_name_A1(user_id=uuid4()):
    """first_of > 0, delta_month != 1"""
    mock_result = [("cat1", 10)]
    with patch("src.app.category.db_session.query") as query_mock, \
         patch("src.app.category.get_fisrt_day_month_by_delta_month", return_value="2025-10-01"), \
         patch("src.app.category.get_last_day_of_month_by_datetime", return_value="2025-10-31"):
        
        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.summ_goods_by_name(first_of=5, user_id=user_id, delta_month=-1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_summ_goods_by_name_A2(user_id=uuid4()):
    """first_of > 0, delta_month == 1"""
    mock_result = [("cat2", 20)]
    with patch("src.app.category.db_session.query") as query_mock:
        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.summ_goods_by_name(first_of=3, user_id=user_id, delta_month=1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_summ_goods_by_name_B1(user_id=uuid4()):
    """first_of=None, delta_month != 1"""
    mock_result = [("cat3", 30)]
    with patch("src.app.category.db_session.query") as query_mock, \
         patch("src.app.category.get_fisrt_day_month_by_delta_month", return_value="2025-09-01"), \
         patch("src.app.category.get_last_day_of_month_by_datetime", return_value="2025-09-30"):

        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.summ_goods_by_name(first_of=None, user_id=user_id, delta_month=-1)
        assert result == mock_result


@pytest.mark.asyncio
async def test_summ_goods_by_name_B2(user_id=uuid4()):
    """first_of=None, delta_month == 1"""
    mock_result = [("cat4", 40)]
    with patch("src.app.category.db_session.query") as query_mock:

        chain = query_mock.return_value.join.return_value.join.return_value.join.return_value
        chain.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result

        cq = CategoryQueries()
        result = await cq.summ_goods_by_name(first_of=None, user_id=user_id, delta_month=1)
        assert result == mock_result


# --------------------------
# CategoryCommands Tests
# --------------------------
@pytest.mark.asyncio
async def test_create_category(category_create):
    mock_cat = MagicMock()
    with patch("src.app.category.db_session.add") as add_mock, \
         patch("src.app.category.db_session.commit") as commit_mock, \
         patch("src.app.category.CategoryORM", return_value=mock_cat):

        cc = CategoryCommands()
        result = await cc.create_category(incoming_item=category_create)
        add_mock.assert_called_once_with(mock_cat)
        commit_mock.assert_called_once()
        assert result == mock_cat


@pytest.mark.asyncio
async def test_get_by_name(category_create, mock_category):
    with patch("src.app.category.CategoryORM.query") as query_mock:
        query_mock.filter.return_value.first.return_value = mock_category
        cc = CategoryCommands()
        result = await cc.get_by_name(category_create)
        assert result == mock_category


@pytest.mark.asyncio
async def test_get_or_create_existing(category_create, mock_category):
    cc = CategoryCommands()
    cc.get_by_name = AsyncMock(return_value=mock_category)
    cc.create_category = AsyncMock()
    result = await cc.get_or_create(category_create, user_id=uuid4())
    cc.create_category.assert_not_called()
    assert result == mock_category


@pytest.mark.asyncio
async def test_get_or_create_create_new(category_create, mock_category):
    cc = CategoryCommands()
    cc.get_by_name = AsyncMock(return_value=None)
    cc.create_category = AsyncMock(return_value=mock_category)
    result = await cc.get_or_create(category_create, user_id=uuid4())
    cc.create_category.assert_called_once()
    assert result == mock_category


@pytest.mark.asyncio
async def test_update_category(category_update, mock_category):
    with patch("src.app.category.CategoryORM.query") as query_mock:
        query_mock.get.return_value = mock_category
        with patch("src.app.category.db_session.commit") as commit_mock:
            cc = CategoryCommands()
            result = await cc.update_category(category_update)
            assert mock_category.name == "Drinks"
            commit_mock.assert_called_once()
            assert result == mock_category


@pytest.mark.asyncio
async def test_delete_category(mock_category):
    with patch("src.app.category.CategoryORM.query") as query_mock, \
         patch("src.app.category.db_session.delete") as delete_mock, \
         patch("src.app.category.db_session.commit") as commit_mock:
        query_mock.filter_by.return_value.first.return_value = mock_category
        cc = CategoryCommands()
        result = await cc.delete_category(id=uuid4())
        delete_mock.assert_called_once_with(mock_category)
        commit_mock.assert_called_once()
        assert result == mock_category
