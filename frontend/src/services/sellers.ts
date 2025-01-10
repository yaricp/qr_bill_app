
import http from "@/http-common";
import { authHeaders } from './';

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

  getCountBillsByNameSeller(first_of: number, token: string): Promise<any> {
    return http.get(
      `/sellers/count_bills_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }

  getSummBillsByNameSeller(first_of: number, token: string): Promise<any> {
    return http.get(
      `/sellers/summ_bills_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }

  getCountGoodsByNameSeller(first_of: number, token: string): Promise<any> {
    return http.get(
      `/sellers/count_goods_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }
}

export default new SellerDataService();
