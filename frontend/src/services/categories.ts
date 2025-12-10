
import http from "@/http-common";
import { authHeaders } from "./";
import { ICategory, ICreateCategory } from "@/interfaces/categories";

class CategoriesService {
  getAll(token: string): Promise<any> {
    return http.get("/categories/", authHeaders(token));
  }

  get(id: string, token: string): Promise<any> {
    return http.get(`/categories/${id}`, authHeaders(token));
  }

  create(data: ICreateCategory, token: string): Promise<any> {
    return http.post("/categories/", data, authHeaders(token));
  }

  update(id: string, data: ICategory, token: string): Promise<any> {
    return http.put(`/categories/${id}`, data, authHeaders(token));
  }

  delete(id: string, token: string): Promise<any> {
    return http.delete(`/categories/${id}`, authHeaders(token));
  }

  findByName(name: string, token: string): Promise<any> {
    return http.get(`/categories/?name=${name}`, authHeaders(token));
  }

  getCountGoodsByNameCategory(
    first_of: number, delta_month: number, token: string
  ): Promise<any> {
    return http.get(
      `/categories/count_goods_by_name/?first_of=${first_of}&delta_month=${delta_month}`,
      authHeaders(token)
    );
  }

  getSummGoodsByNameCategory(
    first_of: number, delta_month: number, token: string
  ): Promise<any> {
    return http.get(
      `/categories/summ_goods_by_name/?first_of=${first_of}&delta_month=${delta_month}`,
      authHeaders(token)
    );
  }
}

export default new CategoriesService();
