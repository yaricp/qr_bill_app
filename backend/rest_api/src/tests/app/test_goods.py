import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from src.app.goods import GoodsQueries, GoodsCommands, GoodsORM, CategoryORM


@pytest.mark.asyncio
async def test_get_all_goods_variants():
    user_id = uuid4()
    mock_goods = [MagicMock(), MagicMock()]

    # 1. limit > 0 and offset > 0
    with patch.object(GoodsORM.query.filter_by(user_id=user_id), 'offset') as offset_mock:
        offset_chain = offset_mock.return_value.limit.return_value
        offset_chain.all.return_value = mock_goods
        gq = GoodsQueries()
        result = await gq.get_all_goods(user_id=user_id, offset=1, limit=2)
        assert result == mock_goods

    # 2. limit > 0 and offset = 0
    with patch.object(GoodsORM.query.filter_by(user_id=user_id), 'limit') as limit_mock:
        limit_mock.return_value.all.return_value = mock_goods
        result = await gq.get_all_goods(user_id=user_id, offset=0, limit=1)
        assert result == mock_goods

    # 3. limit = 0 and offset > 0
    with patch.object(GoodsORM.query.filter_by(user_id=user_id), 'offset') as offset_mock2:
        offset_mock2.return_value.all.return_value = mock_goods
        result = await gq.get_all_goods(user_id=user_id, offset=1, limit=0)
        assert result == mock_goods

    # 4. limit = 0 and offset = 0
    with patch.object(GoodsORM.query.filter_by(user_id=user_id), 'all') as all_mock:
        all_mock.return_value = mock_goods
        result = await gq.get_all_goods(user_id=user_id, offset=0, limit=0)
        assert result == mock_goods


@pytest.mark.asyncio
async def test_get_goods():
    goods_id = uuid4()
    goods_mock = MagicMock()
    with patch.object(GoodsORM.query, 'get', return_value=goods_mock):
        gq = GoodsQueries()
        result = await gq.get_goods(goods_id)
        assert result == goods_mock


@pytest.mark.asyncio
async def test_list_count_group_by_name_variants():
    user_id = uuid4()
    mock_result = [("item1", 5)]

    # first_of > 0 -> limit
    with patch("src.app.goods.db_session.query") as query_mock:
        chain = query_mock.return_value.where.return_value.group_by.return_value.order_by.return_value.limit.return_value
        chain = chain
        chain = MagicMock()
        chain = mock_result
        gq = GoodsQueries()
        with patch("src.app.goods.db_session.query") as q:
            q.return_value.where.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_result
            result = await gq.list_count_group_by_name(user_id=user_id, first_of=3)
            assert result == mock_result

    # first_of = 0 -> all
    with patch("src.app.goods.db_session.query") as q2:
        q2.return_value.where.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result
        result = await gq.list_count_group_by_name(user_id=user_id, first_of=0)
        assert result == mock_result


@pytest.mark.asyncio
async def test_list_summ_group_by_name_variants():
    user_id = uuid4()
    mock_result = [("item1", 123.45)]

    # first_of > 0 -> limit
    with patch("src.app.goods.db_session.query") as query_mock:
        query_mock.return_value.where.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_result
        gq = GoodsQueries()
        result = await gq.list_summ_group_by_name(user_id=user_id, first_of=3)
        assert result == mock_result

    # first_of = 0 -> all
    with patch("src.app.goods.db_session.query") as query_mock:
        query_mock.return_value.where.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result
        result = await gq.list_summ_group_by_name(user_id=user_id, first_of=0)
        assert result == mock_result

@pytest.mark.asyncio
async def test_goods_by_name_group_by_sellers():
    user_id = uuid4()
    name = "item1"
    mock_result = [("seller1", 10)]
    with patch("src.app.goods.GoodsORM.query") as q:
        q.return_value.join.return_value.where.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_result
        gq = GoodsQueries()
        result = await gq.goods_by_name_group_by_sellers(name=name, user_id=user_id)
        assert result == mock_result

@pytest.mark.asyncio
async def test_list_uncategorized_goods():
    user_id = uuid4()
    cat_id = uuid4()
    goods1 = MagicMock(categories=[])
    goods2 = MagicMock(categories=[MagicMock(id=cat_id)])
    with patch.object(GoodsORM.query, 'filter_by', return_value=MagicMock(all=lambda: [goods1, goods2])):
        gq = GoodsQueries()
        # cat_id is None
        result = await gq.list_uncategorized_goods(user_id=user_id)
        assert goods1 in result and goods2 not in result
        # cat_id provided
        result2 = await gq.list_uncategorized_goods(user_id=user_id, cat_id=cat_id)
        assert goods1 in result2 and goods2 not in result2

