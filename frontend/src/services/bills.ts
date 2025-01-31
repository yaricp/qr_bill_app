import http from "@/http-common";
import { authHeaders } from './'

import { IBillUrl } from "@/interfaces/bills";

class BillDataService {
  getAll(token: string): Promise<any> {
    return http.get("/bills/", authHeaders(token));
  }

  get(id: any, token: string): Promise<any> {
    return http.get(`/bills/${id}`, authHeaders(token));
  }

  create(data: any, token: string): Promise<any> {
    return http.post("/bills/", data, authHeaders(token));
  }

  update(id: any, data: any, token: string): Promise<any> {
    return http.put(`/bills/${id}`, data, authHeaders(token));
  }

  delete(id: any, token: string): Promise<any> {
    return http.delete(`/bills/${id}`, authHeaders(token));
  }

  sendUrl(url_data: IBillUrl, token: string): Promise<any> {
    return http.post(`/bills/parse_url/`, url_data, authHeaders(token));
  }

  getUncategorizedGoods(
    id: string, token: string, cat_id?: string
  ): Promise<any> {
    return http.get(
      `/bills/${id}/uncategorized_goods/${cat_id ? cat_id : ""}`,
      authHeaders(token)
    );
  }

  getUncategorizedProducts(
    id: string, token: string, cat_id?: string
  ): Promise<any> {
    console.log("cat_id: ", cat_id);
    return http.get(
      `/bills/${id}/uncategorized_products/${cat_id ? cat_id : ""}`,
      authHeaders(token)
    );
  }

  getSummForMonth(
    delta_month: number, token: string
  ): Promise<any> {
    return http.get(
      `/bills/month_summ/${delta_month}`,
      authHeaders(token)
    );
  }

}

export default new BillDataService();
