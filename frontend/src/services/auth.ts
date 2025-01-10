import axios from 'axios';
// import { apiUrl } from '@/env';
const apiUrl = 'http://localhost:8080/api/v1';

import http from "@/http-common";
import { IUserLogin } from "@/interfaces/users";

class AuthService {
  
  async login(user: IUserLogin): Promise<any> {
    const params = new URLSearchParams();
    params.append('username', user.login);
    params.append('password', user.password);
    try {
      let response = await axios.post(`${apiUrl}/auth/login/`, params);
      return response.data.access_token;
    } catch(e) {
      console.log("Error login", e);
    }
    // return axios
    //   .post(`${apiUrl}/auth/login/`, params)
    //   .then(response => {
    //     return response.data.access_token;
    //   });
  }
  
  async login_by_tg(link: string): Promise<any> {
    try {
      let response = await axios.post(
        `${apiUrl}/auth/login_by_tg`, {"link": link}
      );
      return response.data.access_token;
    } catch(e) {
      console.log("Error login", e);
    }
    // return axios
    //   .post(`${apiUrl}/auth/login_by_tg`, {"link": link})
    //   .then(response => {
    //     return response.data.access_token;
    //   });
  }

  logout() {
    localStorage.removeItem('token');
  }

  register(user: IUserLogin) {
    return http.post('/register', {
      username: user.login,
      password: user.password
    });
  }
}

export default new AuthService();
