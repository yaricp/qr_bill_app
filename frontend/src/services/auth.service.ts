import axios from 'axios';
// import { apiUrl } from '@/env';
const apiUrl = 'http://localhost:8080/api/v1';

import http from "@/http-common";
import { IUserLogin } from "@/interfaces/users";

class AuthService {
  login(user: IUserLogin): Promise<any> {
    const params = new URLSearchParams();
    params.append('username', user.email);
    params.append('password', user.password);
    return axios
      .post(`${apiUrl}/auth/login`, params)
      .then(response => {
        return response.data.access_token;
      });
  }

  logout() {
    localStorage.removeItem('user');
  }

  register(user: IUserLogin) {
    return http.post('/register', {
      username: user.email,
      password: user.password
    });
  }
}

export default new AuthService();
