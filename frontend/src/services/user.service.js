import authHeader from './auth-header';
import http from "@/http-common";

class UserService {
  getPublicContent() {
    return http.get('/users');
  }

  getUserBoard() {
    return http.get('/user', { headers: authHeader() });
  }

  getAdminBoard() {
    return http.get('/admin', { headers: authHeader() });
  }
}

export default new UserService();