
import http from "@/http-common";
import { authHeaders } from ".";
import { 
  IProduct, ICategorizedProduct, IUncategorizedProduct
} from "@/interfaces/product";
import { IUserProductCategories } from "@/interfaces/user_products";

class ProductDataService {
  getAll(token: string): Promise<any> {
    return http.get("/products/", authHeaders(token));
  }

  get(id: any, token: string): Promise<any> {
    return http.get(`/products/${id}`, authHeaders(token));
  }

  create(data: any, token: string): Promise<any> {
    return http.post("/products/", data, authHeaders(token));
  }

  update(id: any, data: any, token: string): Promise<any> {
    return http.put(`/products/${id}`, data, authHeaders(token));
  }

  delete(id: any, token: string): Promise<any> {
    return http.delete(`/products/${id}`, authHeaders(token));
  }

  findByName(name: string, token: string): Promise<any> {
    return http.get(`/products/?name=${name}`, authHeaders(token));
  }

  getUncategorized(token: string, cat_id?: string): Promise<any> {
    return http.get(
      `/products/uncategorized/${cat_id ? cat_id : ""}`, authHeaders(token)
    );
  }

  saveCategorized(
    data: ICategorizedProduct[], token: string
  ): Promise<any> {
    return http.post(
      `/products/save_categorized/`, data, authHeaders(token)
    );
  }

  updateCategory(
    data: IUserProductCategories, token: string
  ): Promise<any> {
    return http.put(
      `/products/update_categories/`,
      data,
      authHeaders(token)
    );
  }

  getProductPrices(product_id: string, token: string): Promise<any> {
    return http.get(
      `/products/prices/${product_id}`,
      authHeaders(token)
    );
  }

  getAllWithMoreOnePrice(token: string): Promise<any> {
    return http.get("/products/for_prices/", authHeaders(token));
  }

}

export default new ProductDataService();
