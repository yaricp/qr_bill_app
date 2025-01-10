import { ICategory } from "./categories";
import { ISeller } from "./seller";
import { IUnit } from "./units";

export interface IGoods {
    id: string;
    name: string;
    quantity: number;
    unit_price_before_vat: number;
    unit_price_after_vat: number;
    rebate: number;
    rebate_reducing: boolean;
    price_before_vat: number;
    vat_rate: number;
    vat_amount: number;
    price_after_vat: number;
    unit: IUnit;
    bill_id: string;
    seller: ISeller;
    categories: ICategory[];
  }

export interface ICountGoodsByName {
    name: string;
    count: number;
  }

export interface ISummGoodsByName {
  name: string;
  summ: number;
}

export interface IUncategorizedGoods {
  id: string;
  name: string;
  checked: boolean;
  categories: string[];
}

export interface ICategorizedGoods {
  goods_id: string;
  cat_id: string;
}