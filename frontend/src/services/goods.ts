
import http from "@/http-common";
import { authHeaders } from "./";
import { ICategorizedGoods } from "@/interfaces/goods";

class GoodsDataService {
  getAll(token: string): Promise<any> {
    return http.get("/goods", authHeaders(token));
  }

  get(id: any, token: string): Promise<any> {
    return http.get(`/goods/${id}`, authHeaders(token));
  }

  create(data: any, token: string): Promise<any> {
    return http.post("/goods", data, authHeaders(token));
  }

  update(id: any, data: any, token: string): Promise<any> {
    return http.put(`/goods/${id}`, data, authHeaders(token));
  }

  delete(id: any, token: string): Promise<any> {
    return http.delete(`/goods/${id}`, authHeaders(token));
  }

  findByName(name: string, token: string): Promise<any> {
    return http.get(`/goods?name=${name}`, authHeaders(token));
  }

  getUncategorized(token: string, cat_id?: string): Promise<any> {
    return http.get(
      `/goods/uncategorized/${cat_id ? cat_id : ""}`, authHeaders(token)
    );
  }

  saveCategorized(
    data: ICategorizedGoods[], token: string
  ): Promise<any> {
    return http.post(
      `/goods/save_categorized/`, data, authHeaders(token)
    );
  }

  updateCategory(
    goods_id: string, data: ICategorizedGoods[], token: string
  ): Promise<any> {
    return http.post(
      `/goods/update_category/${goods_id}`,
      data,
      authHeaders(token)
    );
  }

  getCountGoodsByName(first_of: number, token: string): Promise<any> {
    return http.get(
      `/goods/count_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }

  getSummGoodsByName(first_of: number, token: string): Promise<any> {
    return http.get(
      `/goods/summ_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }
}

export default new GoodsDataService();
