import axios from 'axios';
import { apiUrl, prefixUrl } from '@/env';
import { authHeaders } from ".";

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

  async verify(link: string): Promise<any> {
    try {
      console.log("Verify by link: ", link);
      let response = await axios.post(
        `${apiUrl}${prefixUrl}/auth/verify/`, {"link": link}
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

  sendVerifyLinkToEmail(
    email: string, token: string
  ): Promise<any> {
    var data = {"email": email}
    return http.post('/auth/link_to_email/', data, authHeaders(token));
  }

  sendVerifyLinkToTG(
    tg_id: number, token: string
  ): Promise<any> {
    var data = {"tg_id": tg_id}
    return http.post('/auth/link_to_tg/', data, authHeaders(token));
  }
}

export default new AuthService();
