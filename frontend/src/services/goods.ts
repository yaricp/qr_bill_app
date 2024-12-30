
import http from "@/http-common";

class GoodsDataService {
  getAll(): Promise<any> {
    return http.get("/goods");
  }

  get(id: any): Promise<any> {
    return http.get(`/goods/${id}`);
  }

  create(data: any): Promise<any> {
    return http.post("/goods", data);
  }

  update(id: any, data: any): Promise<any> {
    return http.put(`/goods/${id}`, data);
  }

  delete(id: any): Promise<any> {
    return http.delete(`/goods/${id}`);
  }

  findByName(name: string): Promise<any> {
    return http.get(`/goods?name=${name}`);
  }

  getCountGoodsByName(first_of: number): Promise<any> {
    return http.get(`/goods/count_by_name/?first_of=${first_of}`);
  }

  getSummGoodsByName(first_of: number): Promise<any> {
    return http.get(`/goods/summ_by_name/?first_of=${first_of}`);
  }
}

export default new GoodsDataService();
