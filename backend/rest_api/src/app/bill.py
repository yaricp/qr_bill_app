import json
from uuid import UUID
from typing import List
from decimal import Decimal
from requests import post
from loguru import logger
from datetime import datetime

from ..infra.database import db_session
from ..infra.database.models import Bill as BillORM
from ..infra.database.models import Goods as GoodsORM

from .entities.unit import Unit, UnitCreate
from .entities.bill import Bill, BillCreate
from .entities.goods import Goods, GoodsCreate
from .entities.seller import Seller, SellerCreate
from .unit import UnitCommands
from .seller import SellerCommands
from .goods import GoodsCommands
from .config import bill_config


class BillQueries:

    def __init__(self):
        pass

    async def get_all_bills(self, user_id: UUID):
        return BillORM.query.filter_by(user_id=user_id).all()

    async def get_bill(self, id: UUID):
        return BillORM.query.get(id)

    async def get_uncategorized_goods(
        self, bill_id: UUID, user_id: UUID, cat_id: UUID | None = None
    ) -> List[Goods]:
        result = []
        bill_goods = GoodsORM.query.filter_by(
            bill_id=bill_id, user_id=user_id
        ).all()
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


class BillCommands:

    def __init__(self):
        self.params = {}
        self.url_patterns = [
            "?", "#", "mapr.tax.gov.me", "ic", "verify?"
        ]
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

    async def get_by_id(self, id: UUID) -> Bill:
        return BillORM.query.get(id)

    async def create_new_bill(
        self, incoming_item: BillCreate
    ) -> Bill:
        incoming_item_dict = incoming_item.dict()
        bill = BillORM(**incoming_item_dict)
        db_session.add(bill)
        db_session.commit()
        logger.info(f"bill: {bill}")
        return bill

    async def get_by_datetime(
        self, created: datetime, user_id: UUID
    ) -> Bill:
        return BillORM.query.filter_by(
            created=created,
            user_id=user_id
        ).first()

    async def get_or_create(
        self, incoming_item: BillCreate
    ) -> Bill:
        bill = await self.get_by_datetime(
            created=incoming_item.created,
            user_id=incoming_item.user_id
        )
        if not bill:
            bill = await self.create_new_bill(
                incoming_item=incoming_item
            )
        return bill

    async def parse_link_save_bill(
        self, income_link: str, user_id: UUID
    ) -> Bill:
        if not self.validate_url(income_link):
            raise Exception("Wrong URL")
        self.params = self.get_params_from_income_url(url=income_link)
        data_bill = await self.get_data_from_fiscal_api(**self.params)
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
            user_id=user_id
        )
        logger.info(f"incoming_bill: {incoming_bill}")
        bill_db = await self.get_or_create(
            incoming_item=incoming_bill
        )
        for in_goods in income_goods_items:
            incoming_unit = UnitCreate(
                name=in_goods["unit"].strip().replace(
                    ".", ""
                ).lower()
            )
            unit_db = await self.unit_commands.get_or_create(
                incoming_item=incoming_unit
            )
            logger.info(f"in_goods: {in_goods}")
            incoming_goods = GoodsCreate(
                name=in_goods["name"].strip(),
                quantity=in_goods["quantity"],
                unit_price_before_vat=in_goods["unitPriceBeforeVat"],
                unit_price_after_vat=in_goods["unitPriceAfterVat"],
                rebate=in_goods["rebate"] if in_goods["rebate"] else Decimal(0.0),
                rebate_reducing=in_goods["rebateReducing"],
                price_before_vat=in_goods["priceBeforeVat"],
                vat_rate=in_goods["vatRate"],
                vat_amount=in_goods["vatAmount"],
                price_after_vat=in_goods["priceAfterVat"],
                unit_id=unit_db.id,
                bill_id=bill_db.id,
                seller_id=seller_db.id,
                user_id=user_id
            )
            logger.info(f"incoming_goods: {incoming_goods}")
            goods_db = await self.goods_commands.get_or_create(
                incoming_item=incoming_goods
            )
            logger.info(f"goods_db: {goods_db}")
        bill_db = await self.get_by_id(id=bill_db.id)
        return bill_db

    def get_params_from_income_url(self, url: str) -> dict:
        params = url.split("?")[1]
        parsed_param = params.split("&")
        logger.info(f"parsed_param: {parsed_param}")
        result_dict = {}
        for item in parsed_param:
            key_value = item.split("=")
            result_dict[key_value[0]] = key_value[1]
        result_dict["crtd"] = result_dict["crtd"].replace("%20", " ")
        logger.info(f"result_dict: {result_dict}")
        return result_dict

    def validate_url(self, income_link: str) -> bool:
        for pattern in self.url_patterns:
            logger.info(f"pattern: {pattern}")
            logger.info(f"income_link: {income_link}")
            if income_link.find(pattern) == -1:
                return False
        return True

    async def get_data_from_fiscal_api(self, **kwargs) -> dict:
        params = {
            "iic": kwargs["iic"],
            "tin": kwargs["tin"],
            "dateTimeCreated": kwargs["crtd"]
        }
        logger.info(f"params: {params}")
        headers = {
            "Referer": self.referer_fiscal_service_url,
            "Origin": self.origin_fiscal_service
        }
        result = post(
            url=self.fiscal_service_api_url, headers=headers, data=params
        )
        result_data = json.loads(result.content)
        return result_data

    async def get_total_summ(self, user_id: UUID) -> float:
        return 1700.0
