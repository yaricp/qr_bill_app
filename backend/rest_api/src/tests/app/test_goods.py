from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from src.app.goods import CategoryORM, GoodsCommands, GoodsORM, GoodsQueries
from src.app.entities.goods import GoodsCreate


async def fake_mock_result(incoming_item=None):
    return MagicMock(id=uuid4())


async def fake_mock_none(incoming_item=None):
    return None


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
@patch('src.app.goods.logger')
async def test_get_goods_by_fiscal_id_found(mock_logger):
    """

    """

    incoming_item = MagicMock()
    service_instance = GoodsCommands()
    mock_found_goods = MagicMock() 
    mock_query_filter = MagicMock()
    mock_query_filter.first.return_value = mock_found_goods
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query_filter

    with patch.object(GoodsORM, "query", mock_query):
        result = await service_instance.get_goods_by_fiscal_id(incoming_item)
        assert result is mock_found_goods 
        mock_query.filter.assert_called_once()
        mock_query_filter.first.assert_called_once()
        mock_logger.info.assert_called_with(f"goods: {mock_found_goods}")

    mock_query_filter_empty = MagicMock()
    mock_query_filter_empty.first.return_value = None
    mock_query_empty = MagicMock()
    mock_query_empty.filter.return_value = mock_query_filter_empty

    with patch.object(GoodsORM, "query", mock_query_empty):
        result = await service_instance.get_goods_by_fiscal_id(incoming_item)
        assert result is None
        mock_query_empty.filter.assert_called_once()
        mock_query_filter_empty.first.assert_called_once()
        mock_logger.info.assert_called_with("goods: None")


@pytest.mark.asyncio
@patch('src.app.goods.logger')
async def test_get_goods_by_name_quantity_summ(mock_logger):
    """

    """

    incoming_item = MagicMock()
    service_instance = GoodsCommands()
    mock_found_goods = MagicMock() 
    mock_query_filter = MagicMock()
    mock_query_filter.first.return_value = mock_found_goods
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query_filter

    with patch.object(GoodsORM, "query", mock_query):
        result = await service_instance.get_goods_by_name_quantity_summ(incoming_item)
        assert result is mock_found_goods 
        mock_query.filter.assert_called_once()
        mock_query_filter.first.assert_called_once()
        mock_logger.info.assert_called_with(f"goods: {mock_found_goods}")

    mock_query_filter_empty = MagicMock()
    mock_query_filter_empty.first.return_value = None
    mock_query_empty = MagicMock()
    mock_query_empty.filter.return_value = mock_query_filter_empty

    with patch.object(GoodsORM, "query", mock_query_empty):
        result = await service_instance.get_goods_by_name_quantity_summ(incoming_item)
        assert result is None
        mock_query_empty.filter.assert_called_once()
        mock_query_filter_empty.first.assert_called_once()
        mock_logger.info.assert_called_with("goods: None")


@pytest.mark.asyncio
@patch('src.app.goods.logger')
async def test_get_by_name_bill_id_with_empty_fiscal_id(mock_logger):
    """

    """

    incoming_item = MagicMock()
    service_instance = GoodsCommands()
    mock_found_goods = MagicMock() 
    mock_query_filter = MagicMock()
    mock_query_filter.first.return_value = mock_found_goods
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query_filter

    with patch.object(GoodsORM, "query", mock_query):
        result = await service_instance.get_by_name_bill_id_with_empty_fiscal_id(
            incoming_item
        )
        assert result is mock_found_goods 
        mock_query.filter.assert_called_once()
        mock_query_filter.first.assert_called_once()
        mock_logger.info.assert_called_with(f"goods: {mock_found_goods}")

    mock_query_filter_empty = MagicMock()
    mock_query_filter_empty.first.return_value = None
    mock_query_empty = MagicMock()
    mock_query_empty.filter.return_value = mock_query_filter_empty

    with patch.object(GoodsORM, "query", mock_query_empty):
        result = await service_instance.get_by_name_bill_id_with_empty_fiscal_id(
            incoming_item
        )
        assert result is None
        mock_query_empty.filter.assert_called_once()
        mock_query_filter_empty.first.assert_called_once()
        mock_logger.info.assert_called_with("goods: None")


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
@patch('src.app.goods.logger')
async def test_get_or_create_goods_commands_branches(mock_logger):
    gcmd = GoodsCommands()
    incoming_item = MagicMock(fiscal_id=123)

    # branch 1: fiscal_id exists
    gcmd.get_goods_by_fiscal_id = fake_mock_result
    result1 = await gcmd.get_or_create(incoming_item)
    assert result1
    mock_logger.info.assert_called_with(f"goods found by fiscal_id : {result1}")

    # branch 2: no fiscal_id, found by name/quantity/summ
    incoming_item.fiscal_id = None
    gcmd.get_goods_by_name_quantity_summ = fake_mock_result
    result2 = await gcmd.get_or_create(incoming_item)
    assert result2
    mock_logger.info.assert_called_with(
        f"goods found by name_quantity_summ : {result2}"
    )

    # branch 3: found by name_bill_id_with_empty_fiscal_id, update
    gcmd.get_goods_by_fiscal_id = fake_mock_none
    gcmd.get_goods_by_name_quantity_summ = fake_mock_none
    gcmd.get_by_name_bill_id_with_empty_fiscal_id = fake_mock_result
    gcmd.update_goods = fake_mock_result
    incoming_item = MagicMock(fiscal_id=123)
    result3 = await gcmd.get_or_create(incoming_item)
    assert result3
    mock_logger.info.assert_called_with(f"updated : {result3}")

    # branch 4: not found, create new
    gcmd.get_goods_by_fiscal_id = fake_mock_none
    gcmd.get_goods_by_name_quantity_summ = fake_mock_none
    gcmd.get_by_name_bill_id_with_empty_fiscal_id = fake_mock_none
    gcmd.create_goods = fake_mock_result
    incoming_item.fiscal_id = None
    result4 = await gcmd.get_or_create(incoming_item)
    assert result4
    mock_logger.info.assert_called_with(f"Create a new goods : {incoming_item}!")


