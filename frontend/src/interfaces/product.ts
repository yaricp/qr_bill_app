import { DateTimeFormatResult } from "vue-i18n";

export interface IProduct {
    id: string;
    name: string;
    categories?: string[];
  }

export interface IUncategorizedProduct {
  id: string;
  name: string;
  checked: boolean;
}

export interface ICategorizedProduct {
  user_product_id: string;
  cat_id: string;
}

export interface IProductPrice {
  price: number;
  created: DateTimeFormatResult;
  seller: string;
}