import { IProduct } from "./product";
import { ICategory } from "./categories"

export interface IUserProduct {
    id: string;
    product: IProduct;
    categories: ICategory[];
}

export interface IUserProductCategories {
    user_product_id: string;
    list_cat_id: String[];
}