from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from src.app.goods import CategoryORM, GoodsCommands, GoodsORM, GoodsQueries


class TestGoodsQueries:

    @pytest.mark.asyncio
    async def test_get_all_goods_no_pagination(self):
        """Тест без offset и limit"""
        user_id = uuid4()
        expected_goods = [MagicMock(), MagicMock()]
        
        query_mock = MagicMock()
        filter_by_mock = MagicMock()
        filter_by_mock.all.return_value = expected_goods
        query_mock.filter_by.return_value = filter_by_mock
        
        with patch.object(GoodsORM, "query", query_mock):
            gq = GoodsQueries()
            result = await gq.get_all_goods(user_id)

            query_mock.filter_by.assert_called_once_with(user_id=user_id)
            filter_by_mock.all.assert_called_once()
            assert result == expected_goods

    @pytest.mark.asyncio
    async def test_get_all_goods_with_limit_only(self):
        """Тест только с limit"""
        user_id = uuid4()
        limit = 10
        expected_goods = [MagicMock() for _ in range(limit)]
        
        query_mock = MagicMock()
        filter_by_mock = MagicMock()
        limit_mock = MagicMock()
        limit_mock.all.return_value = expected_goods
        filter_by_mock.limit.return_value = limit_mock
        query_mock.filter_by.return_value = filter_by_mock
        
        with patch.object(GoodsORM, "query", query_mock):
            gq = GoodsQueries()
            result = await gq.get_all_goods(user_id, limit=limit)
            
            query_mock.filter_by.assert_called_once_with(user_id=user_id)
            filter_by_mock.limit.assert_called_once_with(limit)
            limit_mock.all.assert_called_once()
            assert result == expected_goods

    @pytest.mark.asyncio
    async def test_get_all_goods_with_offset_only(self):
        """Тест только с offset"""
        user_id = uuid4()
        offset = 5
        expected_goods = [MagicMock(), MagicMock()]
        
        query_mock = MagicMock()
        filter_by_mock = MagicMock()
        offset_mock = MagicMock()
        offset_mock.all.return_value = expected_goods
        filter_by_mock.offset.return_value = offset_mock
        query_mock.filter_by.return_value = filter_by_mock
        
        with patch.object(GoodsORM, "query", query_mock):
            gq = GoodsQueries()
            result = await gq.get_all_goods(user_id, offset=offset)
            
            query_mock.filter_by.assert_called_once_with(user_id=user_id)
            filter_by_mock.offset.assert_called_once_with(offset)
            offset_mock.all.assert_called_once()
            assert result == expected_goods

    @pytest.mark.asyncio
    async def test_get_all_goods_with_limit_and_offset(self):
        """Тест с offset и limit"""
        user_id = uuid4()
        offset = 10
        limit = 5
        expected_goods = [MagicMock() for _ in range(limit)]

        query_mock = MagicMock()
        filter_by_mock = MagicMock()
        offset_mock = MagicMock()
        limit_mock = MagicMock()
        limit_mock.all.return_value = expected_goods
        offset_mock.limit.return_value = limit_mock
        filter_by_mock.offset.return_value = offset_mock
        query_mock.filter_by.return_value = filter_by_mock

        with patch.object(GoodsORM, "query", query_mock):
            gq = GoodsQueries()
            result = await gq.get_all_goods(
                user_id, offset=offset, limit=limit
            )

            query_mock.filter_by.assert_called_once_with(user_id=user_id)
            filter_by_mock.offset.assert_called_once_with(offset)
            offset_mock.limit.assert_called_once_with(limit)
            limit_mock.all.assert_called_once()
            assert result == expected_goods


@pytest.mark.asyncio
async def test_list_count_group_by_name_variants():
    user_id = uuid4()
    mock_result = [("item1", 5)]

    # first_of > 0 -> limit
    with patch("src.app.goods.db_session.query") as query_mock:
        gq = GoodsQueries()
        with patch("src.app.goods.db_session.query") as q:
            q.return_value.where.return_value.group_by.return_value.order_by.return_value.limit.return_value = (
                mock_result
            )
            result = await gq.list_count_group_by_name(user_id=user_id, first_of=3)
            assert result == mock_result

    # first_of = 0 -> all
    with patch("src.app.goods.db_session.query") as q2:
        q2.return_value.where.return_value.group_by.return_value.order_by.return_value.all.return_value = (
            mock_result
        )
        result = await gq.list_count_group_by_name(user_id=user_id, first_of=0)
        assert result == mock_result


