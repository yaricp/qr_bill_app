
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
}

export default new GoodsDataService();
