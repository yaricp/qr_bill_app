export interface IProduct {
    id: string;
    name: string;
    categories: string[];
  }

export interface IUncategorizedProduct {
  id: string;
  name: string;
  checked: boolean;
  categories: string[];
}

export interface ICategorizedProduct {
  product_id: string;
  cat_id: string;
}