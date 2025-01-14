import { authHeaders } from ".";
import http from "@/http-common";
import { IUser, IUserLogin } from "@/interfaces/users";

class UserService {

  createUser(user_data: IUserLogin, token: string): Promise<any> {
    return http.post('/users/', user_data, authHeaders(token));
  }

  getUsers(token: string): Promise<any> {
    return http.get('/users/', authHeaders(token));
  }

  getUserProfile(token: string): Promise<any> {
    console.log("http: ", http)
    return http.get('/user/', authHeaders(token));
  }

  getAdminBoard(token: string): Promise<any>{
    return http.get('/admin/', authHeaders(token));
  }
}

export default new UserService();