@pytest.mark.asyncio
async def test_create_goods_commands():
    gcmd = GoodsCommands()
    test_data = {"name": "Banana", "price": 100}
    incoming_item = MagicMock()
    incoming_item.dict.return_value = test_data
    created_goods_mock = MagicMock()
    with patch("src.app.goods.GoodsORM") as MockGoodsORMClass, \
         patch("src.app.goods.db_session.add") as add_mock, \
         patch("src.app.goods.db_session.commit") as commit_mock:

        MockGoodsORMClass.return_value = created_goods_mock

        result = await gcmd.create_goods(incoming_item)

        MockGoodsORMClass.assert_called_once_with(**test_data)
        add_mock.assert_called_once_with(created_goods_mock)
        commit_mock.assert_called_once()
        assert result == created_goods_mock


@pytest.mark.asyncio
async def test_update_goods_commands():
    gcmd = GoodsCommands()
    test_data = {"name": "Banana", "price": 100}
    incoming_item = MagicMock()
    incoming_item.dict.return_value = test_data
    goods_query_mock = MagicMock()
    goods_query_mock.get.return_value = MagicMock()
    with patch.object(GoodsORM, "query", goods_query_mock), \
         patch("src.app.goods.db_session.commit") as commit_mock:

        result = await gcmd.update_goods(incoming_item)

        goods_query_mock.get.assert_called_once_with(incoming_item.id)
        commit_mock.assert_called_once()
        assert result == goods_query_mock.get.return_value


