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
    return http.get('/user/', authHeaders(token));
  }

  updateUserProfile(
    user_profile: Object,
    token: string
  ): Promise<any> {
    return http.put('/user/', user_profile, authHeaders(token));
  }

  getAdminBoard(token: string): Promise<any>{
    return http.get('/admin/', authHeaders(token));
  }

  deleteUserProfile(
    user_id: string,
    token: string
  ): Promise<any> {
    return http.delete(`/users/${user_id}`, authHeaders(token));
  }

}

export default new UserService();