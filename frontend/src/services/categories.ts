
import http from "@/http-common";
import { authHeaders } from "./";
import { ICategory, ICreateCategory } from "@/interfaces/categories";

class CategoriesService {
  getAll(token: string): Promise<any> {
    return http.get("/categories", authHeaders(token));
  }

  get(id: ICategory, token: string): Promise<any> {
    return http.get(`/categories/${id}`, authHeaders(token));
  }

  create(data: ICreateCategory, token: string): Promise<any> {
    return http.post("/categories", data, authHeaders(token));
  }

  update(id: ICategory, data: any, token: string): Promise<any> {
    return http.put(`/categories/${id}`, data, authHeaders(token));
  }

  delete(id: any, token: string): Promise<any> {
    return http.delete(`/categories/${id}`, authHeaders(token));
  }

  findByName(name: string, token: string): Promise<any> {
    return http.get(`/categories?name=${name}`, authHeaders(token));
  }

  getCountGoodsByName(first_of: number, token: string): Promise<any> {
    return http.get(
      `/categories/count_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }

  getSummGoodsByName(first_of: number, token: string): Promise<any> {
    return http.get(
      `/categories/summ_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }
}

export default new CategoriesService();
