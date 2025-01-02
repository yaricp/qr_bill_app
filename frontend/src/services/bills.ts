
import http from "@/http-common";

import { IBillUrl } from "@/interfaces/bills";

class BillDataService {
  getAll(): Promise<any> {
    return http.get("/bills");
  }

  get(id: any): Promise<any> {
    return http.get(`/bills/${id}`);
  }

  create(data: any): Promise<any> {
    return http.post("/bills", data);
  }

  update(id: any, data: any): Promise<any> {
    return http.put(`/bills/${id}`, data);
  }

  delete(id: any): Promise<any> {
    return http.delete(`/bills/${id}`);
  }

  sendUrl(url_data: IBillUrl): Promise<any> {
    return http.post(`/bills/parse_url`, url_data);
  }

}

export default new BillDataService();
