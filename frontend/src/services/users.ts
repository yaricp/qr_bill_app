import authHeader from './auth-header';
import { authHeaders } from '.';
import http from "@/http-common";

class UserService {
  getUsers(token: string) {
    return http.get('/users', authHeaders(token));
  }

  getUserProfile(token: string) {
    return http.get('/user', authHeaders(token));
  }

  getAdminBoard() {
    return http.get('/admin', { headers: authHeader() });
  }
}

export default new UserService();