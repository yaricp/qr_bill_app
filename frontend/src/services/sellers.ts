
import http from "@/http-common";
import { authHeaders } from './';

class SellerDataService {
  getAll(offset: number, limit: number, token: string): Promise<any> {
    return http.get(
      `/sellers/?offset=${offset}&limit=${limit}`, authHeaders(token)
    );
  }

  get(id: any, token: string): Promise<any> {
    return http.get(`/sellers/${id}`, authHeaders(token));
  }

  create(data: any, token: string): Promise<any> {
    return http.post("/sellers/", data, authHeaders(token));
  }

  update(id: any, data: any, token: string): Promise<any> {
    return http.put(`/sellers/${id}`, data, authHeaders(token));
  }

  delete(id: any, token: string): Promise<any> {
    return http.delete(`/sellers/${id}`, authHeaders(token));
  }

  findByName(name: string, token: string): Promise<any> {
    return http.get(`/sellers/?name=${name}`, authHeaders(token));
  }

  getCountBillsByNameSeller(
    first_of: number, token: string
  ): Promise<any> {
    return http.get(
      `/sellers/count_bills_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }

  getSummBillsByNameSeller(
    first_of: number, token: string
  ): Promise<any> {
    return http.get(
      `/sellers/summ_bills_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }

  getCountGoodsByNameSeller(
    first_of: number, token: string
  ): Promise<any> {
    return http.get(
      `/sellers/count_goods_by_name/?first_of=${first_of}`,
      authHeaders(token)
    );
  }
}

export default new SellerDataService();
