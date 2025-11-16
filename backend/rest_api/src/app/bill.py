import json
import time
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from loguru import logger
from requests import post
from sqlalchemy.sql import func, text

from ..infra.database import db_session
from ..infra.database.models import Bill as BillORM
from ..infra.database.models import Goods as GoodsORM
from ..utils import (get_fisrt_day_month_by_delta_month,
                     get_last_day_of_month_by_datetime)
from .config import bill_config
from .entities.bill import Bill, BillCreate, BillCreateByURL
from .entities.goods import Goods, GoodsCreate
from .entities.product import ProductCreate
from .entities.seller import SellerCreate
from .entities.unit import UnitCreate
from .entities.user_product import UncategorizedUserProduct
from .goods import GoodsCommands
from .metrics.operations import (metric_bill_processing_time,
                                 metric_call_external_api, metric_created_bill,
                                 metric_processed_bill, metric_validated_bill)
from .product import ProductCommands
from .seller import SellerCommands
from .unit import UnitCommands, UnitQueries
from .utils import unification_names


class BillQueries:

    def __init__(self):
        pass

    async def get_all_bills(self, user_id: UUID, offset: int = 0, limit: int = 0):
        if offset > 0 and limit > 0:
            return (
                BillORM.query.filter_by(user_id=user_id)
                .offset(offset)
                .limit(limit)
                .all()
            )
        elif limit > 0:
            return BillORM.query.filter_by(user_id=user_id).limit(limit).all()
        elif offset > 0:
            return BillORM.query.filter_by(user_id=user_id).offset(offset).all()
        return BillORM.query.filter_by(user_id=user_id).all()

    async def get_bill(self, id: UUID):
        return BillORM.query.get(id)

    async def get_uncategorized_goods(
        self, bill_id: UUID, user_id: UUID, cat_id: UUID | None = None
    ) -> List[Goods]:
        result = []
        bill_goods = GoodsORM.query.filter_by(bill_id=bill_id, user_id=user_id).all()
        for u_goods in bill_goods:
            if cat_id:
                logger.info(f"u_goods.categories: {u_goods.categories}")
                if cat_id not in [item.id for item in u_goods.categories]:
                    result.append(u_goods)
            else:
                logger.info(f"u_goods.categories: {u_goods.categories}")
                if not u_goods.categories:
                    logger.info(f"added: {u_goods}")
                    result.append(u_goods)
        logger.info(f"get_uncategorized_goods result: {result}")
        return result

    async def get_uncategorized_product(
        self, bill_id: UUID, user_id: UUID, cat_id: UUID | None = None
    ) -> List[UncategorizedUserProduct]:
        logger.info(f"user_id: {user_id}")
        logger.info(f"bill_id: {bill_id}")
        logger.info(f"cat_id: {cat_id}")
        result = []
        sql_queries = {
            "cat": "SELECT user_product.id, product.name FROM goods "
            " LEFT JOIN user_product ON user_product.id = goods.user_product_id "
            " LEFT JOIN product ON user_product.product_id = product.id "
            " LEFT JOIN user_product_category "
            " ON user_product_category.user_product_id = user_product.id "
            f" WHERE goods.user_id = '{user_id}' "
            f" AND goods.bill_id = '{bill_id}' "
            " GROUP BY user_product.id, product.name "
            " HAVING SUM(CASE "
            f" WHEN user_product_category.cat_id != '{cat_id}' "
            " THEN 0 ELSE 1 END) = 0;",
            "no_cat": "SELECT user_product.id, product.name FROM goods "
            " LEFT JOIN user_product ON user_product.id = goods.user_product_id "
            " LEFT JOIN product ON user_product.product_id = product.id "
            " LEFT JOIN user_product_category "
            " ON user_product_category.user_product_id = user_product.id "
            f" WHERE goods.user_id = '{user_id}' "
            f" AND goods.bill_id = '{bill_id}' "
            " GROUP BY user_product.id, product.name "
            " HAVING COUNT(user_product_category.id) = 0;",
        }

        # result = db_session.query(
        #     ProductORM.name,
        #     func.count(CategoryORM.id).label("count")
        # ).options(lazyload(CategoryORM.products)).join(
        #     CategoryORM.products, full=True
        # ).where(
        #     CategoryORM.user_id == user_id,
        #     CategoryORM.id == cat_id,
        #     GoodsORM.user_id == user_id,
        #     GoodsORM.bill_id == bill_id,
        # ).group_by(
        #     ProductORM.name
        # ).all()
        # .having(func.count(CategoryORM.id) == 0)
        # if not cat_id:
        #     result = db_session.execute(text(
        #         "SELECT product.name, COUNT(category.id) FROM product"\
        #         " LEFT OUTER JOIN association_product_category"\
        #         " ON product.id = association_product_category.product_id"\
        #         " LEFT OUTER JOIN category ON"\
        #         " association_product_category.cat_id = category.id"\
        #         " JOIN goods ON goods.product_id = product.id"\
        #         " JOIN bill ON goods.bill_id = bill.id"\
        #         f" WHERE bill.user_id = '{user_id}'"\
        #         f" AND goods.bill_id = '{bill_id}'"\
        #         " GROUP BY product.name"\
        #         " HAVING COUNT(category.id) = 0;"
        #     ))

        if cat_id:
            logger.info(f"With cat ID: {cat_id}")
            result = db_session.execute(text(sql_queries["cat"]))
        else:
            logger.info("Without Category")
            result = db_session.execute(text(sql_queries["no_cat"]))

        logger.info(f"result: {result}")

        return result

    async def get_month_summ(self, user_id: UUID, delta_month: int) -> Decimal:
        prev_month_date = get_fisrt_day_month_by_delta_month(delta_month)
        logger.info(f"prev_month_date: {prev_month_date}")
        next_month_date = get_last_day_of_month_by_datetime(prev_month_date)
        logger.info(f"next_month_date: {next_month_date}")
        result = (
            db_session.query(func.sum(BillORM.value).label("summ"))
            .filter(
                BillORM.user_id == user_id,
                BillORM.created >= prev_month_date,
                BillORM.created <= next_month_date,
            )
            .all()
        )
        logger.info(f"result: {result}")
        logger.info(f"result: {result[0].summ}")
        return Decimal(result[0].summ) if result[0].summ else Decimal(0)