class TestUpdateGoodsCategories:

    @pytest.mark.asyncio
    async def test_update_goods_categories_success(self):
        """Тест успешного обновления категорий товара"""
        gcmd = GoodsCommands()
        goods_id = uuid4()
        cat_id = uuid4()

        old_cat = MagicMock()
        goods_mock = MagicMock()

        categories_mock = MagicMock(spec=set)
        categories_mock.__iter__ = MagicMock(return_value=iter([old_cat]))
        goods_mock.categories = categories_mock
        new_cat_mock = MagicMock()

        goods_query_mock = MagicMock()
        goods_query_mock.get.return_value = goods_mock

        category_query_mock = MagicMock()
        category_query_mock.get.return_value = new_cat_mock

        with patch.object(GoodsORM, "query", goods_query_mock), \
             patch.object(CategoryORM, "query", category_query_mock), \
             patch("src.app.goods.db_session.add") as mock_add, \
             patch("src.app.goods.db_session.commit") as mock_commit:

            result = await gcmd.update_goods_categories(
                goods_id=goods_id, 
                goods_data=[MagicMock(cat_id=cat_id)]
            )

            assert result is True
            goods_query_mock.get.assert_called_once_with(goods_id)
            category_query_mock.get.assert_called_once_with(cat_id)
            categories_mock.remove.assert_called_once_with(old_cat)
            categories_mock.add.assert_called_once_with(new_cat_mock)
            mock_add.assert_called_once_with(goods_mock)
            mock_commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_goods_categories_fail_on_commit(self):
        """Тест: ошибка при сохранении в БД"""
        gcmd = GoodsCommands()
        goods_id = uuid4()
        cat_id = uuid4()

        categories_mock = MagicMock(spec=set)
        categories_mock.__iter__ = MagicMock(return_value=iter([]))
        
        goods_mock = MagicMock()
        goods_mock.categories = categories_mock
        cat_mock = MagicMock()

        goods_query_mock = MagicMock()
        goods_query_mock.get.return_value = goods_mock

        category_query_mock = MagicMock()
        category_query_mock.get.return_value = cat_mock

        with patch.object(GoodsORM, "query", goods_query_mock), \
             patch.object(CategoryORM, "query", category_query_mock), \
             patch("src.app.goods.db_session.add") as mock_add, \
             patch("src.app.goods.db_session.commit", side_effect=Exception("DB Error")):

            result = await gcmd.update_goods_categories(
                goods_id=goods_id, 
                goods_data=[MagicMock(cat_id=cat_id)]
            )

            assert result is False
            mock_add.assert_called_once_with(goods_mock)

    @pytest.mark.asyncio
    async def test_update_goods_categories_multiple_categories(self):
        """Тест: обновление нескольких категорий"""
        gcmd = GoodsCommands()
        goods_id = uuid4()
        cat_id1 = uuid4()
        cat_id2 = uuid4()

        old_cat1 = MagicMock()
        old_cat2 = MagicMock()

        categories_mock = MagicMock(spec=set)
        categories_mock.__iter__ = MagicMock(
            return_value=iter([old_cat1, old_cat2])
        )

        goods_mock = MagicMock()
        goods_mock.categories = categories_mock

        new_cat1_mock = MagicMock()
        new_cat2_mock = MagicMock()

        goods_query_mock = MagicMock()
        goods_query_mock.get.return_value = goods_mock

        category_query_mock = MagicMock()
        category_query_mock.get.side_effect = [new_cat1_mock, new_cat2_mock]

        with patch.object(GoodsORM, "query", goods_query_mock), \
             patch.object(CategoryORM, "query", category_query_mock), \
             patch("src.app.goods.db_session.add") as mock_add, \
             patch("src.app.goods.db_session.commit") as mock_commit:

            result = await gcmd.update_goods_categories(
                goods_id=goods_id,
                goods_data=[
                    MagicMock(cat_id=cat_id1),
                    MagicMock(cat_id=cat_id2)
                ]
            )

            assert result is True
            assert categories_mock.remove.call_count == 2
            categories_mock.remove.assert_any_call(old_cat1)
            categories_mock.remove.assert_any_call(old_cat2)
            assert categories_mock.add.call_count == 2
            categories_mock.add.assert_any_call(new_cat1_mock)
            categories_mock.add.assert_any_call(new_cat2_mock)
            mock_add.assert_called_once_with(goods_mock)
            mock_commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_goods_categories_empty_categories(self):
        """Тест: удаление всех категорий (пустой список)"""
        gcmd = GoodsCommands()
        goods_id = uuid4()
        old_cat = MagicMock()

        categories_mock = MagicMock(spec=set)
        categories_mock.__iter__ = MagicMock(return_value=iter([old_cat]))
        goods_mock = MagicMock()
        goods_mock.categories = categories_mock
        goods_query_mock = MagicMock()
        goods_query_mock.get.return_value = goods_mock

        with patch.object(GoodsORM, "query", goods_query_mock), \
             patch("src.app.goods.db_session.add") as mock_add, \
             patch("src.app.goods.db_session.commit") as mock_commit:

            result = await gcmd.update_goods_categories(
                goods_id=goods_id,
                goods_data=[]  # Пустой список - удаляем все категории
            )

            assert result is True
            categories_mock.remove.assert_called_once_with(old_cat)
            categories_mock.add.assert_not_called()
            mock_add.assert_called_once_with(goods_mock)
            mock_commit.assert_called_once()


@pytest.mark.asyncio
async def test_save_categorized_goods_success():
    gcmd = GoodsCommands()

    goods_id = uuid4()
    cat_id = uuid4()
    data = [MagicMock(goods_id=goods_id, cat_id=cat_id)]

    mock_goods = MagicMock()
    mock_goods.categories = MagicMock() # Чтобы отследить .add()

    mock_cat = MagicMock()

    query_mock = MagicMock()

    def get_side_effect(uid):
        if uid == goods_id:
            return mock_goods
        if uid == cat_id:
            return mock_cat
        return None

    query_mock.get.side_effect = get_side_effect

    with patch.object(GoodsORM, "query", query_mock), \
         patch.object(CategoryORM, "query", query_mock), \
         patch("src.app.goods.db_session.commit") as mock_commit:

        result = await gcmd.save_categorized_goods(data)

        assert result is True

        mock_goods.categories.add.assert_called_with(mock_cat)
        mock_commit.assert_called_once()


@pytest.mark.asyncio
async def test_strip_all_names_calls_update_goods():
    gcmd = GoodsCommands()
    goods_list = [MagicMock(id=uuid4(), name="  item  ")]
    with patch.object(
        GoodsORM.query, "all", return_value=goods_list
    ), patch.object(
        GoodsCommands, "update_goods", return_value=MagicMock()
    ):
        result = await gcmd.strip_all_names()
        assert result is True
