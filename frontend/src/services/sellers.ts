
import http from "@/http-common";

class SellerDataService {
  getAll(): Promise<any> {
    return http.get("/sellers");
  }

  get(id: any): Promise<any> {
    return http.get(`/sellers/${id}`);
  }

  create(data: any): Promise<any> {
    return http.post("/sellers", data);
  }

  update(id: any, data: any): Promise<any> {
    return http.put(`/sellers/${id}`, data);
  }

  delete(id: any): Promise<any> {
    return http.delete(`/sellers/${id}`);
  }

  findByName(name: string): Promise<any> {
    return http.get(`/sellers?name=${name}`);
  }

  getCountSellerByName(first_of: number): Promise<any> {
    return http.get(`/sellers/count_by_name/?first_of=${first_of}`);
  }

  getSummSellerByName(first_of: number): Promise<any> {
    return http.get(`/sellers/summ_by_name/?first_of=${first_of}`);
  }
}

export default new SellerDataService();
