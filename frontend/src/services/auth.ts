import axios from 'axios';
import { apiUrl, prefixUrl } from '@/env';
// const apiUrl = 'http://localhost:8080/api/v1';

import http from "@/http-common";
import { IUserLogin } from "@/interfaces/users";

class AuthService {
  
  async login(user: IUserLogin): Promise<any> {
    const formData = new FormData();
    formData.append("username", user.login);
    formData.append("password", user.password)
    return await axios.post(`${apiUrl}${prefixUrl}/auth/login/`, formData);
  }
  
  async login_by_tg(link: string): Promise<any> {
    try {
      let response = await axios.post(
        `${apiUrl}${prefixUrl}/auth/login_by_tg/`, {"link": link}
      );
      return response.data.access_token;
    } catch(e) {
      console.log("Error login", e);
    }
  }

  logout() {
    localStorage.removeItem('token');
  }

  register(user: IUserLogin) {
    return http.post('/register/', {
      username: user.login,
      password: user.password
    });
  }
}

export default new AuthService();