class BillCommands:

    def __init__(self):
        self.params = {}
        self.url_patterns = ["?", "#", "mapr.tax.gov.me", "ic", "verify?"]
        self.referer_fiscal_service_url = (
            f"{bill_config.FISCAL_SERVICE_HOSTNAME}{bill_config.FISCAL_SERVICE_URI}"
        )
        self.origin_fiscal_service = bill_config.FISCAL_SERVICE_HOSTNAME
        self.fiscal_service_api_url = (
            f"{self.referer_fiscal_service_url}{bill_config.FISCAL_SERVICE_API_URI}"
        )
        self.seller_commands = SellerCommands()
        self.goods_commands = GoodsCommands()
        self.unit_commands = UnitCommands()
        self.unit_queries = UnitQueries()
        self.product_commands = ProductCommands()

    async def get_by_id(self, id: UUID) -> Bill:
        return BillORM.query.get(id)

    async def create_new_bill(self, incoming_item: BillCreate) -> Bill:
        incoming_item_dict = incoming_item.dict()
        bill = BillORM(**incoming_item_dict)
        try:
            db_session.add(bill)
            db_session.commit()
        except Exception as e:
            logger.error(f"Exception: {e}")
            metric_created_bill("failure")
            raise e
        metric_created_bill("success")
        logger.info(f"bill: {bill}")
        return bill

    async def get_by_all(
        self, created: datetime, value: Decimal, user_id: UUID, seller_id: UUID
    ) -> Bill:
        return BillORM.query.filter_by(
            created=created, user_id=user_id, value=value, seller_id=seller_id
        ).first()

    async def get_or_create(self, incoming_item: BillCreate) -> Bill:
        bill = await self.get_by_all(
            created=incoming_item.created,
            user_id=incoming_item.user_id,
            value=incoming_item.value,
            seller_id=incoming_item.seller_id,
        )
        if not bill:
            bill = await self.create_new_bill(incoming_item=incoming_item)
        return bill

    async def parse_link_save_bill(
        self, income_link: BillCreateByURL, user_id: UUID
    ) -> Bill | None:
        start_time = time.time()
        if not self.validate_url(income_link.link):
            logger.error("Wrong URL")
            logger.error(f"income_link.link: {income_link.link}")
            delay = time.time() - start_time
            metric_bill_processing_time(status="failure", duration=delay)
            return None
            # raise Exception("Wrong URL")
        self.params = self.get_params_from_income_url(url=income_link.link)
        data_bill = await self.get_data_from_fiscal_api(**self.params)
        if not data_bill:
            logger.error("No data from fiscal API")
            delay = time.time() - start_time
            metric_bill_processing_time(status="failure", duration=delay)
            return None
        logger.info(f"items: {data_bill.items()}")
        bill_seller = data_bill["seller"]
        income_goods_items = data_bill["items"]
        logger.info(f"bill_seller: {bill_seller}")
        logger.info(f"income_goods_items: {income_goods_items}")
        correct_address = None
        if bill_seller["address"]:
            correct_address = bill_seller["address"].strip()
        correct_town = None
        if bill_seller["town"]:
            correct_town = bill_seller["town"].strip()
        incoming_seller = SellerCreate(
            official_name=bill_seller["name"].strip(),
            address=correct_address,
            city=correct_town,
        )
        seller_db = await self.seller_commands.get_or_create(
            incoming_item=incoming_seller
        )
        logger.info(f"paymentMethod: {data_bill["paymentMethod"]}")
        incoming_bill = BillCreate(
            created=data_bill["dateTimeCreated"],
            value=data_bill["totalPrice"],
            payment_method=data_bill["paymentMethod"][0]["type"].strip(),
            seller_id=seller_db.id,
            user_id=user_id,
            image=income_link.image,
        )
        logger.info(f"incoming_bill: {incoming_bill}")
        bill_db = await self.get_or_create(incoming_item=incoming_bill)
        if not bill_db:
            delay = time.time() - start_time
            metric_bill_processing_time(status="failure", duration=delay)
            return None
        logger.info(f"created bill: {bill_db}")
        for in_goods in income_goods_items:
            incoming_unit = UnitCreate(
                name=in_goods["unit"].strip().replace(".", "").lower()
            )
            unit_db = await self.unit_commands.get_or_create(
                incoming_item=incoming_unit
            )
            logger.info(f"in_goods: {in_goods}")
            name_goods_product = unification_names(in_goods["name"])
            income_product = ProductCreate(name=name_goods_product)
            user_product_db = await self.product_commands.get_or_create_user_product(
                incoming_item=income_product, user_id=user_id
            )
            fiscal_id = int(in_goods["id"]) if in_goods["id"] else None
            logger.info(f"Preparing Good for {name_goods_product}")
            incoming_goods = GoodsCreate(
                fiscal_id=fiscal_id,
                name=name_goods_product,
                quantity=in_goods["quantity"],
                unit_price_before_vat=in_goods["unitPriceBeforeVat"],
                unit_price_after_vat=in_goods["unitPriceAfterVat"],
                rebate=in_goods["rebate"] if in_goods["rebate"] else Decimal(0.0),
                rebate_reducing=(
                    in_goods["rebateReducing"]
                    if in_goods["rebateReducing"] != None
                    else False
                ),
                price_before_vat=in_goods["priceBeforeVat"],
                vat_rate=in_goods["vatRate"],
                vat_amount=in_goods["vatAmount"],
                price_after_vat=in_goods["priceAfterVat"],
                unit_id=unit_db.id,
                bill_id=bill_db.id,
                seller_id=seller_db.id,
                user_id=user_id,
                user_product_id=user_product_db.id,
            )
            logger.info(f"incoming_goods: {incoming_goods}")
            goods_db = await self.goods_commands.get_or_create(
                incoming_item=incoming_goods
            )
            logger.info(f"goods_db: {goods_db}")

        bill_db = await self.get_by_id(id=bill_db.id)
        delay = time.time() - start_time
        metric_bill_processing_time(status="success", duration=delay)
        logger.info(f"Processed bill in {delay} seconds")
        return bill_db

    def get_params_from_income_url(self, url: str) -> dict:
        params = url.split("?")[1]
        parsed_param = params.split("&")
        logger.info(f"parsed_param: {parsed_param}")
        result_dict = {}
        for item in parsed_param:
            key_value = item.split("=")
            if len(key_value) == 2:
                result_dict[key_value[0]] = key_value[1]
        result_dict["crtd"] = (
            result_dict["crtd"]
            .replace("%20", " ")
            .replace("%2B", " ")
            .replace("%2b", " ")
            .replace("%3A", ":")
            .replace("%3a", ":")
        )
        logger.info(f"result_dict: {result_dict}")
        return result_dict

    def validate_url(self, income_link: str) -> bool:
        for pattern in self.url_patterns:
            logger.info(f"pattern: {pattern}")
            logger.info(f"income_link: {income_link}")
            if income_link.find(pattern) == -1:
                metric_validated_bill("failure")
                return False
        metric_validated_bill("success")
        return True

    async def get_data_from_fiscal_api(self, **kwargs) -> dict | None:
        params = {
            "iic": kwargs["iic"],
            "tin": kwargs["tin"],
            "dateTimeCreated": kwargs["crtd"],
        }
        logger.info(f"params: {params}")
        headers = {
            "Referer": self.referer_fiscal_service_url,
            "Origin": self.origin_fiscal_service,
        }
        logger.info(f"headers: {headers}")
        start_time = time.time()
        try:
            result = post(url=self.fiscal_service_api_url, headers=headers, data=params)
        except Exception as e:
            metric_processed_bill("failure")
            logger.error(f"Exception: {e}")
            return None

        delay = time.time() - start_time
        logger.info(f"result: {result}")
        metric_call_external_api(
            api_name="fiscal_service", status=result.status_code, delay=delay
        )
        if result.status_code != 200:
            logger.error(f"Bad status code: {result.status_code}")
            metric_processed_bill("failure")
            return None
        logger.info(f"result.__dict__: {result.__dict__}")
        logger.info(f"result.content: {result.content}")
        result_data = json.loads(result.content)
        logger.info(f"result_data: {result_data}")
        metric_processed_bill("success")
        return result_data

    async def get_total_summ(self, user_id: UUID) -> float:
        return 1700.0

    async def create_bill_manually(self, incoming_data: BillCreate) -> Bill:
        incoming_seller = SellerCreate(
            official_name=unification_names(incoming_data.seller.strip())
        )
        seller_db = await self.seller_commands.get_or_create(
            incoming_item=incoming_seller
        )
        incoming_bill = BillCreate(
            created=incoming_data.created,
            value=incoming_data.sum,
            payment_method="cash",
            seller_id=seller_db.id,
            user_id=incoming_data.user_id,
        )
        logger.info(f"incoming_bill: {incoming_bill}")
        bill_db = await self.get_or_create(incoming_item=incoming_bill)
        logger.info(f"created bill: {bill_db}")
        name_goods_product = unification_names(incoming_data.product)
        income_product = ProductCreate(name=name_goods_product)
        user_product_db = await self.product_commands.get_or_create_user_product(
            incoming_item=income_product, user_id=incoming_data.user_id
        )
        unit_db = await self.unit_queries.get_by_name("kom")
        incoming_goods = GoodsCreate(
            name=name_goods_product,
            quantity=1,
            unit_price_before_vat=incoming_data.sum,
            unit_price_after_vat=incoming_data.sum,
            rebate=Decimal(0.0),
            rebate_reducing=False,
            price_before_vat=incoming_data.sum,
            vat_rate=Decimal(0.0),
            vat_amount=Decimal(0.0),
            price_after_vat=incoming_data.sum,
            unit_id=unit_db.id,
            bill_id=bill_db.id,
            seller_id=seller_db.id,
            user_id=incoming_data.user_id,
            user_product_id=user_product_db.id,
        )
        logger.info(f"incoming_goods: {incoming_goods}")
        goods_db = await self.goods_commands.get_or_create(incoming_item=incoming_goods)
        logger.info(f"goods_db: {goods_db}")

        bill_db = await self.get_by_id(id=bill_db.id)
        return bill_db