@pytest.mark.asyncio
async def test_get_or_create_goods_commands_branches():
    gcmd = GoodsCommands()
    incoming_item = MagicMock(fiscal_id="123")
    goods_mock = MagicMock()
    # branch 1: fiscal_id exists
    gcmd.get_goods_by_fiscal_id = lambda x: goods_mock
    result = await gcmd.get_or_create(incoming_item)
    assert result == goods_mock

    # branch 2: no fiscal_id, found by name/quantity/summ
    incoming_item.fiscal_id = None
    gcmd.get_goods_by_fiscal_id = lambda x: None
    gcmd.get_goods_by_name_quantity_summ = lambda x: goods_mock
    gcmd.get_by_name_bill_id_with_empty_fiscal_id = lambda x: None
    gcmd.create_goods = lambda x: MagicMock()
    result = await gcmd.get_or_create(incoming_item)
    assert result == goods_mock

    # branch 3: not found, create new
    gcmd.get_goods_by_fiscal_id = lambda x: None
    gcmd.get_goods_by_name_quantity_summ = lambda x: None
    gcmd.get_by_name_bill_id_with_empty_fiscal_id = lambda x: None
    new_goods = MagicMock()
    gcmd.create_goods = lambda x: new_goods
    result = await gcmd.get_or_create(incoming_item)
    assert result == new_goods

@pytest.mark.asyncio
async def test_create_update_goods_commands():
    gcmd = GoodsCommands()
    incoming_item = MagicMock()
    with patch("src.app.goods.db_session.add") as add_mock, \
         patch("src.app.goods.db_session.commit") as commit_mock:
        # create_goods
        result = await gcmd.create_goods(incoming_item)
        add_mock.assert_called()
        commit_mock.assert_called()
        # update_goods
        goods_mock = MagicMock()
        with patch.object(GoodsORM.query, 'get', return_value=goods_mock):
            result2 = await gcmd.update_goods(incoming_item)
            assert goods_mock == result2

@pytest.mark.asyncio
async def test_update_goods_categories_success_and_fail():
    gcmd = GoodsCommands()
    goods_mock = MagicMock(categories=set())
    cat_mock = MagicMock()
    with patch.object(GoodsORM.query, 'get', return_value=goods_mock), \
         patch.object(CategoryORM, 'query', MagicMock(get=lambda x: cat_mock)), \
         patch("src.app.goods.db_session.add"), \
         patch("src.app.goods.db_session.commit"):
        result = await gcmd.update_goods_categories(goods_id=uuid4(), goods_data=[MagicMock(cat_id=uuid4())])
        assert result is True

    with patch.object(GoodsORM.query, 'get', return_value=goods_mock), \
         patch.object(CategoryORM, 'query', MagicMock(get=lambda x: cat_mock)), \
         patch("src.app.goods.db_session.add", side_effect=Exception), \
         patch("src.app.goods.db_session.commit", side_effect=Exception):
        result2 = await gcmd.update_goods_categories(goods_id=uuid4(), goods_data=[MagicMock(cat_id=uuid4())])
        assert result2 is False

@pytest.mark.asyncio
async def test_save_categorized_goods_success_and_fail():
    gcmd = GoodsCommands()
    goods_mock = MagicMock(categories=set())
    cat_mock = MagicMock()
    data = [MagicMock(goods_id=uuid4(), cat_id=uuid4())]

    with patch.object(GoodsORM.query, 'get', return_value=goods_mock), \
         patch.object(CategoryORM, 'query', MagicMock(get=lambda x: cat_mock)), \
         patch("src.app.goods.db_session.commit"):
        result = await gcmd.save_categorized_goods(data)
        assert result is True

    with patch.object(GoodsORM.query, 'get', side_effect=Exception):
        result2 = await gcmd.save_categorized_goods(data)
        assert result2 is False

@pytest.mark.asyncio
async def test_strip_all_names_calls_update_goods():
    gcmd = GoodsCommands()
    goods_list = [MagicMock(id=uuid4(), name="  item  ")]
    with patch.object(GoodsORM.query, 'all', return_value=goods_list), \
         patch.object(GoodsCommands, 'update_goods', return_value=MagicMock()):
        result = await gcmd.strip_all_names()
        assert result is True