@pytest.mark.asyncio
async def test_list_summ_group_by_name_variants():
    user_id = uuid4()
    mock_result = [("item1", 123.45)]

    # first_of > 0 -> limit
    with patch("src.app.goods.db_session.query") as query_mock:
        query_mock.return_value.where.return_value.group_by.return_value.order_by.return_value.limit.return_value = (
            mock_result
        )
        gq = GoodsQueries()
        result = await gq.list_summ_group_by_name(user_id=user_id, first_of=3)
        assert result == mock_result

    # first_of = 0 -> all
    with patch("src.app.goods.db_session.query") as query_mock:
        query_mock.return_value.where.return_value.group_by.return_value.order_by.return_value.all.return_value = (
            mock_result
        )
        result = await gq.list_summ_group_by_name(user_id=user_id, first_of=0)
        assert result == mock_result


@pytest.mark.asyncio
async def test_goods_by_name_group_by_sellers():
    user_id = uuid4()
    name = "item1"
    mock_result = [("seller1", 10)]
    with patch("src.app.goods.GoodsORM.query") as q:
        q.return_value.join.return_value.where.return_value.group_by.return_value.order_by.return_value.all.return_value = (
            mock_result
        )
        gq = GoodsQueries()
        result = await gq.goods_by_name_group_by_sellers(name=name, user_id=user_id)
        assert result == mock_result


@pytest.mark.asyncio
async def test_list_uncategorized_goods():
    user_id = uuid4()
    cat_id = uuid4()

    goods1 = MagicMock(categories=[])
    goods2 = MagicMock(categories=[MagicMock(id=cat_id)])
    goods3 = MagicMock(categories=[MagicMock(id=uuid4())])

    query_mock = MagicMock()
    filter_by_mock = MagicMock()
    filter_by_mock.all.return_value = [goods1, goods2, goods3]
    query_mock.filter_by.return_value = filter_by_mock

    with patch.object(GoodsORM, "query", query_mock):
        gq = GoodsQueries()

        result = await gq.list_uncategorized_goods(user_id=user_id)

        query_mock.filter_by.assert_called_with(user_id=user_id)
        assert goods1 in result
        assert goods2 not in result
        assert goods3 not in result
        assert len(result) == 1

        result2 = await gq.list_uncategorized_goods(
            user_id=user_id, cat_id=cat_id
        )

        assert query_mock.filter_by.call_count == 2
        assert goods1 in result2
        assert goods2 not in result2
        assert goods3 in result2
        assert len(result2) == 2


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
    with patch("src.app.goods.db_session.add") as add_mock, patch(
        "src.app.goods.db_session.commit"
    ) as commit_mock:
        # create_goods
        result = await gcmd.create_goods(incoming_item)
        add_mock.assert_called()
        commit_mock.assert_called()
        # update_goods
        goods_mock = MagicMock()
        with patch.object(GoodsORM.query, "get", return_value=goods_mock):
            result2 = await gcmd.update_goods(incoming_item)
            assert goods_mock == result2


@pytest.mark.asyncio
async def test_update_goods_categories_success_and_fail():
    gcmd = GoodsCommands()
    goods_mock = MagicMock(categories=set())
    cat_mock = MagicMock()
    with patch.object(GoodsORM.query, "get", return_value=goods_mock), patch.object(
        CategoryORM, "query", MagicMock(get=lambda x: cat_mock)
    ), patch("src.app.goods.db_session.add"), patch("src.app.goods.db_session.commit"):
        result = await gcmd.update_goods_categories(
            goods_id=uuid4(), goods_data=[MagicMock(cat_id=uuid4())]
        )
        assert result is True

    with patch.object(GoodsORM.query, "get", return_value=goods_mock), patch.object(
        CategoryORM, "query", MagicMock(get=lambda x: cat_mock)
    ), patch("src.app.goods.db_session.add", side_effect=Exception), patch(
        "src.app.goods.db_session.commit", side_effect=Exception
    ):
        result2 = await gcmd.update_goods_categories(
            goods_id=uuid4(), goods_data=[MagicMock(cat_id=uuid4())]
        )
        assert result2 is False


@pytest.mark.asyncio
async def test_save_categorized_goods_success_and_fail():
    gcmd = GoodsCommands()
    goods_mock = MagicMock(categories=set())
    cat_mock = MagicMock()
    data = [MagicMock(goods_id=uuid4(), cat_id=uuid4())]

    with patch.object(GoodsORM.query, "get", return_value=goods_mock), patch.object(
        CategoryORM, "query", MagicMock(get=lambda x: cat_mock)
    ), patch("src.app.goods.db_session.commit"):
        result = await gcmd.save_categorized_goods(data)
        assert result is True

    with patch.object(GoodsORM.query, "get", side_effect=Exception):
        result2 = await gcmd.save_categorized_goods(data)
        assert result2 is False


@pytest.mark.asyncio
async def test_strip_all_names_calls_update_goods():
    gcmd = GoodsCommands()
    goods_list = [MagicMock(id=uuid4(), name="  item  ")]
    with patch.object(GoodsORM.query, "all", return_value=goods_list), patch.object(
        GoodsCommands, "update_goods", return_value=MagicMock()
    ):
        result = await gcmd.strip_all_names()
        assert result is True
